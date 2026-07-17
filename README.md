# CS Research Figure Skill

[中文](README.md) | [English](README_EN.md)

面向计算机科学与人工智能论文的可编辑科研绘图 Skill，支持方法框架图、模块图、实验数据分析、自动选图、投稿预设和自动质量检查。

## v0.3 新增能力

每次生成实验图后自动检查：

- 文字是否超出画布、刻度和标签是否重叠。
- 中文缺字、乱码和错误编码字符。
- 配色转为灰度后是否难以区分，是否具有 marker/线型冗余编码。
- PNG/TIFF 是否达到规定 DPI。
- PDF 是否包含 Type-3 或未嵌入字体。
- 自动生成 `*-audit.json`；存在 FAIL 时停止交付。

## 自动分析、选图与检查 Demo

![自动选择的重复实验箱线图](examples/auto-selection/auto-boxplot.png)

输入包含 4 种方法、每组 8 次重复实验。Skill 自动选择“箱线图 + 原始点”，应用 CVPR 双栏预设，并完成 SVG、PDF、PNG 审计。

- [输入 CSV](examples/auto-selection/repeated-runs.csv)
- [数据分析报告](examples/auto-selection/profile.txt)
- [可编辑 SVG](examples/auto-selection/auto-boxplot.svg)
- [PDF](examples/auto-selection/auto-boxplot.pdf)
- [自动检查报告](examples/auto-selection/auto-boxplot-audit.json)

## 安装

在 Codex 中发送：

```text
请使用 skill-installer 安装：https://github.com/qingfeng-qingshi/cs-research-figure-skill/tree/main/skill/draw-cs-research-figures
```

## 使用

```text
使用 $draw-cs-research-figures，分析 results.csv，自动选图，采用 CVPR 双栏预设，生成 SVG/PDF/PNG，并检查裁切、重叠、中文乱码、灰度、DPI 和 PDF 字体嵌入。
```

命令行：

```bash
python skill/draw-cs-research-figures/scripts/plot_experiments.py --input results.csv --kind auto --preset cvpr --layout double --out-prefix output/figure
python skill/draw-cs-research-figures/scripts/audit_figure.py output/figure.svg output/figure.pdf output/figure.png --strict --json-out output/figure-audit.json
```

## 原有能力

- Transformer、Attention、RAG、Agent、MoE、LoRA/Adapter、多模态和知识图谱方法图。
- 张量层叠、Token 条带、图节点、模型图标和局部放大。
- 对比图、离散消融、有序折线、热力图和箱线图。
- CVPR、NeurIPS、ICML、ACL、IEEE 和中文论文预设。

## 测试

```bash
python -m unittest discover -s tests -v
python scripts/package_skill.py
```

代码采用 MIT License。投稿前仍需核对目标会议当年的官方模板。
