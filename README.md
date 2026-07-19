# CS Research Figure Skill

[中文](README.md) | [English](README_EN.md) | 当前版本：`v0.5.1`

面向计算机科学与人工智能论文的可编辑科研绘图 Skill。它可以从方法描述、参考图和实验 CSV 中生成方法框架图、模块说明图、对比实验图和消融实验图，并自动完成数据分析、图型选择、投稿预设和质量检查。

## 核心能力

- 支持 Transformer、Attention、RAG、Agent、MoE、LoRA/Adapter、多模态模型和知识图谱。
- 在方法图中使用张量层叠、Token 条带、网络层堆叠、图节点、模型图标、损失分支和局部放大。
- 自动识别样本量、误差列、变量类型和 IQR 异常值。
- 自动选择对比图、离散消融图、有序折线图、热力图或箱线图。
- 提供 CVPR、NeurIPS、ICML、ACL、IEEE 和中文论文预设。
- 输出可编辑 SVG、PDF、PNG、源数据、场景 JSON 和机器审计报告。
- 检查文字裁切、标签重叠、中文乱码、灰度可辨识性、DPI 和 PDF 字体嵌入。
- 将参考图分区重建为原生可编辑 SVG 文字、形状、连接线和可替换局部素材。
- 使用统一 `template_manifest.json` 替换 PPTX、SVG 和 Draw.io 中的文字与局部图片。

## 生成效果

### 1. AI 方法框架图

![可编辑 AI 方法框架图](examples/method-figure/rich-example-preview.png)

包含多模态输入、张量层叠、Transformer 编码、图节点、融合模块、预测头和损失分支。对应文件：[SVG](examples/method-figure/rich-example.svg) · [场景 JSON](examples/method-figure/rich-example-spec.json)

### 2. 基线对比实验图

![基线对比实验图](examples/comparison/demo-comparison.png)

长方法名称保持水平，通过横向布局、直接数值标注和稳定方法配色提高可读性。对应文件：[SVG](examples/comparison/demo-comparison.svg) · [PDF](examples/comparison/demo-comparison.pdf) · [CSV](examples/comparison/demo-comparison.csv)

### 3. 有序消融与敏感性分析

![有序折线消融实验图](examples/ablation/demo-ablation-curves.png)

适用于层数、LoRA rank、专家数、阈值、epoch 和迭代次数等有序变量；离散 `w/o module` 配置不会被错误连接。对应文件：[SVG](examples/ablation/demo-ablation-curves.svg) · [PDF](examples/ablation/demo-ablation-curves.pdf) · [CSV](examples/ablation/demo-ablation-curves.csv)

### 4. 自动分析、选图和检查

![自动选择的重复实验箱线图](examples/auto-selection/auto-boxplot.png)

输入包含 4 种方法、每组 8 次重复实验。Skill 自动识别重复样本，选择“箱线图 + 原始点”，应用 CVPR 双栏预设，并完成三种格式的质量审计。对应文件：[SVG](examples/auto-selection/auto-boxplot.svg) · [PDF](examples/auto-selection/auto-boxplot.pdf) · [CSV](examples/auto-selection/repeated-runs.csv) · [数据分析](examples/auto-selection/profile.json) · [审计报告](examples/auto-selection/auto-boxplot-audit.json)

### 5. 统一可编辑模板替换

![PPTX 模板替换 Demo](examples/templates/demo-replaced-preview.png)

同一份[模板清单](examples/templates/template_manifest.json)和替换数据，可以同时生成[可编辑 SVG](examples/templates/demo-replaced.svg)、[Draw.io XML](examples/templates/demo-replaced.drawio)和[可编辑 PPTX](examples/templates/demo-replaced.pptx)。这个复杂 Demo 包含三路多模态输入、视觉/语言/图编码器、跨模态注意力、关系图、自适应融合局部放大、预测与三类训练目标；一次测试 8 个文字槽位和 3 个局部矢量素材替换，没有把整张图扁平化为 PNG。
### 6. 大模型、多智能体、视觉与软件系统模块库

![热门计算机与人工智能科研模块库](examples/module-library/hot-topic-module-library.png)

模块库目前包含 35 个机器可读模块，覆盖大模型与 RAG、多智能体协作、计算机视觉基础模型和 AI 软件系统。每个模块都提供中英文关键词、别名、推荐视觉原语、必须表达的科学语义和独立可编辑 SVG 素材。 35 个模块均具有不同的几何结构指纹；功能相近的模块可以共享配色和形状语言，但不会复用完整图示。对应文件：[模块目录 JSON](skill/draw-cs-research-figures/assets/module-catalog.json) · [可编辑模块总览 SVG](examples/module-library/hot-topic-module-library.svg) · [独立 SVG 素材目录](skill/draw-cs-research-figures/assets/module-icons)

### 7. 参考图结构仿绘与新内容重构

下面左侧是合成的高质量参考结构，用于提取分区比例、阅读顺序、形状语言、连接层级和配色角色；右侧使用新的研究内容重新组织，并保留 Scene JSON、稳定元素 ID 和可编辑 SVG。示例不复制具体论文内容。

#### 多智能体 RAG

![多智能体 RAG 参考结构与可编辑重绘对比](examples/imitation/multi-agent-rag/comparison.png)

文件：[参考结构 SVG](examples/imitation/multi-agent-rag/reference-structure.svg) · [目标可编辑 SVG](examples/imitation/multi-agent-rag/target-redraw.svg) · [目标 Scene JSON](examples/imitation/multi-agent-rag/target-redraw-spec.json)

#### 视觉基础模型

![视觉基础模型参考结构与可编辑重绘对比](examples/imitation/vision-foundation-model/comparison.png)

文件：[参考结构 SVG](examples/imitation/vision-foundation-model/reference-structure.svg) · [目标可编辑 SVG](examples/imitation/vision-foundation-model/target-redraw.svg) · [目标 Scene JSON](examples/imitation/vision-foundation-model/target-redraw-spec.json)

#### 大模型推理与软件系统

![大模型推理系统参考结构与可编辑重绘对比](examples/imitation/llm-serving-system/comparison.png)

文件：[参考结构 SVG](examples/imitation/llm-serving-system/reference-structure.svg) · [目标可编辑 SVG](examples/imitation/llm-serving-system/target-redraw.svg) · [目标 Scene JSON](examples/imitation/llm-serving-system/target-redraw-spec.json)
## 安装

### 在 Codex 中安装

在 Codex 对话中发送：

```text
请使用 skill-installer 安装：
https://github.com/qingfeng-qingshi/cs-research-figure-skill/tree/main/skill/draw-cs-research-figures
```

安装成功后，在新一轮任务中调用 `$draw-cs-research-figures`。

如果需要 PPTX 模板替换，进入安装后的 `draw-cs-research-figures` 目录执行一次 `npm install`。

### 手动安装

```bash
git clone https://github.com/qingfeng-qingshi/cs-research-figure-skill.git
cd cs-research-figure-skill
python -m pip install -r requirements.txt
npm install  # 可选：PPTX 模板替换需要
```

Windows PowerShell：

```powershell
Copy-Item -Recurse -Force ./skill/draw-cs-research-figures "$env:USERPROFILE/.codex/skills/"
```

macOS/Linux：

```bash
cp -R skill/draw-cs-research-figures ~/.codex/skills/
```

## 使用

这个仓库不是独立 GUI 软件。安装后，在 Codex 对话中调用 Skill，并提供以下一种或多种输入：

- 方法章节、算法描述、公式、伪代码或代码。
- 实验 CSV，包括模型、指标、数值、重复实验或误差信息。
- 仅用于提炼布局和视觉语言的参考图。
- 目标会议、期刊、栏宽、语言和输出格式。

### 用法一：根据方法描述生成框架图

```text
使用 $draw-cs-research-figures，读取 method.md。
先提取确定信息、待确认信息和图中核心论点，再生成方法总图与创新模块局部放大图。
图中需要包含张量流、Transformer 层、图推理模块、融合模块和损失分支；不要编造文中未说明的模块或维度。
采用 CVPR 双栏风格，输出可编辑 SVG、场景 JSON 和 PNG 预览，并执行自动质量检查。
```

预期输出：

```text
method.svg                 可编辑主文件
method-spec.json           节点、边、分组和样式
method-preview.png         README/PPT 预览
method-audit.json          自动检查结果
```

### 用法二：让 Skill 自动分析实验数据并选图

```text
使用 $draw-cs-research-figures，读取 results.csv。
先分析变量类型、每组样本量、误差列和异常值，再说明推荐图型及理由。
采用 NeurIPS 双栏预设，输出 SVG、PDF、PNG、数据分析 JSON 和自动检查报告。
普通文字保持水平，长标题最多分两行。
```

自动选择规则：

| 数据结构 | 自动选择 |
|---|---|
| `variant, metric, value` | 基线对比图 |
| `full / w/o module` | 离散消融图，不连线 |
| `x, series, value` | 有序折线图 |
| 方法 × 指标的稠密矩阵 | 热力图 |
| 每个方法有多次 seed/run | 箱线图 + 原始点 |

### 用法三：生成整套论文章节配图

```text
使用 $draw-cs-research-figures，读取 method.md、comparison.csv 和 ablation.csv。
统一规划方法框架图、基线对比图和消融实验图；保持模块名称、颜色语义、字体和指标格式一致。
方法图输出 SVG 与结构 JSON，实验图输出 SVG/PDF/PNG 与绘图代码。
使用 ACL 双栏预设，并为每张图生成 audit.json。
```

### 用法四：根据参考图重绘自己的内容

```text
使用 $draw-cs-research-figures，读取 reference.png 和 method.md。
先提取参考图可迁移的分区比例、阅读顺序、形状语言、连接层级、信息密度和配色角色；
不要复制论文专有文字、数据、图标或原始拓扑。
搜索 module-catalog.json，为我的大模型、多智能体、视觉或软件模块选择有科学语义的 SVG 元素，
再根据 method.md 重建节点和连接关系。
输出 reference-structure-spec.json、target-redraw-spec.json、可编辑 target-redraw.svg 和并排 comparison.png，
并检查文字裁切、连线穿过标签、元素重叠和灰度可辨识性。
```

### 用法五：检查已有科研图

```text
使用 $draw-cs-research-figures，检查 figure.svg、figure.pdf 和 figure.png。
报告文字裁切、标签重叠、中文乱码、灰度可辨识性、DPI 和 PDF 字体嵌入问题。
先不要重绘；按 FAIL、WARN、PASS 给出检查结果和修改建议。
```

### 用法六：从参考图分区重建可编辑科研图

```text
使用 $draw-cs-research-figures，通过 SAM3、VLM 和 OCR 分析 reference.png。
把面板、文字、形状、连接线和局部图标整理为区域 JSON；将文字和简单几何重建为原生 SVG，并保留稳定 ID，同时生成 template_manifest.json。只借鉴参考图的通用视觉语法，并根据 method.md 核对所有推断连接。
```

### 用法七：自动修改 PPTX、SVG 或 Draw.io 模板

```text
使用 $draw-cs-research-figures，读取 template_manifest.json 和 replacement_values.json。
替换标题、模块文字和局部插图，保持模板原有布局、字体、配色和元素 ID；输出所有可用的可编辑格式，并执行原有质量检查。
```
## 命令行使用

### 1. 分析 CSV

```bash
python skill/draw-cs-research-figures/scripts/profile_results.py results.csv \
  --json-out output/profile.json \
  --report-out output/profile.txt
```

### 2. 自动选图、套用预设并导出

```bash
python skill/draw-cs-research-figures/scripts/plot_experiments.py \
  --input results.csv \
  --kind auto \
  --preset cvpr \
  --layout double \
  --title "Performance Across Repeated Runs" \
  --out-prefix output/figure
```

`--kind` 支持 `auto`、`comparison`、`ablation`、`heatmap`、`boxplot`；`--preset` 支持 `cvpr`、`neurips`、`icml`、`acl`、`ieee`、`zh-thesis`。

### 3. 生成方法图

```bash
python skill/draw-cs-research-figures/scripts/validate_figure_spec.py method-spec.json
python skill/draw-cs-research-figures/scripts/render_svg.py method-spec.json output/method.svg
```

### 4. 单独检查已有图片

```bash
python skill/draw-cs-research-figures/scripts/audit_figure.py \
  output/figure.svg output/figure.pdf output/figure.png \
  --min-dpi 300 \
  --strict \
  --json-out output/figure-audit.json
```

审计等级：

- `FAIL`：缺字、乱码、最终裁切、低 DPI、Type-3 字体等阻断问题。
- `WARN`：估算重叠、灰度接近或字体回退，需要查看 PNG 预览。
- `PASS`：确定性检查未发现问题，仍建议人工确认科学语义。

### 5. 使用统一清单替换模板

```bash
npm install
python skill/draw-cs-research-figures/scripts/apply_template.py \
  --manifest examples/templates/template_manifest.json \
  --values examples/templates/replacement_values.json \
  --format pptx --output output/method.pptx
```

将 `--format` 改为 `svg` 或 `drawio` 可以生成其他可编辑主文件。先将 SAM3/VLM/OCR 检测结果规范化并裁剪局部元素，再重建参考图：

```bash
python skill/draw-cs-research-figures/scripts/prepare_reference_segments.py reference.png detections.json --out-dir output/segments
```


```bash
python skill/draw-cs-research-figures/scripts/reconstruct_reference.py \
  output/segments/segments.json --svg-out output/reconstructed.svg \
  --manifest-out output/template_manifest.json
```

## 实验 CSV 格式

基线对比：

```csv
variant,metric,value,std,n
Baseline Transformer,Accuracy (%),84.10,0.40,5
Proposed Method,Accuracy (%),87.30,0.30,5
```

有序消融：

```csv
panel,x,series,value,metric,x_label,panel_title
dataset_a,1,rank=4,0.84,AUC,LoRA rank,Dataset A
dataset_a,2,rank=8,0.87,AUC,LoRA rank,Dataset A
```

重复实验：

```csv
variant,metric,value,seed
Baseline,Accuracy (%),84.1,1
Baseline,Accuracy (%),84.5,2
Proposed Method,Accuracy (%),87.3,1
```

## 测试与发布

```bash
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

当前版本：`v0.5.1`。代码采用 MIT License；投稿前请核对目标会议当年的官方模板。

## 2025–2026 顶会科研绘图候选基准库

![40篇论文与100个目标Figure候选总览](examples/paper-figure-benchmark/candidate-overview.png)

第一版包含 CVPR、NeurIPS、ICML、ACL 各 10 篇论文，共 100 个计划审查的 Figure 槽位。它按方法架构、智能体图、RAG/知识图、反馈环、张量流、局部放大、定性结果、对比实验和消融实验等视觉角色分类。

当前状态为“候选总览”：正式用于重绘前，仍需逐篇核实 PDF 页码、Figure 编号、caption 和视觉质量分数。NeurIPS 2026 尚未公布录用结果，因此第一版只使用 NeurIPS 2025；ICML 2026 的 4 篇记录会在最终 PMLR 论文集发布后刷新。

文件：[可编辑总览 SVG](examples/paper-figure-benchmark/candidate-overview.svg) · [论文清单 JSON](skill/draw-cs-research-figures/references/paper-figure-benchmark/papers.json) · [100个 Figure 槽位](skill/draw-cs-research-figures/references/paper-figure-benchmark/figures.jsonl) · [统计摘要](skill/draw-cs-research-figures/references/paper-figure-benchmark/summary.json)
