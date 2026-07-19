#!/usr/bin/env python3
"""Generate hot-topic module assets and reference-guided redraw examples."""

from __future__ import annotations

import argparse
import html
import json
import math
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from module_icon_raster import draw_module_icon


SKILL = Path(__file__).resolve().parents[1]
WORKSPACE = Path.cwd()
INK = "#233B53"
BLUE = "#4C86B6"
GREEN = "#5B9561"
ORANGE = "#D48345"
PURPLE = "#8062A8"
RED = "#C96863"
PALETTES = {
    "llm": ("#EAF2F8", BLUE),
    "agent": ("#F1ECF7", PURPLE),
    "vision": ("#EAF4EA", GREEN),
    "software": ("#F9F0E4", ORANGE),
}


MODULES = [
    # Large language models
    {"id": "decoder-only-llm", "family": "llm", "name": "Decoder-only LLM", "zh": "解码器大模型", "aliases": ["large language model", "foundation model", "GPT", "大模型", "基础模型"], "primitive": "stacked decoder cards with token ports", "semantics": "token sequence, causal mask, frozen/trainable state", "icon": "llm"},
    {"id": "prompt-instruction", "family": "llm", "name": "Prompt / Instruction", "zh": "提示词与指令", "aliases": ["system prompt", "instruction tuning", "prompt template", "指令微调"], "primitive": "document card feeding token cells", "semantics": "system/user roles and prompt boundary", "icon": "prompt"},
    {"id": "rag-pipeline", "family": "llm", "name": "RAG Pipeline", "zh": "检索增强生成", "aliases": ["retrieval augmented generation", "retriever", "evidence", "RAG", "检索增强"], "primitive": "query-retrieve-rerank-generate chain", "semantics": "top-k, provenance, retrieval boundary", "icon": "rag"},
    {"id": "vector-database", "family": "llm", "name": "Vector Database", "zh": "向量数据库", "aliases": ["embedding index", "ANN", "FAISS", "Milvus", "向量库"], "primitive": "database cylinder with embedding cells", "semantics": "index/query direction and similarity metric", "icon": "vector-db"},
    {"id": "reranker", "family": "llm", "name": "Reranker", "zh": "重排序器", "aliases": ["cross encoder", "relevance scoring", "重排", "相关性评分"], "primitive": "ranked document stack", "semantics": "candidate set and relevance scores", "icon": "reranker"},
    {"id": "lora-adapter", "family": "llm", "name": "LoRA / Adapter", "zh": "低秩适配器", "aliases": ["PEFT", "QLoRA", "low rank adaptation", "parameter efficient tuning", "参数高效微调"], "primitive": "narrow side branch beside frozen layer", "semantics": "frozen base, rank/bottleneck and merge", "icon": "lora"},
    {"id": "moe-routing", "family": "llm", "name": "Mixture of Experts", "zh": "混合专家", "aliases": ["MoE", "router", "top-k experts", "expert parallel", "专家路由"], "primitive": "router fan-out to expert bank", "semantics": "routing score, top-k and combine", "icon": "moe"},
    {"id": "kv-cache", "family": "llm", "name": "KV Cache", "zh": "键值缓存", "aliases": ["paged attention", "prefix cache", "continuous batching", "推理缓存"], "primitive": "paired K/V memory blocks", "semantics": "sequence length, reuse and eviction", "icon": "kv-cache"},
    {"id": "alignment-training", "family": "llm", "name": "SFT / RLHF / DPO", "zh": "大模型对齐训练", "aliases": ["preference optimization", "reward model", "human feedback", "监督微调", "偏好优化"], "primitive": "policy-reward-preference loop", "semantics": "policy, preference pairs and objective", "icon": "alignment"},
    {"id": "tool-calling", "family": "llm", "name": "Tool / Function Calling", "zh": "工具与函数调用", "aliases": ["function calling", "MCP", "API tool", "structured output", "工具调用"], "primitive": "LLM-to-tool request/result loop", "semantics": "arguments, execution result and error path", "icon": "tool"},
    # Multi-agent systems
    {"id": "planner-agent", "family": "agent", "name": "Planner Agent", "zh": "规划智能体", "aliases": ["task decomposition", "coordinator", "orchestrator", "规划器", "协调器"], "primitive": "planner card with task branches", "semantics": "plan, subtask ownership and termination", "icon": "planner"},
    {"id": "role-agent", "family": "agent", "name": "Role Agent", "zh": "角色智能体", "aliases": ["specialist agent", "worker agent", "researcher", "coder", "critic", "专家智能体"], "primitive": "person/agent node with role badge", "semantics": "role, capability and local state", "icon": "agent"},
    {"id": "multi-agent-network", "family": "agent", "name": "Multi-Agent Network", "zh": "多智能体网络", "aliases": ["agent society", "agent graph", "collaboration", "multi-agent", "智能体协作"], "primitive": "typed agent nodes with message edges", "semantics": "communication topology and direction", "icon": "multi-agent"},
    {"id": "shared-memory", "family": "agent", "name": "Shared Memory", "zh": "共享记忆", "aliases": ["blackboard", "episodic memory", "semantic memory", "scratchpad", "共享内存"], "primitive": "memory bank connected to agents", "semantics": "read/write boundary, scope and persistence", "icon": "memory"},
    {"id": "message-bus", "family": "agent", "name": "Message Bus", "zh": "智能体消息总线", "aliases": ["event bus", "mailbox", "A2A", "agent protocol", "消息传递"], "primitive": "horizontal bus with typed packets", "semantics": "sender, receiver, ordering and protocol", "icon": "message-bus"},
    {"id": "critic-verifier", "family": "agent", "name": "Critic / Verifier", "zh": "批评与验证智能体", "aliases": ["judge", "reviewer", "self reflection", "debate", "验证器", "反思"], "primitive": "evaluation node returning feedback", "semantics": "criteria, score and revision loop", "icon": "verifier"},
    {"id": "environment-loop", "family": "agent", "name": "Environment Loop", "zh": "环境交互闭环", "aliases": ["observation action loop", "GUI agent", "robot agent", "环境反馈"], "primitive": "observation-planning-action-feedback cycle", "semantics": "state, observation, action and feedback", "icon": "environment"},
    {"id": "tool-sandbox", "family": "agent", "name": "Tool Sandbox", "zh": "工具沙箱", "aliases": ["code execution", "browser", "shell", "secure tool", "代码执行沙箱"], "primitive": "isolated tool container", "semantics": "permission boundary and execution result", "icon": "sandbox"},
    # Computer vision
    {"id": "vision-transformer", "family": "vision", "name": "Vision Transformer", "zh": "视觉Transformer", "aliases": ["ViT", "Swin", "visual encoder", "image transformer", "视觉编码器"], "primitive": "patch tokens entering stacked attention blocks", "semantics": "patch size, stage depth and feature scale", "icon": "vit"},
    {"id": "patch-embedding", "family": "vision", "name": "Patch Embedding", "zh": "图像块嵌入", "aliases": ["visual tokens", "image patches", "patchify", "图像分块"], "primitive": "image grid unfolding into token cells", "semantics": "patch axis and embedding dimension", "icon": "patches"},
    {"id": "feature-pyramid", "family": "vision", "name": "Feature Pyramid", "zh": "特征金字塔", "aliases": ["FPN", "multi-scale feature", "pyramid pooling", "多尺度特征"], "primitive": "layered feature maps at decreasing resolution", "semantics": "spatial scale, channels and fusion direction", "icon": "fpn"},
    {"id": "object-detection", "family": "vision", "name": "Detection Head", "zh": "目标检测头", "aliases": ["YOLO", "DETR", "bounding box", "classification head", "目标检测"], "primitive": "image with boxes plus class/box heads", "semantics": "class, box, confidence and matching", "icon": "detection"},
    {"id": "segmentation-decoder", "family": "vision", "name": "Segmentation Decoder", "zh": "分割解码器", "aliases": ["semantic segmentation", "instance mask", "SAM", "mask decoder", "图像分割"], "primitive": "feature decoder producing colored mask", "semantics": "pixel/instance labels and resolution", "icon": "segmentation"},
    {"id": "vision-language", "family": "vision", "name": "Vision-Language Model", "zh": "视觉语言模型", "aliases": ["VLM", "CLIP", "multimodal LLM", "visual instruction", "多模态大模型"], "primitive": "vision encoder and text encoder joined by bridge", "semantics": "token interface, alignment and frozen state", "icon": "vlm"},
    {"id": "diffusion-model", "family": "vision", "name": "Diffusion Model", "zh": "扩散模型", "aliases": ["denoising", "latent diffusion", "U-Net", "DiT", "生成模型"], "primitive": "noise-to-image timeline with conditional denoiser", "semantics": "time step, condition and reverse process", "icon": "diffusion"},
    {"id": "tracking-temporal", "family": "vision", "name": "Tracking / Temporal", "zh": "跟踪与时序视觉", "aliases": ["MOT", "video understanding", "temporal attention", "光流", "目标跟踪"], "primitive": "frame strip with linked object tracks", "semantics": "time axis, identity and association", "icon": "tracking"},
    {"id": "three-d-vision", "family": "vision", "name": "3D Vision", "zh": "三维视觉", "aliases": ["NeRF", "3D Gaussian Splatting", "point cloud", "depth", "三维重建"], "primitive": "camera rays, point cloud and rendered view", "semantics": "camera pose, geometry and rendering direction", "icon": "3d"},
    # Software and AI systems
    {"id": "api-gateway", "family": "software", "name": "API Gateway", "zh": "接口网关", "aliases": ["load balancer", "request gateway", "rate limit", "API网关", "负载均衡"], "primitive": "gateway fan-out to services", "semantics": "request route, tenant and policy", "icon": "gateway"},
    {"id": "task-scheduler", "family": "software", "name": "Scheduler / Queue", "zh": "调度器与队列", "aliases": ["batching", "job queue", "priority queue", "调度", "任务队列"], "primitive": "ordered queue entering scheduler", "semantics": "priority, batch, resource and latency", "icon": "scheduler"},
    {"id": "model-serving", "family": "software", "name": "Model Serving", "zh": "模型服务", "aliases": ["inference server", "vLLM", "Triton", "GPU worker", "模型推理服务"], "primitive": "router feeding replicated GPU workers", "semantics": "replica, parallelism, batching and cache", "icon": "gpu-worker"},
    {"id": "microservice", "family": "software", "name": "Microservice", "zh": "微服务", "aliases": ["service mesh", "distributed service", "RPC", "微服务架构"], "primitive": "service cards connected by API/event edges", "semantics": "service boundary, protocol and dependency", "icon": "service"},
    {"id": "event-stream", "family": "software", "name": "Event Stream", "zh": "事件流", "aliases": ["Kafka", "message queue", "pub-sub", "stream processing", "消息队列"], "primitive": "topic bus with producers and consumers", "semantics": "topic, ordering, partition and direction", "icon": "event-stream"},
    {"id": "cache-storage", "family": "software", "name": "Cache / Storage", "zh": "缓存与存储", "aliases": ["Redis", "database", "object storage", "缓存", "数据库"], "primitive": "cache blocks plus persistent cylinder", "semantics": "read/write, consistency and lifetime", "icon": "storage"},
    {"id": "container-orchestration", "family": "software", "name": "Container Orchestration", "zh": "容器编排", "aliases": ["Kubernetes", "Docker", "pod", "autoscaling", "容器", "自动扩缩容"], "primitive": "cluster boundary with replicated containers", "semantics": "replica, placement and scaling", "icon": "container"},
    {"id": "observability", "family": "software", "name": "Observability", "zh": "可观测性", "aliases": ["metrics", "logging", "tracing", "monitoring", "日志", "链路追踪"], "primitive": "metrics/logs/traces feeding dashboard", "semantics": "signal source, aggregation and alert", "icon": "monitor"},
]


def esc(value):
    return html.escape(str(value), quote=True)


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def icon_svg(kind, x=0, y=0, w=160, h=110):
    """Return compact vector geometry for a research module icon."""
    sx, sy = w / 160, h / 110
    def p(px, py): return x + px * sx, y + py * sy
    def rect(px, py, pw, ph, fill="#DCEAF4", stroke=INK, rx=6, sw=2):
        ax, ay = p(px, py)
        return f'<rect x="{ax:.1f}" y="{ay:.1f}" width="{pw*sx:.1f}" height="{ph*sy:.1f}" rx="{rx*sx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
    def line(x1, y1, x2, y2, color=INK, sw=2, dash=""):
        a, b = p(x1, y1), p(x2, y2)
        extra = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{color}" stroke-width="{sw}"{extra}/>'
    def circle(px, py, radius, fill="#A9D1E6", stroke=INK):
        ax, ay = p(px, py)
        return f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="{radius*min(sx,sy):.1f}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    s = []
    if kind in {"llm", "vit"}:
        for i in range(4): s.append(rect(35+i*8, 19+i*5, 82, 58, ["#E7EFF6","#D8E7F2","#C8DFEC","#B5D5E6"][i], rx=7))
        for yy in (42, 57, 72): s.append(line(61, yy, 118, yy, "#FFFFFF", 3))
        if kind == "llm":
            for i in range(6): s.append(rect(22+i*17, 88, 12, 12, ["#78B7D8","#91C49A","#E6B16D"][i%3], rx=2, sw=1))
            s += [line(132,28,132,74,PURPLE,3), line(126,68,132,75,PURPLE,3), line(138,68,132,75,PURPLE,3)]
        else:
            s.append(rect(8,28,24,54,"#E6F1E3",GREEN,3))
            for i in range(1,3): s += [line(8+i*8,28,8+i*8,82,"#FFFFFF",2), line(8,28+i*18,32,28+i*18,"#FFFFFF",2)]
            s.append(line(33,55,43,55,GREEN,3))
    elif kind in {"prompt", "rag"}:
        s += [rect(18, 20, 45, 65, "#FFFFFF"), rect(98, 20, 44, 65, "#E8F1E5", GREEN), line(65, 52, 95, 52, BLUE, 3)]
        for yy in (36, 48, 60): s.append(line(27, yy, 53, yy, "#9CAEBB", 2))
        if kind == "rag": s += [circle(80,52,9,"#F5C686",ORANGE), line(74,59,66,69,ORANGE,3)]
    elif kind in {"vector-db", "storage"}:
        ax, ay = p(40, 20)
        s.append(f'<path d="M {ax:.1f} {ay+10:.1f} C {ax:.1f} {ay:.1f}, {ax+80*sx:.1f} {ay:.1f}, {ax+80*sx:.1f} {ay+10:.1f} V {ay+65*sy:.1f} C {ax+80*sx:.1f} {ay+77*sy:.1f}, {ax:.1f} {ay+77*sy:.1f}, {ax:.1f} {ay+65*sy:.1f} Z" fill="#E7F0F6" stroke="{INK}" stroke-width="2"/>')
        for i in range(5): s.append(rect(52+i*13, 40+(i%2)*15, 8, 22, ["#78B6D8","#83BE8C","#E6AD64"][i%3], rx=2, sw=1))
        if kind == "vector-db": s += [circle(132,50,9,"#E7DDF0",PURPLE), line(120,50,123,50,PURPLE,3), line(129,43,136,57,PURPLE,2)]
        else:
            s += [rect(16,20,22,22,"#F2E2CB",ORANGE,4), rect(16,48,22,22,"#DDEBF4",BLUE,4), rect(16,76,22,18,"#E6F1E3",GREEN,4), line(38,31,40,31,ORANGE,2), line(38,59,40,59,BLUE,2), line(38,85,40,85,GREEN,2)]
    elif kind in {"reranker", "scheduler"}:
        widths = [90,72,55]
        for i, ww in enumerate(widths): s.append(rect(30, 21+i*24, ww, 16, ["#B8D8E9","#D9E8F1","#F1DFC4"][i], rx=4))
        s.append(line(128,22,128,83,ORANGE,3)); s.append(line(124,78,128,84,ORANGE,3)); s.append(line(132,78,128,84,ORANGE,3))
        if kind == "reranker":
            for i, yy in enumerate((29,53,77),1): s.append(f'<text x="{p(18,yy)[0]:.1f}" y="{p(18,yy)[1]:.1f}" text-anchor="middle" font-family="Arial" font-size="13" font-weight="700" fill="{INK}">{i}</text>')
        else:
            s += [circle(18,53,13,"#FFFFFF",ORANGE), line(18,53,18,44,ORANGE,2), line(18,53,26,58,ORANGE,2)]
    elif kind == "lora":
        s += [rect(48,15,64,80,"#E4E9EE"), rect(18,30,22,50,"#F1DFC8",ORANGE), line(40,55,48,55,ORANGE,3), line(112,55,138,55,BLUE,3)]
        for yy in (30,46,62): s.append(rect(60,yy,40,10,"#AFC9DC",rx=3,sw=1))
    elif kind == "moe":
        s.append(rect(14,37,35,35,"#F1DFC8",ORANGE)); s.append(line(49,55,77,55,ORANGE,3))
        for i, yy in enumerate((14,42,70)): s += [rect(82,yy,55,22,["#D9EAF4","#E6F1E3","#EEE5F5"][i],rx=5), line(77,55,82,yy+11,BLUE,2)]
    elif kind == "kv-cache":
        s += [rect(24,23,48,62,"#D9E8F3",BLUE), rect(88,23,48,62,"#E8E1F1",PURPLE)]
        for xx in (33,45,57,97,109,121): s.append(rect(xx,35,8,38,"#FFFFFF",rx=2,sw=1))
    elif kind in {"alignment", "verifier"}:
        s += [circle(43,50,18,"#D9EAF4",BLUE), circle(116,50,18,"#E8E1F1",PURPLE), line(61,50,98,50,RED,3), line(98,65,61,65,GREEN,2,"6 4")]
        s.append(f'<path d="M {p(108,49)[0]:.1f} {p(108,49)[1]:.1f} l 6 7 l 13 -16" fill="none" stroke="{GREEN}" stroke-width="4"/>')
        if kind == "alignment": s += [rect(13,20,18,18,"#DDEBF4",BLUE,4), rect(13,72,18,18,"#F3E4D0",ORANGE,4)]
        else: s.append(f'<path d="M {p(80,15)[0]:.1f} {p(80,15)[1]:.1f} L {p(96,23)[0]:.1f} {p(96,23)[1]:.1f} L {p(93,42)[0]:.1f} {p(93,42)[1]:.1f} L {p(80,52)[0]:.1f} {p(80,52)[1]:.1f} L {p(67,42)[0]:.1f} {p(67,42)[1]:.1f} L {p(64,23)[0]:.1f} {p(64,23)[1]:.1f} Z" fill="#E7F1E4" stroke="{GREEN}" stroke-width="2"/>')
    elif kind in {"tool", "sandbox"}:
        s += [rect(25,20,110,70,"#F4E7D5",ORANGE,10)]
        if kind == "sandbox": s.append(rect(43,34,74,42,"#FFFFFF",INK,4))
        s += [line(58,45,75,55,INK,3), line(75,55,58,65,INK,3), line(84,66,109,66,BLUE,3)]
    elif kind in {"planner", "agent"}:
        s += [circle(80,34,16,"#E8E1F1",PURPLE), rect(56,52,48,35,"#EFE9F5",PURPLE,12)]
        if kind == "planner":
            for px in (25,80,135): s.append(circle(px,92,6,"#F5C686",ORANGE))
            s += [line(80,75,25,86,PURPLE,2),line(80,75,80,86,PURPLE,2),line(80,75,135,86,PURPLE,2)]
    elif kind in {"multi-agent", "message-bus"}:
        coords=[(28,28),(80,18),(132,28),(45,78),(115,78)]
        for a,b in [(0,1),(1,2),(0,3),(1,3),(1,4),(2,4),(3,4)]: s.append(line(*coords[a],*coords[b],PURPLE,2))
        for i,(px,py) in enumerate(coords): s.append(circle(px,py,10,["#A9D1E6","#E5B681","#A9CEA6","#C9B5DD","#E99F9B"][i]))
        if kind == "message-bus": s.append(rect(22,48,116,14,"#FFFFFF",PURPLE,4))
    elif kind == "memory":
        for i in range(3): s.append(rect(28+i*10,20+i*9,82,55,["#F1EAF6","#E5DAEF","#D6C6E5"][i],PURPLE,7))
        for yy in (48,61,74): s.append(line(64,yy,118,yy,"#FFFFFF",3))
    elif kind == "environment":
        s += [circle(80,55,28,"#E7F0E5",GREEN), line(80,18,118,35,BLUE,3), line(126,44,118,78,BLUE,3), line(108,88,54,88,BLUE,3), line(38,79,32,42,BLUE,3), line(42,29,68,18,BLUE,3)]
    elif kind == "patches":
        s.append(rect(18,20,58,70,"#E8F1E5",GREEN,4))
        for i in range(1,3): s += [line(18+i*19,20,18+i*19,90,"#FFFFFF",2),line(18,20+i*23,76,20+i*23,"#FFFFFF",2)]
        for i in range(5): s.append(rect(92+i*10,32+(i%2)*12,8,45,["#7FB9D7","#91C49A","#E6B26E"][i%3],rx=2,sw=1))
        s.append(line(78,55,89,55,BLUE,3))
    elif kind == "fpn":
        for i,(ww,hh) in enumerate(((85,58),(65,46),(45,34))): s.append(rect(22+i*22,23+i*9,ww,hh,["#C8E0D1","#B6D7C2","#9DC9AD"][i],GREEN,3))
    elif kind == "detection":
        s.append(rect(20,18,120,75,"#EAF2F8",BLUE,4)); s += [rect(38,33,35,31,"none",RED,2),rect(82,40,42,38,"none",ORANGE,2)]
    elif kind == "segmentation":
        s.append(rect(20,18,120,75,"#EAF2F8",BLUE,4)); ax,ay=p(20,18)
        s.append(f'<path d="M {ax+10:.1f} {ay+54:.1f} C {ax+34:.1f} {ay+20:.1f}, {ax+58:.1f} {ay+70:.1f}, {ax+80:.1f} {ay+28:.1f} C {ax+99:.1f} {ay+9:.1f}, {ax+115:.1f} {ay+22:.1f}, {ax+120:.1f} {ay+36:.1f} V {ay+75:.1f} H {ax:.1f} Z" fill="#9ACB9C" opacity=".8"/>')
    elif kind == "vlm":
        s += [rect(14,25,45,55,"#DDECF5",BLUE),rect(101,25,45,55,"#F2E7D7",ORANGE),circle(80,52,14,"#E7DDF0",PURPLE),line(59,52,66,52,BLUE,3),line(94,52,101,52,ORANGE,3)]
    elif kind == "diffusion":
        for i in range(4):
            fill=["#D5D5D5","#C9D7E4","#B3D8C0","#8EC69D"][i]
            s.append(rect(12+i*37,32,29,46,fill,GREEN,3))
            if i<3: s.append(line(41+i*37,55,49+i*37,55,PURPLE,2))
    elif kind == "tracking":
        for i in range(3):
            s.append(rect(10+i*50,26,42,58,"#E9F1F6",BLUE,3)); s.append(circle(25+i*50,48+i*3,7,"#F0B88D",ORANGE))
        s += [line(25,48,75,51,RED,2,"5 4"),line(75,51,125,54,RED,2,"5 4")]
    elif kind == "3d":
        for px,py in ((64,22),(88,28),(105,47),(91,68),(61,73),(45,49)): s.append(circle(px,py,5,"#A9D1E6",BLUE))
        s += [line(20,80,64,22,ORANGE,2),line(20,80,91,68,ORANGE,2),rect(118,28,28,44,"#E8F1E5",GREEN,3)]
    elif kind in {"gateway", "service", "gpu-worker"}:
        if kind == "gateway":
            s += [rect(12,35,38,40,"#F3E4CF",ORANGE),line(50,55,80,55,ORANGE,3)]
            for yy in (15,45,75): s += [rect(90,yy,55,22,"#E6EEF4",BLUE,5),line(80,55,90,yy+11,BLUE,2)]
        elif kind == "gpu-worker":
            for i in range(3): s.append(rect(18+i*45,28,38,55,["#D9EAF4","#E4EDF3","#E8E1F1"][i],BLUE,5))
            for i in range(3): s.append(circle(37+i*45,55,8,"#F3C07F",ORANGE))
        else:
            for i,(px,py) in enumerate(((20,20),(90,20),(55,66))): s.append(rect(px,py,50,28,["#EAF2F8","#EAF4EA","#F7ECE0"][i],[BLUE,GREEN,ORANGE][i],5))
            s += [line(70,34,90,34,BLUE,2),line(45,48,70,66,GREEN,2),line(115,48,95,66,ORANGE,2)]
    elif kind in {"event-stream", "container", "monitor"}:
        if kind == "event-stream":
            s += [rect(20,44,120,22,"#F4E4CD",ORANGE,5)]
            for px in (32,56,80,104,128): s.append(circle(px,55,5,["#8ABDD8","#9AC69E","#E5B376"][px%3]))
        elif kind == "container":
            s.append(rect(16,16,128,78,"#F3E9D9",ORANGE,8))
            for i in range(3): s.append(rect(30+i*37,34,28,42,"#FFFFFF",ORANGE,4))
        else:
            s.append(rect(20,18,120,76,"#EDF2F5",BLUE,5)); s += [line(32,74,51,55,BLUE,3),line(51,55,70,64,BLUE,3),line(70,64,91,35,GREEN,3),line(91,35,127,46,GREEN,3)]
    else:
        s += [rect(28,22,104,66,"#E8EEF3",BLUE,8),circle(80,55,16,"#FFFFFF",BLUE)]
    return "".join(s)


def write_icon(path: Path, module):
    fill, stroke = PALETTES[module["family"]]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="220" viewBox="0 0 160 110">
<rect x="1" y="1" width="158" height="108" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="2"/>
<g id="{esc(module['id'])}">{icon_svg(module['icon'])}</g>
</svg>'''
    path.write_text(svg, encoding="utf-8")


def scene(name, title, panels, nodes, edges):
    return {"id": name, "canvas": {"width": 1600, "height": 900, "background": "#FFFFFF"}, "title": title, "panels": panels, "nodes": nodes, "edges": edges}


def node(node_id, label, x, y, w, h, kind, family, subtitle=""):
    fill, stroke = PALETTES[family]
    return {"id": node_id, "label": label, "subtitle": subtitle, "x": x, "y": y, "w": w, "h": h, "kind": kind, "family": family, "fill": fill, "stroke": stroke}


def edge(edge_id, source, target, label="", style="solid", color=BLUE):
    return {"id": edge_id, "source": source, "target": target, "label": label, "style": style, "color": color}


def boundary(a, b):
    ac = (a["x"] + a["w"] / 2, a["y"] + a["h"] / 2)
    bc = (b["x"] + b["w"] / 2, b["y"] + b["h"] / 2)
    dx, dy = bc[0] - ac[0], bc[1] - ac[1]
    if abs(dx) / max(a["w"], 1) >= abs(dy) / max(a["h"], 1):
        return (a["x"] + (a["w"] if dx >= 0 else 0), ac[1]), (b["x"] + (0 if dx >= 0 else b["w"]), bc[1])
    return (ac[0], a["y"] + (a["h"] if dy >= 0 else 0)), (bc[0], b["y"] + (0 if dy >= 0 else b["h"]))


def render_scene_svg(spec, path: Path):
    w, h = spec["canvas"]["width"], spec["canvas"]["height"]
    nodes = {item["id"]: item for item in spec["nodes"]}
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker><filter id="shadow"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#263C50" flood-opacity=".12"/></filter></defs>',
           '<rect width="100%" height="100%" fill="#FFFFFF"/>',
           f'<text id="figure-title" x="{w/2}" y="58" text-anchor="middle" font-family="Arial" font-size="32" font-weight="700" fill="{INK}">{esc(spec["title"])}</text>']
    for panel in spec.get("panels", []):
        out.append(f'<g id="{esc(panel["id"])}"><rect x="{panel["x"]}" y="{panel["y"]}" width="{panel["w"]}" height="{panel["h"]}" rx="25" fill="{panel.get("fill","#F5F7F9")}" stroke="#CAD5DE" stroke-width="2"/><text x="{panel["x"]+22}" y="{panel["y"]+38}" font-family="Arial" font-size="21" font-weight="700" fill="{INK}">{esc(panel["label"])}</text></g>')
    for item in spec["edges"]:
        a, b = nodes[item["source"]], nodes[item["target"]]
        (sx, sy), (tx, ty) = boundary(a, b)
        dash = ' stroke-dasharray="10 8"' if item.get("style") != "solid" else ""
        out.append(f'<g id="{esc(item["id"])}"><path d="M {sx:.1f} {sy:.1f} L {tx:.1f} {ty:.1f}" fill="none" stroke="{item.get("color",BLUE)}" stroke-width="4"{dash} marker-end="url(#arrow)"/>')
        if item.get("label"):
            mx, my = (sx + tx) / 2, (sy + ty) / 2 - 12
            out.append(f'<text x="{mx:.1f}" y="{my:.1f}" text-anchor="middle" font-family="Arial" font-size="15" fill="#52677D" paint-order="stroke" stroke="#FFFFFF" stroke-width="7">{esc(item["label"])}</text>')
        out.append('</g>')
    for item in spec["nodes"]:
        out.append(f'<g id="{esc(item["id"])}" filter="url(#shadow)"><rect x="{item["x"]}" y="{item["y"]}" width="{item["w"]}" height="{item["h"]}" rx="18" fill="{item["fill"]}" stroke="{item["stroke"]}" stroke-width="2.5"/>')
        out.append(icon_svg(item["kind"], item["x"] + item["w"]*.23, item["y"] + 20, item["w"]*.54, item["h"]*.55))
        lines = textwrap.wrap(item["label"], width=max(12, int(item["w"] / 13))) or [item["label"]]
        base = item["y"] + item["h"] - 31 - (len(lines)-1)*20
        for index, text in enumerate(lines):
            out.append(f'<text x="{item["x"]+item["w"]/2}" y="{base+index*21}" text-anchor="middle" font-family="Arial" font-size="18" font-weight="700" fill="{INK}">{esc(text)}</text>')
        out.append('</g>')
    out.append('</svg>')
    path.write_text("\n".join(out), encoding="utf-8")


def draw_text(draw, box, value, size=22, bold=False, fill=INK):
    x, y, w, h = box
    f = font(size, bold)
    lines = textwrap.wrap(value, width=max(10, int(w / (size*.58)))) or [value]
    bbox = [draw.textbbox((0,0), line, font=f) for line in lines]
    total = sum(item[3]-item[1] for item in bbox) + max(0,len(lines)-1)*5
    cy = y + (h-total)/2
    for line, bb in zip(lines,bbox):
        tw, th = bb[2]-bb[0], bb[3]-bb[1]
        draw.text((x+(w-tw)/2,cy),line,font=f,fill=fill)
        cy += th+5


def draw_icon(draw, kind, box):
    draw_module_icon(draw, kind, box)


def render_scene_png(spec, path: Path):
    w,h=spec["canvas"]["width"],spec["canvas"]["height"]
    image=Image.new("RGB",(w,h),"white"); draw=ImageDraw.Draw(image)
    draw_text(draw,(80,18,w-160,55),spec["title"],30,True)
    for panel in spec.get("panels",[]):
        draw.rounded_rectangle((panel["x"],panel["y"],panel["x"]+panel["w"],panel["y"]+panel["h"]),radius=25,fill=panel.get("fill","#F5F7F9"),outline="#CAD5DE",width=2)
        draw.text((panel["x"]+22,panel["y"]+14),panel["label"],font=font(20,True),fill=INK)
    nodes={item["id"]:item for item in spec["nodes"]}
    for item in spec["edges"]:
        start,end=boundary(nodes[item["source"]],nodes[item["target"]]); color=item.get("color",BLUE)
        draw.line((*start,*end),fill=color,width=4)
        angle=math.atan2(end[1]-start[1],end[0]-start[0]); size=13
        draw.polygon([end,(end[0]-size*math.cos(angle-.45),end[1]-size*math.sin(angle-.45)),(end[0]-size*math.cos(angle+.45),end[1]-size*math.sin(angle+.45))],fill=color)
    for item in spec["nodes"]:
        draw.rounded_rectangle((item["x"],item["y"],item["x"]+item["w"],item["y"]+item["h"]),radius=18,fill=item["fill"],outline=item["stroke"],width=3)
        draw_icon(draw,item["kind"],(item["x"]+item["w"]*.22,item["y"]+15,item["w"]*.56,item["h"]*.56))
        draw_text(draw,(item["x"]+10,item["y"]+item["h"]*.66,item["w"]-20,item["h"]*.31),item["label"],17,True)
    image.save(path)


def comparison(reference: Path, target: Path, output: Path):
    left=Image.open(reference).convert("RGB"); right=Image.open(target).convert("RGB")
    left.thumbnail((900,510)); right.thumbnail((900,510))
    canvas=Image.new("RGB",(1920,650),"#F7F8FA"); draw=ImageDraw.Draw(canvas)
    draw.rounded_rectangle((20,80,930,620),radius=20,fill="white",outline="#CCD5DD",width=2)
    draw.rounded_rectangle((990,80,1900,620),radius=20,fill="white",outline="#CCD5DD",width=2)
    draw_text(draw,(30,15,890,50),"Reference layout grammar",28,True)
    draw_text(draw,(1000,15,890,50),"Editable redraw with new content",28,True)
    canvas.paste(left,(25+(900-left.width)//2,95)); canvas.paste(right,(995+(900-right.width)//2,95))
    draw.line((940,340,980,340),fill=BLUE,width=5); draw.polygon([(980,340),(963,330),(963,350)],fill=BLUE)
    canvas.save(output)


def examples():
    panels3=[{"id":"p1","label":"Inputs & Context","x":35,"y":95,"w":410,"h":745,"fill":"#F4F7FA"},{"id":"p2","label":"Core Reasoning","x":465,"y":95,"w":690,"h":745,"fill":"#F7F3FA"},{"id":"p3","label":"Actions & Objectives","x":1175,"y":95,"w":390,"h":745,"fill":"#F3F8F2"}]
    return [
      ("multi-agent-rag",
       scene("agent-reference","Centralized Tool-Augmented Agent",panels3,
        [node("query","User Query",90,180,290,160,"prompt","llm"),node("planner","Central Planner",555,155,250,185,"planner","agent"),node("retrieval","Document Retrieval",850,155,250,185,"rag","llm"),node("worker","Single Worker Agent",555,465,250,185,"agent","agent"),node("memory","Shared Memory",850,465,250,185,"memory","agent"),node("answer","Final Answer",1225,250,285,175,"verifier","agent"),node("tools","External Tools",1225,520,285,175,"tool","software")],
        [edge("r1","query","planner"),edge("r2","planner","retrieval"),edge("r3","planner","worker"),edge("r4","retrieval","memory"),edge("r5","memory","worker"),edge("r6","worker","answer"),edge("r7","worker","tools"),edge("r8","tools","worker","result","dashed",ORANGE)]),
       scene("agent-target","Collaborative Multi-Agent RAG with Verification",panels3,
        [node("query","Multimodal Request",90,180,290,160,"prompt","llm"),node("planner","Planner Agent",505,140,210,165,"planner","agent"),node("researcher","Retrieval Agent",755,140,210,165,"rag","agent"),node("coder","Tool Agent",1005,140,110,165,"sandbox","agent"),node("bus","Agent Message Bus",555,380,510,135,"message-bus","agent"),node("memory","Vector + Episodic Memory",555,590,240,170,"vector-db","llm"),node("verifier","Critic / Verifier",835,590,230,170,"verifier","agent"),node("answer","Grounded Response",1225,205,285,175,"llm","llm"),node("tools","Tool Sandbox",1225,520,285,175,"sandbox","software")],
        [edge("t1","query","planner"),edge("t2","planner","researcher"),edge("t3","planner","coder"),edge("t4","planner","bus"),edge("t5","researcher","bus"),edge("t6","coder","bus"),edge("t7","bus","memory"),edge("t8","bus","verifier"),edge("t9","verifier","answer"),edge("t10","coder","tools"),edge("t11","tools","coder","observation","dashed",ORANGE)])),
      ("vision-foundation-model",
       scene("vision-reference","Multi-Scale Visual Recognition Pipeline",panels3,
        [node("image","Input Image",90,180,290,180,"patches","vision"),node("backbone","CNN Backbone",530,160,250,185,"vit","vision"),node("pyramid","Feature Pyramid",840,160,250,185,"fpn","vision"),node("attention","Spatial Attention",685,470,250,180,"alignment","vision"),node("detect","Detection Head",1225,180,285,170,"detection","vision"),node("segment","Segmentation Head",1225,500,285,170,"segmentation","vision")],
        [edge("r1","image","backbone"),edge("r2","backbone","pyramid"),edge("r3","pyramid","attention"),edge("r4","attention","detect"),edge("r5","attention","segment")]),
       scene("vision-target","Prompt-Guided Vision Foundation Model",panels3,
        [node("image","High-Resolution Image",75,150,310,180,"patches","vision"),node("prompt","Text / Point Prompt",75,500,310,170,"prompt","llm"),node("visual","Vision Transformer",500,135,250,185,"vit","vision"),node("promptenc","Prompt Encoder",500,500,250,170,"llm","llm"),node("cross","Cross-Modal Attention",820,250,270,190,"alignment","vision"),node("decoder","Multi-Scale Decoder",820,550,270,170,"fpn","vision"),node("mask","Open-Vocabulary Mask",1215,145,300,175,"segmentation","vision"),node("box","Grounded Boxes",1215,385,300,175,"detection","vision"),node("embed","Aligned Embeddings",1215,625,300,150,"vlm","vision")],
        [edge("t1","image","visual"),edge("t2","prompt","promptenc"),edge("t3","visual","cross"),edge("t4","promptenc","cross"),edge("t5","cross","decoder"),edge("t6","decoder","mask"),edge("t7","decoder","box"),edge("t8","cross","embed") ])),
      ("llm-serving-system",
       scene("system-reference","Scalable LLM Inference Service",panels3,
        [node("request","API Request",90,180,290,170,"gateway","software"),node("gateway","API Gateway",520,155,240,175,"gateway","software"),node("scheduler","Batch Scheduler",820,155,240,175,"scheduler","software"),node("workers","GPU Model Workers",650,475,300,190,"gpu-worker","software"),node("cache","KV Cache",1225,175,285,165,"kv-cache","llm"),node("response","Streaming Response",1225,500,285,165,"event-stream","software")],
        [edge("r1","request","gateway"),edge("r2","gateway","scheduler"),edge("r3","scheduler","workers"),edge("r4","workers","cache"),edge("r5","cache","workers","reuse","dashed",PURPLE),edge("r6","workers","response")]),
       scene("system-target","Multi-Tenant Agentic LLM Serving Platform",panels3,
        [node("request","Tenant Requests",70,155,320,170,"gateway","software"),node("events","Event Stream",70,500,320,160,"event-stream","software"),node("router","Intent + Model Router",495,130,250,175,"gateway","software"),node("scheduler","Priority Scheduler",800,130,250,175,"scheduler","software"),node("agents","Agent Worker Pool",495,465,250,190,"multi-agent","agent"),node("gpu","GPU Inference Pool",800,465,250,190,"gpu-worker","software"),node("cache","Paged KV Cache",1195,125,330,160,"kv-cache","llm"),node("tools","Isolated Tool Runtime",1195,365,330,160,"sandbox","agent"),node("monitor","Metrics / Traces / Cost",1195,605,330,150,"monitor","software")],
        [edge("t1","request","router"),edge("t2","events","agents"),edge("t3","router","scheduler"),edge("t4","router","agents"),edge("t5","scheduler","gpu"),edge("t6","agents","gpu"),edge("t7","gpu","cache"),edge("t8","cache","gpu","reuse","dashed",PURPLE),edge("t9","agents","tools"),edge("t10","gpu","monitor"),edge("t11","tools","monitor") ])),
    ]


def module_gallery(output_dir: Path):
    selected=[item["id"] for item in MODULES]
    lookup={item["id"]:item for item in MODULES}; w,h=1600,1490
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="#FFFFFF"/><text x="800" y="55" text-anchor="middle" font-family="Arial" font-size="34" font-weight="700" fill="{INK}">Hot-Topic CS &amp; AI Editable Module Library</text>']
    image=Image.new("RGB",(w,h),"white"); draw=ImageDraw.Draw(image); draw_text(draw,(100,12,1400,55),"Hot-Topic CS & AI Editable Module Library",32,True)
    for i,module_id in enumerate(selected):
        item=lookup[module_id]; col=i%5; row=i//5; x=30+col*310; y=90+row*195; fill,stroke=PALETTES[item["family"]]
        svg.append(f'<g id="catalog-{item["id"]}"><rect x="{x}" y="{y}" width="285" height="165" rx="18" fill="{fill}" stroke="{stroke}" stroke-width="2"/>{icon_svg(item["icon"],x+72,y+8,140,92)}<text x="{x+142.5}" y="{y+126}" text-anchor="middle" font-family="Arial" font-size="17" font-weight="700" fill="{INK}">{esc(item["name"])}</text><text x="{x+142.5}" y="{y+149}" text-anchor="middle" font-family="Arial" font-size="11" fill="#5E7183">{esc(item["primitive"])}</text></g>')
        draw.rounded_rectangle((x,y,x+285,y+165),radius=18,fill=fill,outline=stroke,width=3); draw_icon(draw,item["icon"],(x+72,y+8,140,92)); draw_text(draw,(x+14,y+112,257,28),item["name"],16,True); draw_text(draw,(x+14,y+140,257,18),item["primitive"],10,False,"#5E7183")
    svg.append('</svg>'); (output_dir/"hot-topic-module-library.svg").write_text("\n".join(svg),encoding="utf-8"); image.save(output_dir/"hot-topic-module-library.png")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--examples-dir", default=str(WORKSPACE/"examples"/"imitation"))
    parser.add_argument("--gallery-dir", default=str(WORKSPACE/"examples"/"module-library"))
    args=parser.parse_args()
    icons=SKILL/"assets"/"module-icons"; icons.mkdir(parents=True,exist_ok=True)
    catalog=[]
    for item in MODULES:
        filename=f'{item["id"]}.svg'; write_icon(icons/filename,item); catalog.append({**item,"asset":f"module-icons/{filename}"})
    (SKILL/"assets"/"module-catalog.json").write_text(json.dumps({"schema_version":"1.0","families":list(PALETTES),"modules":catalog},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    examples_dir=Path(args.examples_dir); examples_dir.mkdir(parents=True,exist_ok=True)
    for slug,reference,target in examples():
        folder=examples_dir/slug; folder.mkdir(parents=True,exist_ok=True)
        for name,spec in (("reference-structure",reference),("target-redraw",target)):
            (folder/f"{name}-spec.json").write_text(json.dumps(spec,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
            render_scene_svg(spec,folder/f"{name}.svg"); render_scene_png(spec,folder/f"{name}.png")
        comparison(folder/"reference-structure.png",folder/"target-redraw.png",folder/"comparison.png")
    gallery=Path(args.gallery_dir); gallery.mkdir(parents=True,exist_ok=True); module_gallery(gallery)
    print(f"Wrote {len(MODULES)} module entries and {len(examples())} imitation examples")


if __name__ == "__main__":
    main()
