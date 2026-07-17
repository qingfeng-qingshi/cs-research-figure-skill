# CS Research Figure Skill

面向计算机科学与人工智能论文的可编辑科研绘图 Skill。它可以从不完整的方法描述、参考图和实验数据中，规划并生成方法框架图、模块图、对比实验图与消融实验图。

当前版本：`v0.1.1`

## 主要能力

- 从算法描述、公式、伪代码或代码中提取可视化结构。
- 支持 Transformer、Attention、RAG、Agent、MoE、LoRA/Adapter、多模态模型和知识图谱。
- 在方法图中使用张量层叠、Token 条带、网络层堆叠、图节点、模型图标、损失分支和局部放大。
- 生成可编辑 SVG；实验图同时导出 SVG、PDF、PNG 和数据源。
- 长标题自动按语义分成最多两行，SVG 文字保持可编辑。
- 对有序消融变量生成多折线图；对离散 remove-one 消融保留柱状图或点图。
- 检查文字越界、节点重叠、悬空连线、斜排文字和过窄配色。

## 测试生成效果

### 方法框架图

![Editable method framework](examples/method-figure/rich-example-preview.png)

对应的 [可编辑 SVG](examples/method-figure/rich-example.svg) 和 [结构规格](examples/method-figure/rich-example-spec.json) 均由同一份场景规格生成。

### 对比实验图

![Comparison with baselines](examples/comparison/demo-comparison.png)

对应的 [SVG](examples/comparison/demo-comparison.svg)、[PDF](examples/comparison/demo-comparison.pdf) 和 [CSV](examples/comparison/demo-comparison.csv) 可复现。

### 折线消融实验

![Ablation curves](examples/ablation/demo-ablation-curves.png)

对应的 [SVG](examples/ablation/demo-ablation-curves.svg)、[PDF](examples/ablation/demo-ablation-curves.pdf) 和 [CSV](examples/ablation/demo-ablation-curves.csv) 可复现。示例数据仅用于展示，不代表真实实验结论。

## 在 Codex 中安装

推荐直接在 Codex 中发送：

```text
请使用 skill-installer 安装：
https://github.com/qingfeng-qingshi/cs-research-figure-skill/tree/main/skill/draw-cs-research-figures
```

安装成功后，从下一轮任务开始即可调用 `$draw-cs-research-figures`。

也可以手动安装：

```bash
git clone https://github.com/qingfeng-qingshi/cs-research-figure-skill.git
cd cs-research-figure-skill
python -m pip install -r requirements.txt
```

Windows PowerShell：

```powershell
Copy-Item -Recurse -Force ./skill/draw-cs-research-figures "$env:USERPROFILE/.codex/skills/"
```

macOS/Linux：

```bash
cp -R skill/draw-cs-research-figures ~/.codex/skills/
```

## 实际使用方式

这个项目不是独立GUI软件。安装后，应在 Codex 对话中明确调用 Skill，并提供论文材料、表格或参考图。

生成方法框架图：

```text
使用 $draw-cs-research-figures，读取我提供的方法章节，先提取确定信息和待确认信息，再生成方法总图与创新模块局部放大图。输出可编辑SVG、结构JSON和PNG预览，不要编造未说明的模块。
```

生成对比实验图：

```text
使用 $draw-cs-research-figures，读取 results.csv。为不同基线生成配色严谨的对比实验图，长标题最多分两行，普通文字保持水平，输出绘图代码、SVG、PDF和PNG。
```

生成折线消融图：

```text
使用 $draw-cs-research-figures，读取 ablation.csv。识别迭代次数、层数或超参数等有序横轴，生成多折线消融图；如果是 w/o module 这类离散配置，不要强行连线。
```

生成整套论文章节图：

```text
使用 $draw-cs-research-figures，根据 method.md、comparison.csv 和 ablation.csv，规划并生成方法框架图、对比实验图和消融实验图。保持模块名称、颜色与指标格式一致。
```
## 命令行复现示例

生成方法图：

```bash
python skill/draw-cs-research-figures/scripts/validate_figure_spec.py examples/method-figure/rich-example-spec.json
python skill/draw-cs-research-figures/scripts/render_svg.py examples/method-figure/rich-example-spec.json output/method.svg
```

生成对比实验图：

```bash
python skill/draw-cs-research-figures/scripts/plot_experiments.py --input examples/comparison/demo-comparison.csv --kind comparison --title "Comparison with Baselines" --out-prefix output/comparison
```

生成折线消融图：

```bash
python skill/draw-cs-research-figures/scripts/plot_experiments.py --input examples/ablation/demo-ablation-curves.csv --kind ablation --ablation-mode auto --title "Sensitivity Analysis of Feature-Combination Depth Across Multiple Evaluation Settings" --out-prefix output/ablation
```

## 数据格式

对比实验：

```csv
variant,metric,value
Baseline A,Accuracy (%),84.10
Proposed Method,Accuracy (%),87.30
```

有序折线消融：

```csv
panel,x,series,value,metric,x_label,panel_title
group_1,0,depth=2,0.730,AUC,Iteration,Feature combination group 1
```

离散删模块消融：

```csv
variant,metric,value
Full model,Accuracy (%),87.30
w/o graph reasoning,Accuracy (%),84.80
```

## 仓库结构

```text
skill/draw-cs-research-figures/  Codex Skill 本体
examples/                        README 展示与可复现实例
tests/                           自动化测试
scripts/                         发布打包工具
.github/workflows/               GitHub Actions
```

## 测试与打包

```bash
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

测试会重新生成方法图、对比图和折线消融图，并验证 SVG XML、预览PNG、文字、配色和结构。

## 当前限制

- 原生 PowerPoint 形状生成仍在开发中；当前以可编辑 SVG 为主。
- 复杂三维张量和定制插画仍需要针对论文内容精修。
- Skill 不会编造模块、指标或实验结果；缺失的科学信息会保留为待确认项。

## 许可证与素材

代码使用 MIT License。仓库不包含论文原图；参考论文只用于提炼通用结构与视觉语法。提交自己的数据或图像前，请确认相应授权。
