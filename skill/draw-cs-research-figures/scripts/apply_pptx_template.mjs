#!/usr/bin/env node
/** Apply template_manifest.json to a PPTX template with pptx-automizer. */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import {
  Automizer,
  ModifyImageHelper,
  ModifyTextHelper,
  modify,
} from 'pptx-automizer';


function fail(message) {
  console.error(`ERROR: ${message}`);
  process.exit(2);
}

function readJson(filename) {
  return JSON.parse(fs.readFileSync(filename, 'utf8').replace(/^\uFEFF/, ''));
}

function replacement(values, slot) {
  const raw = values[slot.id];
  if (raw === undefined || raw === null) return null;
  if (typeof raw === 'object') return raw.value ?? raw.path ?? raw.text ?? null;
  return raw;
}

const [manifestArg, valuesArg, outputArg] = process.argv.slice(2);
if (!manifestArg || !valuesArg || !outputArg) {
  fail('usage: apply_pptx_template.mjs MANIFEST.json VALUES.json OUTPUT.pptx');
}

const manifestPath = path.resolve(manifestArg);
const valuesPath = path.resolve(valuesArg);
const outputPath = path.resolve(outputArg);
const baseDir = path.dirname(manifestPath);
const valuesDir = path.dirname(valuesPath);
const manifest = readJson(manifestPath);
const values = readJson(valuesPath);
const pptxEntry = manifest.templates?.pptx;
const relativeTemplate = typeof pptxEntry === 'string' ? pptxEntry : pptxEntry?.path;
if (!relativeTemplate) fail('manifest has no templates.pptx.path');
const templatePath = path.resolve(baseDir, relativeTemplate);
if (!fs.existsSync(templatePath)) fail(`template does not exist: ${templatePath}`);
fs.mkdirSync(path.dirname(outputPath), { recursive: true });

const pptxSlots = manifest.slots
  .map((slot) => ({ slot, selector: slot.selectors?.pptx, value: replacement(values, slot) }))
  .filter((item) => item.selector && item.value !== null);

const media = [];
for (const item of pptxSlots) {
  if (item.slot.kind === 'image' || item.slot.kind === 'svg-fragment') {
    const source = path.resolve(valuesDir, String(item.value));
    if (!fs.existsSync(source)) fail(`replacement asset does not exist: ${source}`);
    const mediaName = path.basename(source);
    media.push({ source, mediaName });
    item.mediaName = mediaName;
  }
}

const automizer = new Automizer({
  templateDir: path.dirname(templatePath),
  outputDir: path.dirname(outputPath),
  mediaDir: valuesDir,
  removeExistingSlides: true,
  autoImportSlideMasters: true,
  verbosity: 1,
});

let pres = automizer
  .loadRoot(path.basename(templatePath))
  .load(path.basename(templatePath), 'editable-template');

for (const item of media) {
  pres = pres.loadMedia(item.mediaName, path.dirname(item.source));
}

const info = await pres.getInfo();
let slides = info.slidesByTemplate('editable-template').map((slide) => slide.number);
const requestedSlides = Array.isArray(pptxEntry?.slides) ? pptxEntry.slides : null;
if (requestedSlides) slides = slides.filter((number) => requestedSlides.includes(number));

for (const slideNumber of slides) {
  pres.addSlide('editable-template', slideNumber, (slide) => {
    for (const item of pptxSlots) {
      const selector = typeof item.selector === 'string'
        ? { slide: 1, shape: item.selector }
        : item.selector;
      if ((selector.slide ?? 1) !== slideNumber) continue;
      const shape = selector.shape ?? selector.shape_name ?? selector.creation_id;
      if (!shape) fail(`${item.slot.id}: PPTX selector needs shape`);
      if (item.slot.kind === 'text') {
        if (selector.mode === 'replace-tag') {
          slide.modifyElement(shape, [modify.replaceText([{
            replace: selector.tag ?? item.slot.id,
            by: { text: String(item.value) },
          }])]);
        } else {
          slide.modifyElement(shape, [ModifyTextHelper.setText(String(item.value))]);
        }
      } else {
        const modifier = typeof ModifyImageHelper.setRelationTargetCover === 'function' && selector.fit === 'cover'
          ? ModifyImageHelper.setRelationTargetCover(item.mediaName, pres)
          : ModifyImageHelper.setRelationTarget(item.mediaName);
        slide.modifyElement(shape, [modifier]);
      }
    }
  });
}

await pres.write(path.basename(outputPath));
console.log(`Wrote editable PPTX: ${outputPath}`);

