#!/usr/bin/env node
/** Create the complex editable PPTX method-figure template demo. */
import fs from 'node:fs';
import path from 'node:path';
import process from 'node:process';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const PptxGenJS = require('pptxgenjs');

const output = path.resolve(process.argv[2] ?? 'examples/templates/template.pptx');
const assetDir = path.resolve(process.argv[3] ?? 'examples/templates');
const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'draw-cs-research-figures';
pptx.title = 'Complex Editable Scientific Figure Template';
pptx.theme = { headFontFace: 'Arial', bodyFontFace: 'Arial', lang: 'en-US' };
const s = pptx.addSlide(); s.background = { color: 'FFFFFF' };
const line = { color: '47789E', width: 1.5, endArrowType: 'triangle' };
const edge = (x,y,w,h,color='47789E',dash='solid') => s.addShape(pptx.shapes.LINE,{x,y,w,h,line:{...line,color,dash}});
const panel=(x,y,w,h,fill,stroke,title)=>{s.addShape(pptx.shapes.ROUNDED_RECTANGLE,{x,y,w,h,rectRadius:.05,fill:{color:fill},line:{color:stroke,width:1}});s.addText(title,{x:x+.12,y:y+.12,w:w-.24,h:.28,fontFace:'Arial',fontSize:12,bold:true,color:'172B4D',margin:0});};

// Background panels first, connectors second, entity nodes last.
panel(.2,.78,2.2,6.05,'F3F7FA','C9D6DF','Multimodal Inputs');
panel(2.6,.78,3.05,6.05,'EDF5FA','C9D6DF','View-specific Encoding');
panel(5.85,.78,4.75,6.05,'F7F2FA','D7CADF','Graph-Guided Fusion & Zoom-in');
panel(10.8,.78,2.3,6.05,'F2F8F1','CCDCCB','Predictions & Objectives');
[[2.1,1.85,.8,0],[2.1,3.55,.8,0],[2.1,5.28,.8,0],[5.25,1.85,.8,0],[5.25,3.62,.8,-.8],[5.25,5.28,2.8,-2.55],[7.5,2.2,.5,0],[9.8,2.2,1.25,0],[6.78,3.18,0,.9],[8.9,3.18,-.45,.9],[8.0,5.6,0,.6],[9.15,4.8,1.9,-2.75],[9.15,5.2,1.9,-1.45]].forEach(v=>edge(...v));
edge(12.0,2.55,0,2.45,'C96E66','dash');
edge(7.15,3.18,4.0,2.85,'8062A8','dash');
edge(9.15,3.18,2.15,3.3,'55945B','dash');

s.addText('{{FIGURE_TITLE}}',{objectName:'FIGURE_TITLE',x:.85,y:.18,w:11.7,h:.38,fontSize:20,bold:true,color:'172B4D',align:'center',margin:0});
const card=(name,text,x,y,w,h,fill,stroke,fs=12)=>s.addText(text,{objectName:name,shape:pptx.shapes.ROUNDED_RECTANGLE,x,y,w,h,fill:{color:fill},line:{color:stroke,width:1.5},fontSize:fs,bold:true,color:'172B4D',align:'center',valign:'mid',margin:.06});
card('IMAGE_INPUT','Image / Document',.5,1.35,1.6,1.05,'E1EEF6','426986');
card('TEXT_INPUT','Text Tokens',.5,3.0,1.6,1.05,'EEF0F7','5D6F91');
card('GRAPH_INPUT','Metadata Graph',.5,4.65,1.6,1.25,'EEF5EA','5A805E');
card('VISUAL_ENCODER_CARD','',2.9,1.28,2.35,1.25,'D9ECF5','426986',11);
card('LANGUAGE_ENCODER','{{LANGUAGE_ENCODER}}',2.9,2.95,2.35,1.4,'E3EBF3','426986',11);
card('GRAPH_ENCODER_CARD','',2.9,4.65,2.35,1.25,'E2F0E0','5A805E',11);
const svgData=(file)=>`data:image/svg+xml;base64,${fs.readFileSync(path.join(assetDir,file)).toString('base64')}`;
s.addImage({data:svgData('tensor-stack.svg'),objectName:'VISUAL_TENSOR',x:3.35,y:1.38,w:1.45,h:.62});
s.addText('{{VISUAL_ENCODER}}',{objectName:'VISUAL_ENCODER',x:3.03,y:2.05,w:2.08,h:.32,fontSize:10.5,bold:true,color:'172B4D',align:'center',valign:'mid',margin:0});
s.addImage({data:svgData('replacement-icon.svg'),objectName:'GRAPH_ILLUSTRATION',x:3.35,y:4.73,w:1.45,h:.62});
s.addText('{{GRAPH_ENCODER}}',{objectName:'GRAPH_ENCODER',x:3.03,y:5.42,w:2.08,h:.32,fontSize:10.5,bold:true,color:'172B4D',align:'center',valign:'mid',margin:0});
card('ATTENTION_MODULE_CARD','',6.05,1.28,1.45,1.9,'F7DFD3','C77945',11);
s.addImage({data:svgData('attention-map.svg'),objectName:'ATTENTION_MAP',x:6.35,y:1.45,w:.85,h:.78});
s.addText('Cross-modal\nAttention',{objectName:'ATTENTION_MODULE',x:6.18,y:2.38,w:1.18,h:.48,fontSize:10.5,bold:true,color:'172B4D',align:'center',valign:'mid',margin:0});
card('RELATION_GRAPH','Learned Relation\nGraph',8.0,1.28,1.8,1.9,'E6F1E3','55945B',11);
card('FUSION_MODULE','{{FUSION_MODULE}}',6.55,4.05,2.6,1.55,'E9DFF2','7E5AA6',12);
card('JOINT_REP','Joint Representation',6.85,6.2,2.05,.55,'D9E8F4','426986',10);
s.addShape(pptx.shapes.ROUNDED_RECTANGLE,{x:6.18,y:3.83,w:3.35,h:1.98,fill:{color:'FFFFFF',transparency:100},line:{color:'A25B8B',width:1.5,dash:'dash'}});
s.addText('Innovation zoom-in',{x:6.25,y:3.65,w:1.5,h:.25,fontSize:10,bold:true,color:'A25B8B',margin:0});
card('PREDICTION_HEAD','{{PREDICTION_HEAD}}',11.05,1.35,1.8,1.2,'E1F1DF','55945B',11);
card('EXPLANATION','Graph Explanation',11.05,3.15,1.8,1.2,'F5ECD8','B98B42',11);
card('TASK_LOSS','{{TASK_LOSS}}',11.1,5.0,1.7,.48,'F8DFDC','C96E66',10);
card('ALIGNMENT_LOSS','{{ALIGNMENT_LOSS}}',11.1,5.78,1.7,.48,'E9E0F4','8062A8',10);
card('GRAPH_LOSS','Graph Regularization',11.1,6.47,1.7,.42,'E3F0E0','55945B',9);
fs.mkdirSync(path.dirname(output),{recursive:true});
await pptx.writeFile({fileName:output});
console.log(`Wrote complex PPTX template: ${output}`);
