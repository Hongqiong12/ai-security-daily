#!/usr/bin/env python3
"""2026-11-24 门面同步（幂等）：写入本轮 6 篇 + 修复 11-23 遗留的 t2i-survey 更新注记。

覆盖：selected_papers.json / _meta.json / README（徽章+今日区块+洞察表+三模态索引）/
两份 Survey（头部+表格行+更新注记）/ Landscape（v3.19 + 热点三十一）/
两份 benchmark README（t2i 50→52 / t2t 29→31）。

重复执行不会产生重复行：每处按唯一 ID 或唯一串做存在性检查。
"""
import json, re, os

ROOT = "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
os.chdir(ROOT)

TODAY = "2026-11-24"
COUNTS = {"t2t": 134, "t2i": 160, "agentic": 40, "total": 334}
MISSING = ["2026-11-%02d" % d for d in range(11, 23)]
IDS = ["2611.27339", "2611.27905", "2611.20623", "2611.27229",
       "2611.27155", "2611.26881"]


def rd(p):
    return open(p, encoding="utf-8").read()


def wr(p, s):
    open(p, "w", encoding="utf-8").write(s)


def rows_after(s, prefix, rows, marker):
    """把 rows 插到以 prefix 开头的那一行之后，保持 Markdown 表格连续。"""
    if marker in s:
        return s
    out, done = [], False
    for ln in s.split("\n"):
        out.append(ln)
        if not done and ln.startswith(prefix):
            out.extend(rows)
            done = True
    if not done:
        raise RuntimeError("anchor not found: " + prefix[:60])
    return "\n".join(out)


def prepend_to_bullet(s, start, disc, payload):
    """在「以 start 开头且含 disc」的那条索引 bullet 内容开头插入新链接。

    start 用稳定的表头前缀、disc 用原首个链接名，这样插入后前缀仍可匹配 → 幂等。
    """
    out, done = [], False
    for ln in s.split("\n"):
        if not done and ln.startswith(start) and disc in ln:
            # 表头形如 "- **Defense (安全加固):** " —— 加粗闭合 ** 后才跟空格
            head, sep, rest = ln.partition("** ")
            if not sep:
                head, sep, rest = ln.partition(": ")
            if not sep:
                raise RuntimeError("bad bullet: " + start)
            ln = head + sep + payload + " | " + rest
            done = True
        out.append(ln)
    if not done:
        raise RuntimeError("bullet not found: " + start + " / " + disc)
    return "\n".join(out)


# ---------- 1. selected_papers.json 102 → 108 ----------
sel = json.load(open("selected_papers.json", encoding="utf-8"))
have = {x["id"].split("v")[0] for x in sel}
pool = json.load(open("/tmp/full_1124.json", encoding="utf-8"))
byid = {x["id"].split("v")[0]: x for x in pool}
added = []
for aid in IDS:
    if aid in have:
        continue
    x = byid.get(aid, {})
    title = re.sub(r"^(?:Title|Abstract):\s*", "", x.get("title", "")).strip()
    abstract = re.sub(r"^(?:Title|Abstract):\s*", "", x.get("abstract", "")).strip()
    sel.append({"id": aid + "v1", "title": title, "summary": abstract,
                "published": x.get("published", TODAY), "selected_date": TODAY})
    added.append(aid)
wr("selected_papers.json", json.dumps(sel, ensure_ascii=False, indent=1) + "\n")
print("selected_papers:", len(sel), "| added:", added)

# ---------- 2. _meta.json ----------
meta = {
    "_meta_version": "1.0",
    "last_updated": TODAY,
    "paper_counts": COUNTS,
    "survey_versions": {
        "t2t-survey": {"date": TODAY, "count": 134},
        "t2i-survey": {"date": TODAY, "count": 160},
        "agentic-search-survey": {"date": "2026-10-30", "version": "v1.9", "count": 40},
        "landscape_2026": {"date": TODAY, "version": "v3.19", "total_papers": 334},
    },
    "benchmark_status": {
        "t2t_benchmark": {"entries": 31, "last_updated": TODAY},
        "t2i_benchmark": {"entries": 52, "last_updated": TODAY},
        "agentic_benchmark": {"entries": 10, "last_updated": "2026-04-30"},
    },
    "daily_reports": {
        "latest": TODAY,
        "this_month_count": 10,
        "missing_dates": MISSING,
    },
    "workflow_version": "2.3",
    "today_selection": {
        "t2i": ["2611.27339_unimodal_shortcuts_scene_intent",
                "2611.27905_animalfarm_hateful_image_audit",
                "2611.20623_ebsg_example_based_spatial_guidance",
                "2611.27229_p2e_supervision_redundancy"],
        "t2t_migration": ["2611.27155_vulnerability_window_quantized_judges",
                          "2611.26881_judge_inherits_prompt_directional_bias"],
        "theme": "分数没动，判定全换了 —— 代理量与目标量的六次脱钩",
    },
    "_note": "This file is the single source of truth for all paper counts. Automation must update this file on every run. Never estimate counts — always use search_file to scan papers/ directories.",
}
wr("_meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
print("_meta.json: 334 / month_count 10 / missing_dates", len(MISSING))

# ---------- 3. README ----------
r = rd("README.md")
r = r.replace("Papers-328-green.svg", "Papers-334-green.svg")
r = r.replace("Last-Update-2026--11--23-orange.svg", "Last-Update-2026--11--24-orange.svg")
r = r.replace("基于 **328** 篇安全论文萃取的全局视野", "基于 **334** 篇安全论文萃取的全局视野")

TODAY_BLOCK = """## 🔥 今日最具业务价值论文评测 (2026-11-24)

> **今天六篇没有一篇在说"分数不够高"。它们在说：被当成达标读数的那个量，往往只是真正风险的代理，而且脱钩是单方向的——所以分数没动，判定已经全换了。**
>
> **✅ 供给侧**：网页端十分类 `/list/<cat>/recent?show=2000` 串行全批扫描（避开导出 API 的 IP 级 429），公告批次 **11-17→11-23 五个批次**，其中 **11-23 为新增 565 篇**；全批池 **3991 篇**（1739 篇带摘要），主题词 **18 路** + 方法论形态 **12 路**全部在本地池正则复现、零额外检索请求。本轮为**供给回暖轮**。
>
> **⚠️ 空窗第 十七 周，口径写得更窄**：`t2_prompt_rewrite` 严格 **0**（输入侧安全改写法仍零供给）；但 `t3_i2i_edit_safety` 1、`t6_concept_erasure`/`t18_generated_risk` 20/28、`t10_video_safety` **1**（视频扩展本轮有强相关工作）⇒ 出图侧干预 / 图审 / 图文联合判定 / 量化不劣化**四条相邻带同时有强供给**。`t14_policy_guard` 5 命中逐篇核验 **0 可迁移**（全是 RAG 混合检索），"有量不等于有供给"第四次生效。
>
> **🎯 本轮最扎的一个数**：AnimalFarm —— 源场景经**两名标注员独立接受**的保守人工筛查（输入侧已相当干净），生成系统仍对 **92.1%** 的计划查询出图、其中 **95.9%** 含仇恨，而最强图审只认出 **73.9%**。⇒ **改写后文本无害 ≠ 出图侧无害**，与本项目 3,000 条 case 中 2,700+ 条源于出图侧内生风险同构。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **不看图的探针拿了 0.9645 AUROC** | [Unimodal Shortcuts](./categories/t2i/papers/2611.27339_unimodal_shortcuts_scene_intent.md) | **港科大 + 深大 + XGEN Labs + 港科广 + 清华**。五个情境安全 benchmark 的标签都能由单模态预测：灰图纯文本探针 **0.9645–0.9846 AUROC**，而四路控制把单模态上界压到 **0.500**；中间层 joint probe **0.958/0.930**，跨 benchmark 只 **0.48–0.67**。缓存探针 **0.234 ms** vs 独立安全 pass **95.82 ms**、prefill 仅 **+0.36%**。⇒ 连验收用的公开 benchmark 都不要求读图，I2I 0/0% 拿到第五种归因。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **输入干净，出图照样 95.9% 带仇恨** | [AnimalFarm](./categories/t2i/papers/2611.27905_animalfarm_hateful_image_audit.md) | **CISPA Helmholtz + Independent + HPE**。14,250 queries / 12,900 attempts，**92.1% 出图 / 95.9% 仇恨**；三通路 GPT Image 2 **66.6/68.0/75.3**，最强 GPT-5.5 图审 recall 仅 **73.9%**、LlavaGuard **28.0**；Prompt Enhancement 使 LlavaGuard **28.8→64.4**；SFT+GRPO 检测器 F1 **0.962/0.979**，奖励 **0.7/0.1/0.1/0.1**；`1−G/Q` 是 non-generation、**不等于拒答率**；LABUBU 未见仍 **96.6%**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **二值安全评测会放过"塌成噪声"** | [EBSG](./categories/t2i/papers/2611.20623_ebsg_example_based_spatial_guidance.md) | **KAIST（NeurIPS 2026 poster）**。细粒度子概念 + 空间局部引导，training-free、不改输入不改权重：VLM rubric 与人工一致 **82.6%**；SR **97.2/96.2/84.2/97.4** 而 NR 仅 **1.4/1.3/0.4/0.0**；FID **6.31 vs 7.83**、CLIP **0.263 vs 0.259**；新增 `NOTRELEVANT` 档。⇒ 出图侧生成过程干预第一次有了可执行的第三条通路。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **生成增益差 25 倍，改写器只差 0.14 分** | [P2E / Prune to Expand](./categories/t2i/papers/2611.27229_p2e_supervision_redundancy.md) | **港城大 + 港中深**。`D_H` 增益 **3.20** vs `D_M` **0.13**（约 25×），同配置训出的 PE 却只差 **+0.14 HPS v2 / +0.05 PicS / +0.002 MIQA / +0.000 VQ-R1**；无约束剪枝 **27.27→26.46**，视觉守护剪枝反升 **27.59**；K=3 / τ=0.4 / 800 prompts / 4 generators / Qwen3.5-9B。⇒ "按生成增益选 SFT 监督目标"被配对证伪。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **准确率只动 0.03 点，判定换了 1.1–12.3%** | [The Vulnerability Window](./categories/t2t/papers/2611.27155_vulnerability_window_quantized_judges.md) | **Illinois Institute of Technology + UW–Milwaukee**。4-bit 量化下 **1.1–12.3%** 成对判定翻转而聚合准确率只动 **0.03 点**；NF4 Llama-3.2-1B **3.99%**；harmful:helpful 翻转 **146:54**；脆弱窗口随规模 **25%→7%**；best-of-64 选中项变 **14.6–65.7%** 而最终答案只 **2.6–9.6%**（**5–8×**）。⇒ fp8/fp4 上线必须做「逐对翻转」四栏不劣化验收。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |
| **judge 的偏置是单向的** | [Your Judge Inherits Your Prompt](./categories/t2t/papers/2611.26881_judge_inherits_prompt_directional_bias.md) | **University of Essex + Independent（BlackboxNLP 2026 Workshop）**。只改 judge 的 Yes/No few-shot 标签平衡、其余全冻结：偏向接受在 NExT-QA S3 虚高 **+29.5 点**、FP:FN **9.4**，MSVD-QA **+19.5**、FP:FN **4.0**；偏向拒绝/balanced 只在 **±2.5** 内 ⇒ **inflation-only asymmetry**；单次抽样波动达 **18 点**；每数据集 **200 例人工共识**。⇒ 图审 AB 看板必须冻结 judge 配置指纹。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-24_AI安全每日深度情报.md) |

⏱ **今日一句话**：**别再往输入侧加码了**。先把「灰图探针验收、三通路对照、出图侧生成过程干预、逐对翻转 + judge 尺子四栏不劣化」补进验收，把 2,700+ 条 case 从"改写还不够严"改写为"风险长在出图侧"；否则 0/0% 会继续被写成"改写没写好"。
"""
start = r.find("## 🔥 今日最具业务价值论文评测 (")
end = r.find("\n---\n\n## 🔭 前沿 Survey", start)
if start != -1 and end != -1:
    r = r[:start] + TODAY_BLOCK + r[end:]

# 洞察状态表三行
insight = {
    "| 🏆": "| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **分数没动，判定全换了（热点三十一）**（NEW） · **灰图探针 0.9645 AUROC**（NEW） · **出图 92.1% / 仇恨 95.9% 而图审 recall 73.9%**（NEW） · **量化后 1.1–12.3% 成对翻转**（NEW） | 2026-11-24 |",
    "| 🛡️": "| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **聚合准确率只动 0.03 点而 1.1–12.3% 成对判定被 4-bit 重写**（NEW） · **judge 偏置单向：接受侧虚高 +29.5 点、拒绝侧不下降**（NEW） · **量化/加速安全率不劣化四栏验收**（NEW） | 2026-11-24 |",
    "| 🖼️": "| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **五个情境安全 benchmark 都有单模态捷径**（NEW） · **AnimalFarm：三通路输入干净而出图侧内生风险**（NEW） · **EBSG：不改输入/权重的子概念空间引导**（NEW） · **P2E：SFT 监督冗余使生成增益与改写器脱钩 25×**（NEW） | 2026-11-24 |",
}
lines = r.split("\n")
for i, ln in enumerate(lines):
    for k, v in insight.items():
        if ln.startswith(k):
            lines[i] = v
            break
r = "\n".join(lines)

# 三模态论文索引：把本轮 6 篇挂到对应 bullet 的最前面
IDX = [
    ("- **Defense (安全加固):**", "Tripwire-WM",
     "[EBSG 子概念空间引导](./categories/t2i/papers/2611.20623_ebsg_example_based_spatial_guidance.md) (SR 97.2/96.2/84.2/97.4 而 NR ≤1.4 / FID 6.31 vs 7.83) | "
     "[P2E 冗余监督](./categories/t2i/papers/2611.27229_p2e_supervision_redundancy.md) (生成增益 25× 而改写器只差 +0.14 HPS v2)",
     "2611.20623"),
    ("- **Benchmark:**", "EditSafetyBench",
     "[Unimodal Shortcuts](./categories/t2i/papers/2611.27339_unimodal_shortcuts_scene_intent.md) (灰图纯文本探针 0.9645–0.9846 AUROC / 四路控制上界 0.500) | "
     "[AnimalFarm](./categories/t2i/papers/2611.27905_animalfarm_hateful_image_audit.md) (92.1% 出图 / 95.9% 仇恨 / 最强图审 recall 73.9%)",
     "2611.27339"),
    ("- **Benchmark:**", "Operating-Point Failure",
     "[The Vulnerability Window](./categories/t2t/papers/2611.27155_vulnerability_window_quantized_judges.md) (1.1–12.3% 成对翻转 / 聚合准确率只动 0.03 点) | "
     "[Your Judge Inherits Your Prompt](./categories/t2t/papers/2611.26881_judge_inherits_prompt_directional_bias.md) (接受偏置虚高 +29.5 点，拒绝侧不对称)",
     "2611.27155"),
]
for start, disc, payload, marker in IDX:
    hit = [ln for ln in r.split("\n") if ln.startswith(start) and disc in ln]
    if hit and marker in hit[0]:
        continue  # 幂等：该 bullet 已挂过本轮链接
    r = prepend_to_bullet(r, start, disc, payload)

wr("README.md", r)
print("README: badge 334 / date 11-24 / 今日区块 / 洞察表 / 索引 6 篇")

# ---------- 4. t2i-survey ----------
s = rd("insights/t2i-survey.md")
s = s.replace("本项目收录的 **156** 篇 T2I 安全论文", "本项目收录的 **160** 篇 T2I 安全论文")
s = s.replace("**更新日期**: 2026-11-23", "**更新日期**: 2026-11-24")
t2i_rows = [
 " | **Unimodal Shortcuts / Joint Scene-Intent Dependence** | [2611.27339](https://arxiv.org/abs/2611.27339) | 2026 (**港科大 + 深大 + XGEN Labs + 港科广 + 清华**) | **验收集本身允许不看图**：风险是 scene × intent 的合取，需 I(Y;I|U)>0 且 I(Y;U|I)>0 才测得到联合态；五个情境安全 benchmark 上灰图纯文本探针 **0.9645–0.9846 AUROC**，四路控制把单模态上界压到 **0.500**；中间层 joint probe **0.958/0.930**、concat separately encoded states **0.930/0.859**、跨 benchmark 只有 **0.48–0.67**；缓存探针 **0.234 ms** vs 独立安全 pass **95.82 ms**、prefill **+0.36%**。⇒ 改写后「文本无害」不能推出「图文联合状态安全」，I2I 0/0% 第五种归因 (NEW) |",
 " | **AnimalFarm** | [2611.27905](https://arxiv.org/abs/2611.27905) | 2026 (**CISPA Helmholtz + Independent + HPE**) | **输入干净、出图侧照样内生风险**：14,250 queries / 12,900 attempts，两名标注员独立接受才保留；**92.1% 出图、其中 95.9% 含仇恨**；三通路（T2I / 图像编辑 / 多轮会话）GPT Image 2 **66.6/68.0/75.3**；最强 GPT-5.5 图审 recall **73.9%**、LlavaGuard **28.0**，Prompt Enhancement 使 LlavaGuard **28.8→64.4**；SFT+GRPO 检测器 F1 **0.962/0.979**，奖励正确性/格式/checklist/群体 **0.7/0.1/0.1/0.1**；`1−G/Q` 为 non-generation **≠ 拒答率**；未见过的 LABUBU 仍 **96.6%** (NEW) |",
 " | **EBSG / Example-Based Spatial Guidance** | [2611.20623](https://arxiv.org/abs/2611.20623) | 2026 (**KAIST**, NeurIPS 2026 poster) | **二值安全分是语义完整性的坏代理**：一个塌成无信息噪声、没人物也没内容的模型能通过 NudeNet/Q16（model collapse bypass safety checks）。把宽泛负向概念拆成**细粒度子概念 + 空间局部引导**，training-free、不改输入不改权重；VLM rubric 与人工一致 **82.6%**、新增 `NOTRELEVANT` 档；SR **97.2/96.2/84.2/97.4** 而 NR **1.4/1.3/0.4/0.0**，FID **6.31 vs 7.83**、CLIP **0.263 vs 0.259**；h/τ/βtxt/βimg 按概念配置 ⇒ 第三条降风险通路 (NEW) |",
 " | **P2E / Prune to Expand** | [2611.27229](https://arxiv.org/abs/2611.27229) | 2026 (**港城大 + 港中深**) | **「生成变好的 caption 就是好监督目标」被配对证伪**：按 Δq 取最高/最低各 10K 得 `D_H` **3.20** vs `D_M` **0.13**（**25×**），同初始化同配置训出的 Prompt Enhancer 在 200 条留出短 prompt 上只差 **+0.14 HPS v2 / +0.05 PicS / +0.002 MIQA / +0.000 VQ-R1**；dense caption 里大量图像专属细节与用户意图弱相关 = **冗余监督**；无约束剪枝 **27.27→26.46**，视觉守护剪枝 **→27.59**；K=3 / τ=0.4 / 800 prompts / 4 generators / Qwen3.5-9B (NEW) |",
]
# 每行开头去掉多余空格（保持表格语法）
t2i_rows = [x.lstrip() for x in t2i_rows]
s = rows_after(s, "| **Tripwire-WM / Reject and Report**", t2i_rows, "2611.27339")
note24 = "*本次 Survey 更新：2026-11-24（新增 4 篇：2611.27339 五个情境安全 benchmark 的单模态捷径与 0.9645 AUROC 灰图探针、2611.27905 AnimalFarm 三通路出图侧内生风险 92.1%/95.9%/73.9%、2611.20623 EBSG 子概念+空间局部引导与二值评测塌缩、2611.27229 P2E 冗余监督使生成增益与改写器脱钩 25×；现为 **160** 篇）。*"
if "本次 Survey 更新：2026-11-24" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-10（新增 4 篇：2611.09304",
                  note24 + "\n*历史 Survey 更新：2026-11-10（新增 4 篇：2611.09304", 1)
wr("insights/t2i-survey.md", s)
print("t2i-survey: 160 / +4 rows / 更新注记")

# ---------- 5. t2t-survey ----------
s = rd("insights/t2t-survey.md")
s = s.replace("本项目收录的 **132** 篇 T2T 安全论文", "本项目收录的 **134** 篇 T2T 安全论文")
s = s.replace("**更新日期**: 2026-11-23", "**更新日期**: 2026-11-24")
t2t_rows = [
 "| **The Vulnerability Window** | [2611.27155](https://arxiv.org/abs/2611.27155) | 2026 (**Illinois Institute of Technology + UW–Milwaukee**) | 量化后判定漂移 / 推理加速不劣化 / 成对验收 | **聚合准确率几乎没动是最接近盲的检查**：4-bit 量化同时修掉和引入错误、聚合互相抵消，于是 **1.1–12.3%** 成对判定翻转而 aggregate accuracy 只动 **0.03 点**；Llama-3.2-1B/NF4 **3.99%**；harmful:helpful 翻转 **146:54**；脆弱窗口随规模 **25%→7%**（小模型 judge 风险显著更高）；best-of-64 选中项变 **14.6–65.7%** 而最终答案只 **2.6–9.6%**（**5–8×**）、top-k 仅 **+0.35** ⇒ fp8/fp4 与跨硬件迁移必须做逐对翻转四栏验收 (NEW) |",
 "| **Your Judge Inherits Your Prompt** | [2611.26881](https://arxiv.org/abs/2611.26881) | 2026 (**Independent Researcher + University of Essex**, BlackboxNLP 2026 Workshop) | LLM-as-judge 偏差 / VLM 图审 AB / 评测装置冻结 | **偏置是单向的**：generator–judge 全冻结、只改 Yes/No few-shot 标签平衡，偏向接受在 NExT-QA S3 虚高 **+29.5 点**（FP:FN **9.4**）、MSVD-QA **+19.5**（**4.0**），而 balanced / refusal-skew 都在 **±2.5** 内 ⇒ **inflation-only asymmetry**；单次示例抽样波动达 **18 点**、超过任意两套演示集之间的差异；每数据集 **200 例人工共识** ⇒ AB 看板必须冻结「judge 配置指纹」并多次抽样 (NEW) |",
]
s = rows_after(s, "| **Risk-certified Prompt Optimization**", t2t_rows, "2611.27155")
note24t = "*本次 Survey 更新：2026-11-24（新增 2 篇方法论迁移：2611.27155 量化后 1.1–12.3% 成对判定翻转而聚合准确率只动 0.03 点、2611.26881 judge 的 in-context 标签偏置只会单向抬高分数；现为 **134** 篇）。*"
if "本次 Survey 更新：2026-11-24" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-23（新增 2 篇",
                  note24t + "\n*上次 Survey 更新：2026-11-23（新增 2 篇", 1)
wr("insights/t2t-survey.md", s)
print("t2t-survey: 134 / +2 rows / 更新注记")

# ---------- 6. benchmark README ----------
b = rd("categories/t2i/benchmark/README.md")
b = b.replace("最后回填: 2026-11-23 | 共 **50** 条", "最后回填: 2026-11-24 | 共 **52** 条")
newrows = [
 "| **Unimodal Shortcuts（五个情境安全 benchmark 诊断）** | [2611.27339](https://arxiv.org/abs/2611.27339) | 2026 arXiv（**港科大 + 深大 + XGEN Labs + 港科广 + 清华**） | **benchmark 标签能由单模态预测**：灰图纯文本探针 **0.9645–0.9846 AUROC** vs 四路控制上界 **0.500**；提出需 I(Y;I|U)>0 且 I(Y;U|I)>0 才能验收图文联合态；跨 benchmark 泛化只有 **0.48–0.67** (NEW) |",
 "| **AnimalFarm（仇恨图像生成-检测审计）** | [2611.27905](https://arxiv.org/abs/2611.27905) | 2026 arXiv（**CISPA + Independent + HPE**） | **14,250 queries / 三通路**：92.1% 出图、95.9% 带仇恨而最强图审 recall 仅 **73.9%**；主体非人时检测器系统性失明；`non-generation ≠ refusal rate` 口径纪律 (NEW) |",
]
tail = "\n[← 返回文生图目录](../README.md)"
if "2611.27339" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2i/benchmark/README.md", b)

b = rd("categories/t2t/benchmark/README.md")
b = b.replace("最后回填: 2026-11-23 | 共 **29** 条", "最后回填: 2026-11-24 | 共 **31** 条")
newrows = [
 "| **The Vulnerability Window（量化判定漂移评测）** | [2611.27155](https://arxiv.org/abs/2611.27155) | 2026 arXiv（**IIT + UW–Milwaukee**） | **聚合准确率 0.03 点 vs 1.1–12.3% 成对翻转**：量化误差双向抵消使聚合指标失明，需逐对翻转 + 分层 F1 + 安全率不劣化四栏验收 (NEW) |",
 "| **Your Judge Inherits Your Prompt（judge 偏置审计）** | [2611.26881](https://arxiv.org/abs/2611.26881) | 2026 arXiv（**Essex + Independent**, BlackboxNLP 2026） | **只改 few-shot 标签平衡即虚高 29.5 点**且偏置单向；单次抽样波动 18 点；每数据集 200 例人工共识 ⇒ judge 配置指纹 + 多次抽样 (NEW) |",
]
tail = "\n[← 返回文生文目录](../README.md)"
if "2611.27155" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2t/benchmark/README.md", b)
print("benchmark: t2i 52 / t2t 31")

# ---------- 7. Landscape ----------
L = rd("insights/AI_Security_Landscape_2026.md")
L = L.replace("基于本项目收录的 **328 篇**", "基于本项目收录的 **334 篇**")
L = L.replace("**更新日期**: 2026-11-23（v3.18 增量更新）", "**更新日期**: 2026-11-24（v3.19 增量更新）")
L = L.replace("### T2T 论文分布（132 篇）", "### T2T 论文分布（134 篇）")
L = L.replace("### T2I 论文分布（156 篇）", "### T2I 论文分布（160 篇）")
L = L.replace(
    "*最近更新：2026-11-23（v3.18 增量更新），累计论文数 **328**（T2T: **132** 篇，T2I: **156** 篇，Agentic Search: **40** 篇）。*",
    "*最近更新：2026-11-24（v3.19 增量更新），累计论文数 **334**（T2T: **134** 篇，T2I: **160** 篇，Agentic Search: **40** 篇）。*")

hot31 = """### 🔥 热点三十一：分数没动，判定全换了 —— 代理量与目标量的六次脱钩（2026-11-24 新增）

热点三十说"部件合格，不等于组合安全"。这一轮六篇再往下一层：**被当成达标读数的那个量，往往只是真正风险的代理**；更关键的是，**脱钩是单方向的**——代理量稳住甚至变好，目标量已经整体换了一边，所以只盯代理量永远发现不了。

| 被当成的达标读数（代理量） | 真正要守的量（目标量） | 实测脱钩 |
|---|---|---|
| 情境安全 benchmark 高 AUROC | 模型是否编码了 scene × intent 联合态 | 灰图**纯文本**探针 **0.9645–0.9846 AUROC**，四路控制上界 **0.500** |
| 输入侧文本已被判无害 | 出图侧是否内生风险 | **92.1% 出图 / 95.9% 带仇恨**，而最强图审 recall 仅 **73.9%** |
| 二值安全检测"通过" | 图是否还有语义完整性 | 塌成无信息噪声的模型技术上能**通过**检查（model collapse bypass） |
| SFT 监督目标的生成增益 | 改写器下游实际质量 | `D_H` 3.20 vs `D_M` 0.13（**25×**）而下游只差 **+0.14 HPS v2** |
| 量化后聚合准确率 | 具体哪一对判定/哪个候选被选中 | 聚合只动 **0.03 点**，成对翻转 **1.1–12.3%**；selection 变 **5–8×** 于 answer |
| judge 的 Yes/No 准确率 | judge 是否对齐人工共识 | 偏向接受虚高 **+29.5 点**、偏向拒绝不下降 ⇒ **inflation-only asymmetry** |

**由此提炼三条新纪律**：① **任何聚合指标上线前，必须配一个"逐单元"的对照量**（单模态控制上界 / 三通路对照 / 二值之外的语义完整性 / 逐对翻转 / 人工共识），否则聚合里的正负抵消会把整套判定换掉而不留痕；② **验收装置本身要先被验收**——benchmark 有没有单模态捷径、judge 的示例标签平衡有没有冻结，都会让版本间比的是装置而不是模型；③ **归因方向比归因数值重要**：3,000 条改写后仍被打击的 case 里 2,700+ 条改写后文本无害 ⇒ 重心应从"加严输入改写"移到**出图侧生成过程干预**与输出侧图审，而不是继续在入口加码。

**权重侧/输入侧边界第十一轮**：本轮给出**四层降风险通路的互补形状**——输入侧热更新改写（P2E 证明其 SFT 监督目标需按"意图相关"而非"生成增益"筛选）、权重侧概念擦除（仍为互补非替代）、**不改输入不改权重的生成过程干预**（EBSG 的子概念 + 空间局部引导，SR 97.2/96.2/84.2/97.4 而 NR ≤1.4、FID 6.31 vs 7.83）、输出侧图审与溯源（AnimalFarm 证明主体非人时检测器系统性失明）。新结论：**输入改写的有效性上界不是训练问题，是责任边界问题**——它只能对"文本无害"负责，不能对"出图无害"负责。

"""
if "热点三十一" not in L:
    L = L.replace("### 🔥 热点三十：", hot31 + "### 🔥 热点三十：", 1)

v319 = """*本次 v3.19 更新：新增 4 篇 T2I/T+I2I 论文（Unimodal Shortcuts：五个情境安全 benchmark 都有单模态捷径，灰图纯文本探针 0.9645–0.9846 AUROC 而四路控制上界 0.500，缓存探针 0.234 ms vs 独立安全 pass 95.82 ms；AnimalFarm：14,250 queries / 三通路，输入侧经双人保守筛查后仍 92.1% 出图、95.9% 带仇恨，最强图审 recall 73.9%、LlavaGuard 28.0，Prompt Enhancement 使其 28.8→64.4，SFT+GRPO 奖励 0.7/0.1/0.1/0.1，`non-generation ≠ refusal rate`；EBSG：细粒度子概念 + 空间局部引导，VLM rubric 人工一致 82.6%、SR 97.2/96.2/84.2/97.4 而 NR ≤1.4、FID 6.31 vs 7.83；P2E：生成增益 25× 而改写器只差 +0.14 HPS v2，视觉守护剪枝 27.27→27.59）与 2 篇方法论迁移（Vulnerability Window：4-bit 下 1.1–12.3% 成对翻转而聚合准确率只动 0.03 点、脆弱窗口 25%→7%、selection 变 5–8× 于 answer；Your Judge Inherits Your Prompt：in-context 标签偏置单向抬高 +29.5 点、单次抽样波动 18 点），并新增一条范式信号（热点三十一）：**分数没动，判定全换了**。供给侧为**供给回暖轮**：网页端十分类串行全批 **3991 篇**（1739 篇带摘要），公告批次 11-17→11-23 其中 **11-23 新增 565 篇**；主题词 **18 路** + 形态 **12 路**全部本地正则复现、零额外检索请求；`t2_prompt_rewrite` 严格 **0**（输入侧安全改写法空窗第 **17** 周），但出图侧干预 / 图审 / 图文联合判定 / 量化不劣化**四条相邻带同时有强供给**，`t10_video_safety` 本轮 **1** 命中（与上一轮 0 不同）；`t14_policy_guard` 5 命中全为 RAG 混合检索、逐篇核验 **0 可迁移**（"有量不等于有供给"第四次生效）。权重侧/输入侧边界第十一轮把四层降风险通路补齐，并明确**输入改写的有效性上界是责任边界问题而非训练问题**。机构核验 8/8 HTTP 200、HTML affiliation 全空由 PDF 首页 pypdf 回退（第 11 次连续生效）；**头部公司 0 篇**，如实标注。*
"""
if "v3.19 更新" not in L:
    L = L.replace("*本次 v3.18 更新：", v319 + "*本次 v3.18 更新：", 1)
wr("insights/AI_Security_Landscape_2026.md", L)
print("Landscape: v3.19 / 334 / 热点三十一")
