#!/usr/bin/env node
/** Create the editable PPTX template used by examples/templates. */

import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const pptxgen = require('pptxgenjs');

const output = path.resolve(process.argv[2] ?? 'examples/templates/template.pptx');
const iconPath = path.resolve(process.argv[3] ?? 'examples/templates/replacement-icon.svg');
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'draw-cs-research-figures';
pptx.subject = 'Editable scientific figure template demo';
pptx.title = 'Editable Method Figure Template';
pptx.company = 'cs-research-figure-skill';
pptx.lang = 'zh-CN';
pptx.theme = {
  headFontFace: 'Arial', bodyFontFace: 'Arial', lang: 'zh-CN',
};
const slide = pptx.addSlide();
slide.background = { color: 'FFFFFF' };
slide.addText('{{FIGURE_TITLE}}', {
  objectName: 'FIGURE_TITLE', x: 1.1, y: 0.25, w: 11.1, h: 0.5,
  fontFace: 'Arial', fontSize: 24, bold: true, color: '172B4D', align: 'center', margin: 0,
});
slide.addShape(pptx.shapes.ROUNDED_RECTANGLE, {
  x: 0.9, y: 1.65, w: 3.25, h: 3.1, rectRadius: 0.08,
  fill: { color: 'EAF3F8' }, line: { color: '47789E', width: 2 },
});
const iconData = `data:image/svg+xml;base64,${fs.readFileSync(iconPath).toString('base64')}`;
slide.addImage({
  data: iconData, objectName: 'LOCAL_ILLUSTRATION', x: 1.35, y: 2.0, w: 2.35, h: 1.55,
});
slide.addText('{{MODULE_NAME}}', {
  objectName: 'MODULE_NAME', x: 1.15, y: 4.05, w: 2.75, h: 0.35,
  fontFace: 'Arial', fontSize: 17, bold: true, color: '172B4D', align: 'center', margin: 0,
});
slide.addShape(pptx.shapes.LINE, {
  x: 4.15, y: 3.15, w: 1.5, h: 0,
  line: { color: '47789E', width: 2.5, endArrowType: 'triangle' },
});
slide.addText('Editable Fusion', {
  objectName: 'FUSION_MODULE', shape: pptx.shapes.ROUNDED_RECTANGLE,
  x: 5.65, y: 1.65, w: 3.25, h: 3.1,
  fill: { color: 'F6EFE8' }, line: { color: 'C77945', width: 2 },
  fontFace: 'Arial', fontSize: 18, bold: true, color: '172B4D', align: 'center', valign: 'mid',
});
slide.addShape(pptx.shapes.LINE, {
  x: 8.9, y: 3.15, w: 1.25, h: 0,
  line: { color: '47789E', width: 2.5, endArrowType: 'triangle' },
});
slide.addText('Output', {
  objectName: 'OUTPUT_NODE', shape: pptx.shapes.ELLIPSE,
  x: 10.15, y: 2.45, w: 1.45, h: 1.45,
  fill: { color: 'EAF4E8' }, line: { color: '55945B', width: 2 },
  fontFace: 'Arial', fontSize: 16, color: '172B4D', align: 'center', valign: 'mid',
});
fs.mkdirSync(path.dirname(output), { recursive: true });
await pptx.writeFile({ fileName: output });
console.log(`Wrote PPTX template: ${output}`);
