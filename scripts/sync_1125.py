#!/usr/bin/env python3
"""2026-11-25 门面同步（幂等）：写入本轮 6 篇 + 刷新全部计数锚点。

覆盖：selected_papers.json / _meta.json / README（徽章+今日区块+洞察表+三模态索引）/
两份 Survey（头部+表格行+更新注记）/ 两份 benchmark README（t2i 52→54 / t2t 31→33）/
Landscape（v3.20 + 热点三十二）。

重复执行不会产生重复行：每处按唯一 ID 或唯一串做存在性检查。
"""
import json, re, os

ROOT = "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
os.chdir(ROOT)

TODAY = "2026-11-25"
COUNTS = {"t2t": 136, "t2i": 164, "agentic": 40, "total": 340}
MISSING = ["2026-11-%02d" % d for d in range(11, 23)]
IDS = ["2611.25382", "2611.30545", "2611.30117", "2611.30592",
       "2611.23685", "2611.29629"]


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
    out, done = [], False
    for ln in s.split("\n"):
        if not done and ln.startswith(start) and disc in ln:
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


# ---------- 1. selected_papers.json 108 → 114 ----------
sel = json.load(open("selected_papers.json", encoding="utf-8"))
have = {x["id"].split("v")[0] for x in sel}
pool = json.load(open("/tmp/full_1125.json", encoding="utf-8"))
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
        "t2t-survey": {"date": TODAY, "count": 136},
        "t2i-survey": {"date": TODAY, "count": 164},
        "agentic-search-survey": {"date": "2026-10-30", "version": "v1.9", "count": 40},
        "landscape_2026": {"date": TODAY, "version": "v3.20", "total_papers": 340},
    },
    "benchmark_status": {
        "t2t_benchmark": {"entries": 33, "last_updated": TODAY},
        "t2i_benchmark": {"entries": 54, "last_updated": TODAY},
        "agentic_benchmark": {"entries": 10, "last_updated": "2026-04-30"},
    },
    "daily_reports": {
        "latest": TODAY,
        "this_month_count": 11,
        "missing_dates": MISSING,
    },
    "workflow_version": "2.3",
    "today_selection": {
        "t2i": ["2611.25382_silent_text_rewrite_guidance_cache",
                "2611.30545_batch_dependent_nondeterminism_t2i",
                "2611.30117_sae_audit_concept_erasure_residue",
                "2611.30592_hose_hierarchical_orthogonal_erasure"],
        "t2t_migration": ["2611.23685_latent_safety_filter_conservatism",
                          "2611.29629_operating_point_contamination"],
        "theme": "钉死了输入，也钉不住出图 —— 输入改写够不到的四层：生成过程、执行环境、权重残留、验收装置",
    },
    "_note": "This file is the single source of truth for all paper counts. Automation must update this file on every run. Never estimate counts — always use search_file to scan papers/ directories.",
}
wr("_meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
print("_meta.json: 340 / month_count 11 / missing_dates", len(MISSING))

# ---------- 3. README ----------
r = rd("README.md")
r = r.replace("Papers-334-green.svg", "Papers-340-green.svg")
r = r.replace("Last-Update-2026--11--24-orange.svg", "Last-Update-2026--11--25-orange.svg")
r = r.replace("基于 **334** 篇安全论文萃取的全局视野", "基于 **340** 篇安全论文萃取的全局视野")

TODAY_BLOCK = """## 🔥 今日最具业务价值论文评测 (2026-11-25)

> **今天六篇把「出图侧内生风险」从一个现象拆成四条可分别检验的机制：生成过程、执行环境、权重残留、验收装置。每一层都独立削掉一次输入改写的有效性上界。**
>
> **✅ 供给侧**：网页端十分类 `/list/<cat>/recent?show=2000` 串行全批扫描，公告批次 **11-18→11-24**，其中 **11-24 单批新增 1442 篇**；全批池 **4139 篇**（1871 篇带摘要），复用昨日 1739 条摘要缓存只新抓 **688** 篇，主题词 **18 路** + 形态 **12 路**全部本地正则复现、零第二次检索请求。本轮为**供给回暖第二轮**。
>
> **⚠️ 空窗第 十八 周，口径按层写窄**：`t2_prompt_rewrite` 严格 **0**；`t3_i2i_edit_safety` 1 命中是**已收录**的 AnimalFarm ⇒ I2I 编辑改写仍零供给；`t9_unified_edit` 2 篇均非编辑安全改写；`t14_policy_guard` 5 命中全是 RAG 混合检索、逐篇核验 **0 可迁移**（"有量不等于有供给"**第五次**生效）；`t10_video_safety` 2 命中均非安全工作 ⇒ 主线⑥本轮**不给建议**。
>
> **🎯 本轮最扎的一个数**：同 prompt 同 seed，所有配置 **bit-identity 全为 0.0**，Emu3.5 SSIM **0.580**、Janus-Pro-7B **0.229** —— 作者原文直接点名「**safety audits and A/B tests on generated images need the serving setup reported**」。**连"改写前后对照"这件事在执行层都不成立**。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **输入没改，图里的字被换了** | [Text Lives in the Guidance](./categories/t2i/papers/2611.25382_silent_text_rewrite_guidance_cache.md) | **北师大 + 北京交大**（主干 Z-Image / Qwen-Image）。缓存 **2.9×** 加速使 word accuracy **62%→46%** 而 ImageReward / CLIP 几乎不动；误差沿 CFG 分解主要来自 **guidance term**（文本区占比为背景 **1.66×**，中英一致）；只重算无条件分支反而更差 **0.235 < 0.386**；GuideCache `r=10%` 在 **2.46×** 下 **46%→61%**（恢复 91%，Qwen-Image 73%）；同等算力只减步数恢复 **83%/90%**。⇒ 出图侧内生风险的机制级证据，修法在生成过程。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-25_AI安全每日深度情报.md) |
| **同 seed 也钉不住出图** | [Reproducible by Seed? Not on GPUs](./categories/t2i/papers/2611.30545_batch_dependent_nondeterminism_t2i.md) | **马德里理工 + 电子科大**（含 Qwen-Image-2.1）。6 模型 × 4 精度 × 3 GPU，**bit-identity 全 0.0**；Emu3.5 bf16/int8 SSIM **0.580/0.551**、Janus-Pro-7B **0.261/0.229**、Qwen-Image-2.1 fp8 **0.811–0.863**，FLUX bf16 **0.999** 而 fp8 破例 **0.829**；跨 GPU 差异与 batch 效应同量级。⇒ 推理加速 / 量化验收必须加 **serving setup 指纹**；I2I 0/0% 拿到**第六种**归因。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-25_AI安全每日深度情报.md) |
| **擦到 0.00，方向一注入就回来** | [SAE-Audit](./categories/t2i/papers/2611.30117_sae_audit_concept_erasure_residue.md) | **上海 AI Lab + Mila + McGill + 大阪大学**。6 擦除器 × 4 域：**nudity 原模型 0.91 → 擦除 0.00 → 注入 0.71/0.48/0.59/0.74/0.77**，随机对照 ≤**0.06**；67 cells 上 Ours 恢复 **38** 格、Wrong-concept 0.04、random 0.02；**31/40** 恢复格满足 scene consistency；Seurat relabel 让 ours **0.94→0.19**（检测器是代理量）。⇒ **行为层归零 ≠ 移除**，权重侧只是压制。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-25_AI安全每日深度情报.md) |
| **赢的是 trade-off，不是擦除率** | [HOSE](./categories/t2i/papers/2611.30592_hose_hierarchical_orthogonal_erasure.md) | **上海大学 + 中科大**。正交子空间投影 + Tripartite 分层 `ε`（深层 2×10⁻¹ vs 浅层 5×10⁻²）；harmful content **−80%**；但 `%HARM` **2.14%** 高于 RECE **1.49%**，赢在 **FID 34.87 最低 / CLIP 26.12 最高 / 组二 Total 19 最低**；Uniform(shallow) FID 31.26 但 Total **178**，Uniform(deep) Total **45** 但 FID **40.28**。⇒ 单指标选方法会挑错；多概念效果依赖语义重叠（PORN/VULG 边界最险）。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-25_AI安全每日深度情报.md) |
| **误杀不是模型弱，是表示逼的** | [Conservatism of Latent Safety Filters](./categories/t2t/papers/2611.23685_latent_safety_filter_conservatism.md) | **UCSD + SDSU**。证明 **overlap 是「接受 0 个不安全转移」时必须拒绝的最小安全转移比例**：planner latent **0.96–0.97** → 独立 safety latent **0.44–0.46**，误杀 **0.302→0.161**、任务达成 **0.39→0.72**（=不设过滤器）；`K_z=50/200` 会改读数；200 次校准抽样 10–90 分位 **0.14–0.18**。⇒ 「能改则不拒」有了数学下界：**换表示才降得了误杀**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-25_AI安全每日深度情报.md) |
| **误杀率读数本身可能是假的** | [Contamination at the Operating Point](./categories/t2t/papers/2611.29629_operating_point_contamination.md) | **Fu Dai 等（首页未列机构）**。null-calibrated 审计（β=0.1%）标出 **88.6% MS1MV3 身份 / 14.3% IJB-C**，人工复核 **69.2%**、残留 **~9.9%**；固定模型只删重叠身份，FNMR 抬 **3.6×/6.3×/13.9×**（FMR 10⁻⁴/10⁻⁵/10⁻⁶），随机删除无效、偏差**不跨模型抵消**（优势削一半）；IJB-C 在 10⁻⁶ 仅 **2.7M** 有效独立比较。⇒ **5.2% 误杀基线要先被审计**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-25_AI安全每日深度情报.md) |

⏱ **今日一句话**：**别再往输入侧加码了，而且连「出图侧」也别再当成一个黑盒**。先把「四栏归因、五臂生成过程干预、serving setup 指纹进事件审计、评测集重叠审计先于阈值调优、反事实恢复对照」补进验收；否则 0/0% 会继续被写成「改写没写好」，而误杀率 5.2% 这个硬约束可能连读数本身都还没被审计过。
"""
start = r.find("## 🔥 今日最具业务价值论文评测 (")
end = r.find("\n---\n\n## 🔭 前沿 Survey", start)
if start != -1 and end != -1:
    r = r[:start] + TODAY_BLOCK + r[end:]

insight = {
    "| 🏆": "| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **钉死输入也钉不住出图（热点三十二）**（NEW） · **生成过程 / 执行环境 / 权重残留 / 验收装置四层**（NEW） · **bit-identity 全 0.0，safety audit 必须报 serving setup**（NEW） | 2026-11-25 |",
    "| 🛡️": "| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **误杀有表示决定的结构性下界 overlap 0.96→0.44**（NEW） · **低 FPR 区 FNMR 被评测集重叠抬高 3.6×→13.9×**（NEW） · **先审计评测集再体检表示最后调阈值**（NEW） | 2026-11-25 |",
    "| 🖼️": "| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **缓存经 CFG guidance 静默改写文本 62%→46%**（NEW） · **同 seed 跨 batch SSIM 0.580/0.229**（NEW） · **擦除归零后 SAE 注入恢复 nudity 0.48–0.77**（NEW） · **HOSE 层次正交子空间赢 trade-off**（NEW） | 2026-11-25 |",
}
lines = r.split("\n")
for i, ln in enumerate(lines):
    for k, v in insight.items():
        if ln.startswith(k):
            lines[i] = v
            break
r = "\n".join(lines)

IDX = [
    ("- **Defense (安全加固):**", "EBSG",
     "[GuideCache / 静默文本改写](./categories/t2i/papers/2611.25382_silent_text_rewrite_guidance_cache.md) (word acc 62%→46% 而图像级分不动 / CFG guidance 项归因) | "
     "[HOSE 层次正交擦除](./categories/t2i/papers/2611.30592_hose_hierarchical_orthogonal_erasure.md) (harmful −80% / FID 34.87 但 %HARM 非最优)",
     "2611.25382"),
    ("- **Benchmark:**", "Unimodal Shortcuts",
     "[SAE-Audit 擦除残留审计](./categories/t2i/papers/2611.30117_sae_audit_concept_erasure_residue.md) (nudity 0.00→注入 0.48–0.77 / 随机 ≤0.06) | "
     "[Batch-Dependent Non-Determinism](./categories/t2i/papers/2611.30545_batch_dependent_nondeterminism_t2i.md) (bit-identity 全 0.0 / SSIM 0.580, 0.229 / serving setup 指纹)",
     "2611.30117"),
    ("- **Benchmark:**", "The Vulnerability Window",
     "[Latent Safety Filter Conservatism](./categories/t2t/papers/2611.23685_latent_safety_filter_conservatism.md) (overlap 0.96→0.44 / 误杀 0.302→0.161) | "
     "[Operating-Point Contamination](./categories/t2t/papers/2611.29629_operating_point_contamination.md) (FNMR 虚高 3.6×→13.9× / N_eff 下限)",
     "2611.23685"),
]
for st, disc, payload, marker in IDX:
    hit = [ln for ln in r.split("\n") if ln.startswith(st) and disc in ln]
    if hit and marker in hit[0]:
        continue
    r = prepend_to_bullet(r, st, disc, payload)

wr("README.md", r)
print("README: badge 340 / date 11-25 / 今日区块 / 洞察表 / 索引 6 篇")

# ---------- 4. t2i-survey ----------
s = rd("insights/t2i-survey.md")
s = s.replace("本项目收录的 **160** 篇 T2I 安全论文", "本项目收录的 **164** 篇 T2I 安全论文")
s = s.replace("**更新日期**: 2026-11-24", "**更新日期**: 2026-11-25")
t2i_rows = [
 " | **Text Lives in the Guidance / GuideCache** | [2611.25382](https://arxiv.org/abs/2611.25382) | 2026 (**北师大 + 北京交大**；主干 Z-Image / Qwen-Image) | **生成过程会静默改写输出语义**：缓存 **2.9×** 使 word accuracy **62%→46%**（0.621→0.464）而 ImageReward / CLIP 几乎不动；误差沿 CFG 分解主要来自 **guidance term**（文本区占比为背景 **1.66×**，中英一致），同等算力只减步数恢复 **83%/90%** ⇒ 损失在缓存对跳步的预测；消融 plain 0.386 / **unconditional only 0.235（更差）** / conditional only 0.481 / both **0.532**；GuideCache `r=10%` 在 **2.46×** 下 **46%→61%**（恢复 91%，Qwen-Image 73%）；13 anchors 3.85× 时 0.124/0.057→0.388/0.334；Qwen-Image 关掉 conditional-norm 重缩放损失翻倍 **0.169 vs 0.084**；中文恢复多于拉丁文本 (NEW) |",
 " | **Reproducible by Seed? Not on GPUs** | [2611.30545](https://arxiv.org/abs/2611.30545) | 2026 (**马德里理工 + 电子科大**；含 Qwen-Image-2.1) | **同 prompt + 同 seed 仍固定不住出图**：6 模型 × 4 精度 × 3 GPU，所有配置 **bit-identity = 0.0**、replay control bit-exact；Emu3.5 bf16/int8 SSIM **0.580/0.551**、Janus-Pro-7B sampled/greedy **0.261/0.229**、Qwen-Image-2.1 fp8 **0.811–0.863**、HiDream-O1 fp8 **0.748/0.731/0.686**、FLUX bf16 0.999 而 **fp8 破例 0.829**；跨 GPU 差异与 batch 效应同量级。作者原文：**safety audits / A/B tests 必须报 serving setup**；以 image editing「改一个对象其余保持原样」为例 ⇒ **I2I 0/0% 第六种归因** (NEW) |",
 " | **SAE-Audit / What Remains After Concept Erasure?** | [2611.30117](https://arxiv.org/abs/2611.30117) | 2026 (**上海 AI Lab + Mila + McGill + 大阪大学**) | **行为层归零不构成移除证据**：共享 SAE 找擦除后响应变弱的特征，把原模型导出的固定稀疏方向注入编辑后模型（不改权重不改 prompt）；6 擦除器 × 4 域，**NSFW nudity 原模型 0.91 → 擦除 0.00 → 注入 0.71/0.48/0.59/0.74/0.77**，随机对照 ≤**0.06**；67 cells 上 Ours **0.40 / nudity 0.66**、恢复 **38** 格，Reverse-SAeUron 0.35，Wrong-concept 0.04、random 0.02；**31/40** 恢复格满足 scene consistency；**Seurat relabel 使 ours 0.94→0.19**（检测器是代理量）；SAE round-trip 单独对 UCE/cat **+0.16~+0.34**；top-10 Jaccard 0.154。⇒ 权重侧只是压制 (NEW) |",
 " | **HOSE / Hierarchical Orthogonal Subspace Erasure** | [2611.30592](https://arxiv.org/abs/2611.30592) | 2026 (**上海大学 + 中科大**) | **赢的是 trade-off 不是擦除率**：参数更新投到通用知识正交子空间 + Tripartite 分层 `ε`（一般概念 5×10⁻²/6×10⁻²/**2×10⁻¹**，风格 1×10⁻³/3×10⁻³/1.6×10⁻¹）；harmful content **−80%**；组一 `%HARM` **2.14%** 高于 RECE **1.49%** / UCE 1.82%，但 **FID 34.87 为编辑类最低、CLIP 26.12 最高**，组二 Total **19** 最低；消融 Uniform(shallow) FID **31.26** 但 Total **178**、Uniform(deep) Total **45** 但 FID **40.28**；5 次运行 95% CI，Genitalia 6.50→1.10 (p=4.5×10⁻⁵)。局限：SD1.4/U-Net、多概念依赖语义重叠 (NEW) |",
]
t2i_rows = [x.lstrip() for x in t2i_rows]
s = rows_after(s, "| **P2E / Prune to Expand**", t2i_rows, "2611.25382")
note = "*本次 Survey 更新：2026-11-25（新增 4 篇：2611.25382 缓存经 CFG guidance 静默改写文本 62%→46%、2611.30545 同 seed 下 batch/GPU/精度决定出图且 bit-identity 全 0、2611.30117 SAE 注入使擦除归零的 nudity 恢复到 0.48–0.77、2611.30592 HOSE 层次正交子空间赢 trade-off 而非擦除率；现为 **164** 篇）。*"
if "本次 Survey 更新：2026-11-25" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-24（新增 4 篇：2611.27339",
                  note + "\n*上次 Survey 更新：2026-11-24（新增 4 篇：2611.27339", 1)
wr("insights/t2i-survey.md", s)
print("t2i-survey: 164 / +4 rows / 更新注记")

# ---------- 5. t2t-survey ----------
s = rd("insights/t2t-survey.md")
s = s.replace("本项目收录的 **134** 篇 T2T 安全论文", "本项目收录的 **136** 篇 T2T 安全论文")
s = s.replace("**更新日期**: 2026-11-24", "**更新日期**: 2026-11-25")
t2t_rows = [
 "| **Measuring the Conservatism of Latent Safety Filters** | [2611.23685](https://arxiv.org/abs/2611.23685) | 2026 (**UCSD + SDSU**, PMLR 2027) | over-refusal 结构性下界 / conformal / per-category 阈值 | **误杀不是模型弱，是表示逼的**：证明 **overlap 是「接受 0 个不安全转移」时必须拒绝的最小安全转移比例**；planner latent **0.96–0.97** / jointly trained 0.94–0.96 / 独立 safety latent **0.44–0.46**，δ=0.02 下拒安全动作 **0.302/0.318/0.161**、任务达成 **0.39/0.32/0.72**（无过滤器 0.72）；`K_z=50/200` 会改 overlap 读数，200 次校准抽样 10–90 分位 `z_s` **0.14–0.18**。⇒ 调阈值降不下去，只能换表示；「能改则不拒」有了数学下界 (NEW) |",
 "| **Contamination at the Operating Point** | [2611.29629](https://arxiv.org/abs/2611.29629) | 2026 (**Fu Dai, K. Taha, N. Werghi, M. Assefa**；PDF 首页未列机构) | 评测集重叠审计 / operating point / 最小可报告 FPR | **误杀率读数本身可能是假的**：偏差不是加性小量（旧工作最多 +1.01pp）而是**随 FMR 下降增长的乘性误差**；null-calibrated 审计（β=0.1%）标出 **88.6% MS1MV3 身份 / 14.3% IJB-C**，人工复核 **69.2%** ⇒ 残留 ~**9.9%**；固定模型只删重叠身份，FNMR 抬 **3.6×/6.3×/13.9×**（10⁻⁴/10⁻⁵/10⁻⁶），随机删除无效，偏差**不跨模型抵消**（优势削一半）；IJB-C 在 10⁻⁶ 仅 **2.7M** 有效独立比较、最小可报 FMR ≈ **6×10⁻⁵**。⇒ 5.2% 误杀基线要先审计评测集 (NEW) |",
]
s = rows_after(s, "| **Your Judge Inherits Your Prompt**", t2t_rows, "2611.23685")
note_t = "*本次 Survey 更新：2026-11-25（新增 2 篇方法论迁移：2611.23685 误杀有表示决定的结构性下界 overlap 0.96→0.44 且换表示才降、2611.29629 低 FPR 区 FNMR 被评测集重叠乘性抬高 3.6×→13.9×；现为 **136** 篇）。*"
if "本次 Survey 更新：2026-11-25" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-24（新增 2 篇方法论迁移：2611.27155",
                  note_t + "\n*上次 Survey 更新：2026-11-24（新增 2 篇方法论迁移：2611.27155", 1)
wr("insights/t2t-survey.md", s)
print("t2t-survey: 136 / +2 rows / 更新注记")

# ---------- 6. benchmark README ----------
b = rd("categories/t2i/benchmark/README.md")
b = b.replace("最后回填: 2026-11-24 | 共 **52** 条", "最后回填: 2026-11-25 | 共 **54** 条")
newrows = [
 "| **SAE-Audit（概念擦除残留审计协议）** | [2611.30117](https://arxiv.org/abs/2611.30117) | 2026 arXiv（**上海 AI Lab + Mila + McGill + 大阪大学**） | **行为层归零 ≠ 移除**：6 擦除器 × 4 域，nudity 原模型 0.91 → 擦除 0.00 → 固定稀疏方向注入恢复 **0.48–0.77**（随机对照 ≤0.06）；67 cells 恢复 38 格、31/40 满足 scene consistency；Seurat relabel 使判定 0.94→0.19 ⇒ 检测器代理量体检 (NEW) |",
 "| **Batch-Dependent Non-Determinism（生成侧执行环境评测）** | [2611.30545](https://arxiv.org/abs/2611.30545) | 2026 arXiv（**马德里理工 + 电子科大**） | **同 prompt + 同 seed 仍不可复现**：6 模型 × 4 精度 × 3 GPU，**bit-identity 全 0.0**、SSIM 低至 **0.580/0.551/0.261/0.229**；作者点名 safety audits / A/B 必须报 serving setup ⇒ 生成侧不劣化验收协议 (NEW) |",
]
tail = "\n[← 返回文生图目录](../README.md)"
if "2611.30117" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2i/benchmark/README.md", b)

b = rd("categories/t2t/benchmark/README.md")
b = b.replace("最后回填: 2026-11-24 | 共 **31** 条", "最后回填: 2026-11-25 | 共 **33** 条")
newrows = [
 "| **Latent Safety Filter Conservatism（over-refusal 下界度量）** | [2611.23685](https://arxiv.org/abs/2611.23685) | 2026 arXiv（**UCSD + SDSU**, PMLR 2027） | **overlap 是必须拒绝的最小安全转移比例**：planner 0.96–0.97 → safety latent 0.44–0.46，误杀 0.302→0.161、任务达成 0.39→0.72；`K_z` 口径必报、200 次校准抽样分位 (NEW) |",
 "| **Contamination at the Operating Point（评测集重叠审计）** | [2611.29629](https://arxiv.org/abs/2611.29629) | 2026 arXiv（**首页未列机构**） | **低 FPR 区 FNMR 被重叠乘性抬高 3.6×/6.3×/13.9×**，随机删除无效、偏差不跨模型抵消；null-calibrated 审计 + 2×2 + `N_eff` + 最小可报告 FPR (NEW) |",
]
tail = "\n[← 返回文生文目录](../README.md)"
if "2611.23685" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2t/benchmark/README.md", b)
print("benchmark: t2i 54 / t2t 33")

# ---------- 7. Landscape ----------
L = rd("insights/AI_Security_Landscape_2026.md")
L = L.replace("基于本项目收录的 **334 篇**", "基于本项目收录的 **340 篇**")
L = L.replace("**更新日期**: 2026-11-24（v3.19 增量更新）", "**更新日期**: 2026-11-25（v3.20 增量更新）")
L = L.replace("### T2T 论文分布（134 篇）", "### T2T 论文分布（136 篇）")
L = L.replace("### T2I 论文分布（160 篇）", "### T2I 论文分布（164 篇）")
L = L.replace(
    "*最近更新：2026-11-24（v3.19 增量更新），累计论文数 **334**（T2T: **134** 篇，T2I: **160** 篇，Agentic Search: **40** 篇）。*",
    "*最近更新：2026-11-25（v3.20 增量更新），累计论文数 **340**（T2T: **136** 篇，T2I: **164** 篇，Agentic Search: **40** 篇）。*")

hot32 = """### 🔥 热点三十二：钉死了输入，也钉不住出图 —— 输入改写够不到的四层（2026-11-25 新增）

热点三十一说「分数没动，判定全换了」。这一轮六篇再往下一层：**连输入与输出之间的对应关系都不成立**。11-24 把 3,000 条 case 中 2,700+ 条归为「出图侧内生风险」，本轮把这个黑盒拆成四条**互不覆盖、可分别检验**的机制：

| 层 | 机制 | 实测 | 对应修法 |
|---|---|---|---|
| **① 生成过程** | 缓存对跳步的预测经 **CFG guidance 项**改写输出语义 | word accuracy **62%→46%**，ImageReward / CLIP 几乎不动；误差文本区占比为背景 **1.66×** | 只对 guidance 误差大的 token 重算条件+无条件两分支（**46%→61% @2.46×**） |
| **② 执行环境** | 归约顺序随 batch 张量形状变、8-bit 放大数值差 | 同 prompt+seed 下 **bit-identity 全 0.0**；SSIM **0.580 / 0.551 / 0.261 / 0.229** | serving setup 指纹（batch / bit 宽 / GPU / 缓存 / 步数）进事件审计 |
| **③ 权重残留** | 概念擦除是压制不是移除 | nudity 擦除后 strict ASR **0.00** → 固定 SAE 方向注入 **0.48–0.77**（随机 ≤0.06） | 任何「已擦除」结论必须过反事实恢复对照；同日 HOSE 的 −80% 只是能力上界 |
| **④ 验收装置** | 误杀有表示决定的下界；误杀读数还会被评测集重叠污染 | overlap **0.96→0.44** 使误杀 **0.302→0.161**；低 FPR 区 FNMR 虚高 **3.6×→13.9×** | ① 审计评测集 → ② 体检表示可判性 → ③ 才做约束式选点与 conformal 认证 |

**由此提炼三条新纪律**：① **「出图侧」不再是一个可整体归因的黑盒**——3,000 条 case 的 2,700+ 条应按四栏重打标，任何一栏占比 >20% 即宣告「改写还不够严」这个归因作废；② **推理加速/量化的不劣化验收必须同时覆盖生成侧与判定侧**：11-24 的判定模型逐对翻转（1.1–12.3%）+ 本轮生成模型语义改写与执行环境漂移，合成「生成侧语义完整性 / 判定侧逐对翻转 / 分层 F1 与安全率 / serving setup 指纹」四栏下限；③ **误杀率 5.2% 这个硬约束本身要先被审计**——23685 证明它有结构性下界、29629 证明读数可能被评测集重叠在低 FPR 区乘性抬高且偏差不跨模型抵消。

**权重侧/输入侧边界第十二轮**：本轮第一次出现**同日配对**——HOSE（有害内容 −80%、FID 34.87 为编辑类最低、但 `%HARM` 2.14% 并非最优）给出权重侧能力上界，SAE-Audit（行为层 0.00 而恢复层 0.48–0.77）给出失效边界。⇒ **不能用「擦除器更强」回答「擦除是否可靠」**；四层通路（输入侧热更新改写 / 权重侧擦除 / 生成过程干预 / 输出侧图审与溯源）失效方向互不覆盖，任一层单独宣称内容安全已解决即判越界。新结论：**行为层归零不构成移除证据**。

**I2I 0/0% 新增两种可证伪归因**：第六种——30545 以 image editing「改一个对象、其余保持原样」为例，说明编辑前后对照会被 batch 非确定性污染，导致「改对了」永远无法判定；第七种——23685 的粗粒度「每 cell 一个判定」路由有结构性 overlap，会把安全指令一起拒/放。二者都不需要重训：先强制 solo-vs-solo 同配置，再把分流输出从「是否改写」改成带分数的多候选排序。

"""
if "热点三十二" not in L:
    L = L.replace("### 🔥 热点三十一：", hot32 + "### 🔥 热点三十一：", 1)

v320 = """*本次 v3.20 更新：新增 4 篇 T2I/T+I2I 论文（Text Lives in the Guidance：缓存 2.9× 使 word accuracy 62%→46% 而图像级分不动，误差源于 CFG guidance 项，只重算无条件分支反而更差 0.235，GuideCache 2.46× 下恢复 91%，中英退化幅度不同；Reproducible by Seed?：6 模型 × 4 精度 × 3 GPU 下 bit-identity 全 0.0、SSIM 低至 0.229，作者点名 safety audits / A/B 必须报 serving setup；SAE-Audit：nudity 擦除归零后固定方向注入恢复 0.48–0.77、随机 ≤0.06，Seurat relabel 使判定 0.94→0.19；HOSE：正交子空间 + Tripartite 分层 ε，harmful −80% 但 %HARM 2.14% 高于 RECE 1.49%，赢在 FID 34.87 / CLIP 26.12 的 trade-off）与 2 篇方法论迁移（Latent Safety Filter Conservatism：overlap 0.96→0.44 使误杀 0.302→0.161、任务达成 0.39→0.72；Contamination at the Operating Point：低 FPR 区 FNMR 虚高 3.6×/6.3×/13.9×、偏差不跨模型抵消、IJB-C 仅 2.7M 有效独立比较），并新增一条范式信号（热点三十二）：**钉死了输入，也钉不住出图**。供给侧为**供给回暖第二轮**：网页端十分类串行全批 **4139 篇**（1871 篇带摘要），公告批次 11-18→11-24 其中 **11-24 单批新增 1442 篇**；复用昨日 1739 条摘要缓存只新抓 688 篇；主题词 **18 路** + 形态 **12 路**全部本地正则复现、零第二次检索请求；`t2_prompt_rewrite` 严格 **0**（空窗第 **18** 周），I2I 编辑改写 / 统一模型改写面 / NSFW 图审 / 跨语言安全改写 / GRPO 安全改写 / 策略护栏混合召回**本轮全部零供给**；`t14_policy_guard` 5 命中全为 RAG 混合检索、逐篇核验 **0 可迁移**（「有量不等于有供给」第五次生效），`t10_video_safety` 2 命中均非安全工作 ⇒ 主线⑥不给建议。机构核验 6/6 HTTP 200、HTML affiliation 全空由 PDF 首页 pypdf 回退（**第 12 次连续生效**），并修复 HOSE PDF 代理字符写入失败；**头部公司作者机构 0 篇**，但被测主干含阿里 Z-Image / Qwen-Image / Qwen-Image-2.1。*
"""
if "v3.20 更新" not in L:
    L = L.replace("*本次 v3.19 更新：", v320 + "*本次 v3.19 更新：", 1)
wr("insights/AI_Security_Landscape_2026.md", L)
print("Landscape: v3.20 / 340 / 热点三十二")
