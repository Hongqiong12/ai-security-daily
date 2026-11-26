#!/usr/bin/env python3
"""2026-11-27 门面同步（WORKFLOW.md Step 5 / Step 6）。

幂等：所有插入带 marker 检查，复跑不改变任何文件内容。
计数一律以磁盘 papers/*.md 精确扫描为准，禁止估算。
"""
import json, re, os, glob

ROOT = "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
os.chdir(ROOT)

TODAY = "2026-11-27"
IDS = ["2611.33316", "2611.34446", "2611.26627", "2611.29029",
       "2611.33307", "2611.33263"]
SLUG = {
    "2611.33316": "2611.33316_flowgrpo_sharpening_unlocking",
    "2611.34446": "2611.34446_preservereward_edit_consistency",
    "2611.26627": "2611.26627_rl_is_activation_steering",
    "2611.29029": "2611.29029_t2ispec_topic_disparity",
    "2611.33307": "2611.33307_multilingual_confidence_lag",
    "2611.33263": "2611.33263_what_who_when_policy_decoupling",
}

counts = {
    "t2t": len(glob.glob("categories/t2t/papers/*.md")),
    "t2i": len(glob.glob("categories/t2i/papers/*.md")),
    "agentic": len(glob.glob("categories/agentic-search/papers/*.md")),
}
counts["total"] = sum(counts.values())
assert counts == {"t2t": 139, "t2i": 173, "agentic": 40, "total": 352}, counts
MONTH_COUNT = len(glob.glob("daily-reports/2026-11/*.md"))
MISSING = ["2026-11-%02d" % d for d in range(11, 23)]


def rd(p):
    return open(p, encoding="utf-8").read()


def wr(p, s):
    open(p, "w", encoding="utf-8").write(s)


def rows_after(s, prefix, rows, marker):
    """把 rows 插到以 prefix 开头的行之后，保持 Markdown 表格连续。"""
    if marker in s:
        return s
    out, done = [], False
    for ln in s.split("\n"):
        out.append(ln)
        if not done and ln.startswith(prefix):
            out.extend(rows)
            done = True
    if not done:
        raise RuntimeError("anchor not found: " + prefix[:70])
    return "\n".join(out)


def prepend_bullet(s, start, disc, payload, marker):
    """在指定模态的 bullet 头部前插链接，marker 存在即跳过。"""
    if marker in s:
        return s
    lines = s.split("\n")
    hits = [i for i, ln in enumerate(lines) if ln.startswith(start) and disc in ln]
    if len(hits) != 1:
        raise RuntimeError("bullet not unique: %s / %s -> %d" % (start, disc, len(hits)))
    i = hits[0]
    head, sep, rest = lines[i].partition("** ")
    if not sep:
        head, sep, rest = lines[i].partition(": ")
    if not sep:
        raise RuntimeError("bad bullet")
    lines[i] = head + sep + payload + " | " + rest
    return "\n".join(lines)


# ---------- 1. selected_papers.json 120 → 126 ----------
sel = json.load(open("selected_papers.json", encoding="utf-8"))
have = {x["id"].split("v")[0] for x in sel}
pool = json.load(open("/tmp/full_1127.json", encoding="utf-8"))
byid = {x["id"].split("v")[0]: x for x in pool}
added = []
for aid in IDS:
    if aid in have:
        continue
    x = byid.get(aid, {})
    title = re.sub(r"^(?:Title|Abstract):\s*", "", x.get("title", "")).strip()
    abstract = re.sub(r"^(?:Title|Abstract):\s*", "", (x.get("abstract") or "")).strip()
    assert title and abstract, aid
    sel.append({"id": aid + "v1", "title": title, "summary": abstract,
                "published": x.get("published", TODAY), "selected_date": TODAY})
    added.append(aid)
wr("selected_papers.json", json.dumps(sel, ensure_ascii=False, indent=1) + "\n")
print("selected_papers:", len(sel), "| added:", added)

# ---------- 2. _meta.json ----------
meta = {
    "_meta_version": "1.0",
    "last_updated": TODAY,
    "paper_counts": counts,
    "survey_versions": {
        "t2t-survey": {"date": TODAY, "count": counts["t2t"]},
        "t2i-survey": {"date": TODAY, "count": counts["t2i"]},
        "agentic-search-survey": {"date": "2026-10-30", "version": "v1.9", "count": 40},
        "landscape_2026": {"date": TODAY, "version": "v3.22", "total_papers": counts["total"]},
    },
    "benchmark_status": {
        "t2t_benchmark": {"entries": 35, "last_updated": TODAY},
        "t2i_benchmark": {"entries": 58, "last_updated": TODAY},
        "agentic_benchmark": {"entries": 10, "last_updated": "2026-04-30"},
    },
    "daily_reports": {
        "latest": TODAY,
        "this_month_count": MONTH_COUNT,
        "missing_dates": MISSING,
    },
    "workflow_version": "2.3",
    "today_selection": {
        "t2i": [SLUG[a] for a in IDS[:4]],
        "t2t_migration": [SLUG[a] for a in IDS[4:]],
        "theme": "把「一个增益」拆开 —— RL 涨点、加速比、置信阈值、安全标签全都装错了单位；Flow-GRPO 解剖与 Activation Steering 构成「安全率上涨不等于策略变强」的独立双证据",
    },
    "_note": "This file is the single source of truth for all paper counts. Automation must update this file on every run. Never estimate counts — always use search_file to scan papers/ directories.",
}
wr("_meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
print("_meta.json:", counts["total"], "/ month_count", MONTH_COUNT)

# ---------- 3. README ----------
r = rd("README.md")
r = r.replace("Papers-346-green.svg", "Papers-352-green.svg")
r = r.replace("Last-Update-2026--11--26-orange.svg", "Last-Update-2026--11--27-orange.svg")
r = r.replace("基于 **346** 篇安全论文萃取的全局视野", "基于 **352** 篇安全论文萃取的全局视野")

TODAY_BLOCK = """## 🔥 今日最具业务价值论文评测 (2026-11-27)

> **今天六篇把「一个增益」拆开：RL 涨的 0.32 分里四个技能只是锐化、一个才是解锁；1/65 参数的常数向量能复现 90–96.3% 的 RL 奖励增益。最扎的一刀：英文上钉 95% 的阈值，中文只有 93.1%、泰米尔语 90.0%——因为置信度只掉一半。**
>
> **✅ 供给侧**：网页端十分类 `/list/<cat>/recent?show=2000` 串行全批扫描，公告批次 **11-20→11-26**（717/562/1440/844/**775**）；全批池 **4338 篇**（2056 篇带摘要），复用昨日 1982 条摘要缓存回填 1671、仅新抓 **385** 篇；主题词 **26 路** + 形态 **12 路**全部本地正则复现、零第二次检索请求。`t2_prompt_rewrite` 严格词表 3 命中**全为误命中**（空窗第 **20** 周），但三条长期空窗通道同日补齐 —— **GRPO 奖励解剖 / 跨语言阈值 / 策略可配置护栏**。
>
> **🎯 工业界连续两轮命中 3 篇**：**JD.com（京东）** PreserveReward（被优化主干 **Qwen-Image-2.1**）、**IBM Research** 参与 RL=Activation Steering、**Sword Health** 策略护栏。**T2I 占比 66.7%。**
>
> **⚠️ 仍零供给**：输入侧安全改写方法（第 20 周）/ I2I 安全改写方法 / 统一生成-编辑改写面 / NSFW 图审 SFT / i2v-t2v 生成安全（主线⑥不给建议）。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **安全率涨了 ≠ 策略变强** | [Flow-GRPO 按技能解剖](./categories/t2i/papers/2611.33316_flowgrpo_sharpening_unlocking.md) | **NCSU + Purdue**（SD3.5-M）。GenEval **0.63→0.95** 拆成：四技能**锐化**（RL 的 pass@1 = base 的 4–10 个样本，pass@32 动 ≤0.013，best-of-4 回收 76%）；空间关系**解锁**（pass@32 **0.76→1.00**、Δceiling +0.31、31 个零覆盖 prompt **93%** 被救、**128 个 base 样本仍买不到**）。⇒ 锐化转 best-of-k + verifier，解锁才动训练；**D2 的零训练闸门**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-27_AI安全每日深度情报.md) |
| **1/65 参数复现 90–96.3% RL 增益** | [RL = Activation Steering](./categories/t2i/papers/2611.26627_rl_is_activation_steering.md) | **Virginia Tech + fal + Georgia Tech + IBM Research**。188 个常数向量 **0.29M 参数 = rank-32 LoRA 的 1/65**，对每个 prompt/token/seed 完全相同，拟合目标**不含奖励**，恢复六个 image ckpt **90.0–96.3%**；只训向量跑 Flow-GRPO 反超权重 RL **104.6%/103.6%**。⇒ 策略容量不是瓶颈，奖励稀疏才是；与上篇构成独立双证据。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-27_AI安全每日深度情报.md) |
| **奖励器自己没被验收** | [PreserveReward](./categories/t2i/papers/2611.34446_preservereward_edit_consistency.md) | **JD.com 京东 + 中科大 + 华南理工 + 南京大学**（主干 Qwen-Image-2.1）。双教师 OPSD + minimum-KL 校准 + 梯度路由（双负则跳过）；**84.70%/84.60%/80.73%** 人类偏好对齐、9B 超所有开源 reward model。**Table 2 反例**：EditScore-72B / RationalRewards / UnifiedReward 做 RL 后 GEdit-v1 **反不如 Base**（8.73/8.47/8.57 vs 8.86）而 KRIS 却涨 ⇒ 同一奖励器跨集方向反转。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-27_AI安全每日深度情报.md) |
| **减 42% 的活只快 1.09 倍** | [T2ISpec](./categories/t2i/papers/2611.29029_t2ispec_topic_disparity.md) | **密歇根 + 斯坦福 + 宾大 + 俄亥俄州立 + 南洋理工**（兑现 11-26 优先精读）。1,400 prompts × 7 topic × 2 难度；AR topic 偏离 **±20%**；ADT-Tree **−42.0% work → 仅 1.0889×**；Overall criterion **0.0000** 掩盖 text **+0.0233** / commonsense **−0.0242**；SpeCa 阈值 5→9 使 Easy **+0.0383** / Hard **−0.0517**。⇒ 加速比必须按类目 × 难度拆开报。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-27_AI安全每日深度情报.md) |
| **英文阈值在中文只有 93.1%** | [Lost in Translation](./categories/t2t/papers/2611.33307_multilingual_confidence_lag.md) | **南洋理工 + NUS + VinUniversity**（迁移）。25 模型 × 17 子类 × 14 语言 × 25,626 平行条目；**325** 个 model–language pair 全掉准确率、**301** 个过度自信上升；`ΔAcc −3.5` 而 `ΔConf −1.8`；英文 τ 的实际准确率 **泰米尔 90.0% / 中文 93.1% / 均值 92.6%**；温度缩放修 ECE **4.1%→2.9%** 但修不回准确率。⇒ 英文 ASR 飙升的机制级解释，先分语言校准再谈合并训练。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-27_AI安全每日深度情报.md) |
| **策略不写进权重** | [What, Who, and When](./categories/t2t/papers/2611.33263_what_who_when_policy_decoupling.md) | **Sword Health + Yale + IST**（迁移，`t14_policy_guard` 六周零供给终结）。模型只输出 (what, who, when) 三元组，`triplet → safety protocol` 是**权重外可热更新、可审计的决策树**；3WS 分维加权（what/who >89% vs when **0.53** 一致率）；短 CoT + 长度惩罚使 median latency 低 **~10×**，高 recall 下 **FPR 0.02–0.09**；推理收益集中在 3W **0.72→0.90** 而非 BA。⇒ 换策略不重训、不重标注。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-27_AI安全每日深度情报.md) |

⏱ **今日一句话**：**别急着把涨分记成能力**。动训练前先报 `k*` / Δceiling / 常数臂解释率；阈值先按语言 × 难度体检；策略表换一次要比换 ckpt 更优先。输入改写优化预算继续冻结，重心留在出图侧生成过程干预与验收单位重构。
"""
start = r.find("## 🔥 今日最具业务价值论文评测 (")
end = r.find("\n---\n\n## 🔭 前沿 Survey", start)
if start != -1 and end != -1:
    r = r[:start] + TODAY_BLOCK + r[end:]

insight = {
    "| 🏆": "| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **把「一个增益」拆开（热点三十四）**（NEW） · **RL 涨分分锐化/解锁 + 常数参数自由度**（NEW） · **阈值语言漂移与策略表解耦**（NEW） | 2026-11-27 |",
    "| 🛡️": "| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **英文 95% 阈值中文只有 93.1%**（NEW） · **置信度只掉一半**（NEW） · **策略写在权重外可热更新**（NEW） | 2026-11-27 |",
    "| 🖼️": "| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **Flow-GRPO：128 个 base 样本买不到 RL 的 pass@1**（NEW） · **1/65 参数复现 90–96.3% RL 增益**（NEW） · **奖励器跨评测集方向反转**（NEW） · **−42% work 只换 1.0889×**（NEW） | 2026-11-27 |",
}
lines = r.split("\n")
for i, ln in enumerate(lines):
    for k, v in insight.items():
        if ln.startswith(k):
            lines[i] = v
            break
r = "\n".join(lines)

# 索引：按模态专属判别词插入到对应 bullet 头部
IDX = [
    ("- **Defense (安全加固):**", "HinT 蒸馏修正而非改写",
     "[PreserveReward 编辑一致性奖励](./categories/t2i/papers/2611.34446_preservereward_edit_consistency.md) (84.70% 人类对齐 / 双教师+梯度路由双负跳过 / 奖励器跨集方向反转 / JD.com) | "
     "[RL = Activation Steering](./categories/t2i/papers/2611.26627_rl_is_activation_steering.md) (0.29M = LoRA 1/65 / 恢复 90.0–96.3% / 拟合不含奖励 / IBM Research)",
     "2611.34446", "t2i"),
    ("- **Benchmark:**", "BODYBENCH 裸体化防护审计",
     "[T2ISpec topic 加速背离](./categories/t2i/papers/2611.29029_t2ispec_topic_disparity.md) (−42.0% work 只换 1.0889× / Overall 0.0000 掩盖两向 topic / 阈值跨难度方向反) | "
     "[Flow-GRPO 按技能 pass@k 解剖](./categories/t2i/papers/2611.33316_flowgrpo_sharpening_unlocking.md) (四技能锐化 k*=4–10 / 关系解锁 Δceiling +0.31 / 零覆盖 93% 被救)",
     "2611.29029", "t2i"),
    ("- **Defense (安全加固):**", "Risk-certified 约束式策略选点",
     "[What/Who/When 策略表解耦](./categories/t2t/papers/2611.33263_what_who_when_policy_decoupling.md) (权重外可热更新 / 3WS 分维加权 / when 一致率 0.53 / FPR 0.02–0.09)",
     "2611.33263", "t2t"),
    ("- **Benchmark:**", "Measurement Artifacts 量化评测仪器项",
     "[Lost in Translation 跨语言阈值漂移](./categories/t2t/papers/2611.33307_multilingual_confidence_lag.md) (325/325 pair 掉准确率 / Gap +1.6 / 中文 93.1% 泰米尔 90.0% / ECE 4.1→2.9% 而准确率不回)",
     "2611.33307", "t2t"),
]
for st, disc, payload, marker, mod in IDX:
    r = prepend_bullet(r, st, disc, payload, marker)

wr("README.md", r)
print("README: badge 352 / date 11-27 / 今日区块 / 洞察表 / 索引 6 篇")

# ---------- 4. t2i-survey ----------
s = rd("insights/t2i-survey.md")
s = s.replace("本项目收录的 **169** 篇 T2I 安全论文", "本项目收录的 **173** 篇 T2I 安全论文")
s = s.replace("**更新日期**: 2026-11-26", "**更新日期**: 2026-11-27")
t2i_rows = [
    "| **Flow-GRPO / A Skill-Wise Analysis** | [2611.33316](https://arxiv.org/abs/2611.33316) | 2026 (**NCSU + Purdue**；SD3.5-M) | **0.63→0.95 不是一个数**：共享种子 pass@k 逐技能解剖，四技能**锐化**（RL 的 pass@1 = base 的 **4/10/8/5** 个样本、pass@32 动 ≤**0.013**、best-of-4 回收 **76%**）；空间关系**解锁**（pass@32 **0.76→1.00**、Δceiling **+0.31**、31 个零覆盖 prompt **93%** 被救、base pass@128 **0.89** 仍低于 RL pass@1 **0.94**）；LoRA dial 显示 ceiling 领先 pass@1；训练顺序「锐化先到、解锁晚到」。⇒ **安全率涨了先判锐化/解锁**，锐化转 best-of-k + verifier，解锁才动训练 (NEW) |",
    "| **RL Post-Training Is Activation Steering** | [2611.26627](https://arxiv.org/abs/2611.26627) | 2026 (**Virginia Tech + fal + Georgia Tech + IBM Research**；SD3.5-M / FLUX.1-dev / Wan2.1/2.2) | **1/65 参数复现 90–96.3% RL 增益**：188 个常数向量 **0.29M = 288,768 参数**，对每个 prompt/token/seed 相同，拟合目标为 velocity matching、**不含奖励**；六个 image ckpt 恢复 **90.0/90.8/94.4/95.2/95.9/96.3%**，video 89.8%/111.9%；s_mean 只恢复 12.2–79.0%；只训向量跑 Flow-GRPO 反超权重 RL **104.6%/103.6%**。LoRA $\\Delta W=ba^\\top$ 是「固定方向 × 输入相关权重」，steering 把权重钉成常数。⇒ 策略容量不是瓶颈、奖励稀疏才是；与 33316 构成独立双证据 (NEW) |",
    "| **PreserveReward / 编辑一致性奖励** | [2611.34446](https://arxiv.org/abs/2611.34446) | 2026 (**JD.com 京东 + 中科大 + 华南理工 + 南京大学**；主干 **Qwen-Image-2.1**) | **一致性必须区分「必要修改 vs 意外改动」**：双教师 OPSD（local 匹配裁剪 / joint 全图+意图）、minimum-KL 投影校准到误差预算 0.01、按与 Score-MSE 梯度对齐度路由且**双负跳过蒸馏**；额外局部证据仅训练期用、推理零开销。Table 1 人类偏好 **84.70/84.60/80.73%**（9B 80.60/78.93/76.61% 超所有开源 reward model）；消融「双负跳过」值 **+4.7 点**。**Table 2 反例**：EditScore-72B / RationalRewards / UnifiedReward 做 RL 后 GEdit-v1 **反不如 Base**（8.73/8.47/8.57 vs 8.86）而 KRIS 却涨 ⇒ 奖励器跨集方向反转、本身要先被验收 (NEW) |",
    "| **T2ISpec / 投机解码分层基准** | [2611.29029](https://arxiv.org/abs/2611.29029) | 2026 (**密歇根 + 斯坦福 + 宾大 + 俄亥俄州立 + 南洋理工 + Independent**) | **一个 Overall 加速比装错单位**：1,400 prompts × 7 topic × 2 难度、paired Target-only 三列同报；AR topic 偏离 **±20%**、diffusion **±4%**；**ADT-Tree −42.0% work → 仅 1.0889×**；Overall criterion **0.0000** 掩盖 text **+0.0233** / commonsense **−0.0242**；SpeCa 阈值 5→9 使 Easy **+0.0383** / Hard **−0.0517**；TopicRoute 六组几何均值 **1.0308×** 且外迁 DrawBench。⇒ 加速比按类目 × 难度拆报，并配 Δwork 与安全率两列 (NEW) |",
]
s = rows_after(s, "| **VeriOrigin / 主动图像保护**", t2i_rows, "2611.33316")
note = "*本次 Survey 更新：2026-11-27（新增 4 篇 T2I/T+I2I：2611.33316 Flow-GRPO 按技能 pass@k 把 0.63→0.95 拆成四锐化一解锁 / 128 个 base 样本仍买不到；2611.26627 常数 steering vectors 0.29M 参数恢复 90–96.3% RL 增益；2611.34446 PreserveReward 双教师一致性奖励 + 奖励器跨集方向反转，JD.com 主干 Qwen-Image-2.1；2611.29029 T2ISpec −42% work 只换 1.0889× 且 Overall 掩盖两向 topic；现为 **173** 篇）。*"
if "本次 Survey 更新：2026-11-27" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-26（新增 5 篇 T2I/T+I2I",
                  note + "\n*上次 Survey 更新：2026-11-26（新增 5 篇 T2I/T+I2I", 1)
wr("insights/t2i-survey.md", s)
print("t2i-survey: 173 / +4 rows")

# ---------- 5. t2t-survey ----------
s = rd("insights/t2t-survey.md")
s = s.replace("本项目收录的 **137** 篇 T2T 安全论文", "本项目收录的 **139** 篇 T2T 安全论文")
s = s.replace("**更新日期**: 2026-11-26", "**更新日期**: 2026-11-27")
t2t_rows = [
    "| **Lost in Translation, Not in Confidence** | [2611.33307](https://arxiv.org/abs/2611.33307) | 2026 (**南洋理工 + NUS + VinUniversity**) | 跨语言阈值漂移 / guardrail 校准 / 分层宏平均背离 | **英文设的 95% 阈值，中文只有 93.1%、泰米尔语 90.0%**：25 决策模型 × 17 子类 × 14 语言 × **25,626** 平行条目；**325/325** model–language pair 掉准确率、**301** 个过度自信上升；`ΔAcc −3.5` 而 `ΔConf −1.8`（**置信度只掉一半**）、Gap 均值 **+1.6**；中文 −2.2/−1.0/+1.2/93.1%；语言 **60%** + 底座 **34%** 解释方差、与排行榜名次无关；per-language temperature scaling 500 items 把 pooled ECE **4.1%→2.9%** 但**准确率不回**。⇒ 微调修校准易、修准确率难；英文阈值不得全局下发 (NEW) |",
    "| **What, Who, and When / MindGuard2** | [2611.33263](https://arxiv.org/abs/2611.33263) | 2026 (**Sword Health + Yale + IST**) | 策略可配置护栏 / 层级标签 / tag-weighted / 误杀体感 / 短 CoT | **「判有害」与「怎么处置」拆成两层**：模型只输出 (what, who, when) 三元组，`triplet → safety protocol` 是**权重外临床医生策展、可编辑可审计的决策树**，换策略**不重标注、不重训**；3WS 分维加权，what/who 一致率 **>89%** 而 when 仅 **0.53**（故降权）；short-rollout SFT → RL with reasoning-length penalty，BA 与 GLM-5.3 相当而 median latency 低 **~10×**，发布版 FPR **0.09/0.02/0.03**、R 0.92/0.84/0.87；**推理收益集中在 3W 0.72→0.90 而非 BA 0.81→0.91** ⇒ 细粒度才开 CoT。原文点名 over-flagging 破坏信任 (NEW) |",
]
s = rows_after(s, "| **Measurement Artifacts in Trustworthiness Evaluations of Quantized Small LMs**",
               t2t_rows, "2611.33307")
note_t = "*本次 Survey 更新：2026-11-27（新增 2 篇方法论迁移：2611.33307 跨语言置信度滞后——325/325 pair 掉准确率、英文 95% 阈值中文 93.1% 泰米尔 90.0%、温度缩放修 ECE 不修准确率；2611.33263 策略与权重解耦——what/who/when 三元组 + 权重外可热更新映射表 + 3WS 分维加权 + 短 CoT 低 10× 延迟，`t14_policy_guard` 六周零供给终结；现为 **139** 篇）。*"
if "本次 Survey 更新：2026-11-27" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-26（新增 1 篇方法论迁移",
                  note_t + "\n*上次 Survey 更新：2026-11-26（新增 1 篇方法论迁移", 1)
wr("insights/t2t-survey.md", s)
print("t2t-survey: 139 / +2 rows")

# ---------- 6. benchmark README ----------
b = rd("categories/t2i/benchmark/README.md")
b = b.replace("最后回填: 2026-11-26 | 共 **56** 条", "最后回填: 2026-11-27 | 共 **58** 条")
newrows = [
    "| **T2ISpec（投机解码分层基准）** | [2611.29029](https://arxiv.org/abs/2611.29029) | 2026 arXiv（**密歇根 + 斯坦福 + 宾大 + 俄亥俄州立 + 南洋理工**） | **聚合加速比掩盖 topic 差异**：1,400 prompts × 7 topic × 2 难度、paired Target-only 三列同报；AR 偏离 **±20%**；**ADT-Tree −42.0% work → 仅 1.0889×**；Overall **0.0000** 掩盖 text +0.0233 / commonsense −0.0242；阈值跨难度方向相反 (NEW) |",
    "| **Flow-GRPO Skill-Wise pass@k 解剖** | [2611.33316](https://arxiv.org/abs/2611.33316) | 2026 arXiv（**NCSU + Purdue**） | **把一个奖励增益拆成锐化/解锁**：553 held-out prompts × 32 共享种子；四技能 k*=4–10 且 Δceiling ≤0.013，关系技能 Δceiling **+0.31**、零覆盖 93% 被救、pass@128 0.89 仍低于 RL pass@1 0.94；best-of-4 回收 76% vs 41% ⇒ 锐化可推理侧买、解锁只能训练侧给 (NEW) |",
]
tail = "\n[← 返回文生图目录](../README.md)"
if "2611.29029" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2i/benchmark/README.md", b)

b = rd("categories/t2t/benchmark/README.md")
b = b.replace("最后回填: 2026-11-26 | 共 **34** 条", "最后回填: 2026-11-27 | 共 **35** 条")
newrows = [
    "| **Multilingual Decision Models（跨语言阈值校准基准）** | [2611.33307](https://arxiv.org/abs/2611.33307) | 2026 arXiv（**南洋理工 + NUS + VinUniversity**） | **英文校准的 95% 阈值中文 93.1% / 泰米尔 90.0%**：25 模型 × 17 子类 × 14 语言 × 25,626 平行条目；**325/325** pair 掉准确率、**301** 个过度自信上升，`Gap=ΔConf−ΔAcc` 均值 **+1.6**；per-language 温度缩放 ECE 4.1%→2.9% 而准确率不回 ⇒ 阈值须按语言分格 (NEW) |",
]
tail = "\n[← 返回文生文目录](../README.md)"
if "2611.33307" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2t/benchmark/README.md", b)
print("benchmark: t2i 58 / t2t 35")

# ---------- 7. Landscape ----------
L = rd("insights/AI_Security_Landscape_2026.md")
L = L.replace("基于本项目收录的 **346 篇**", "基于本项目收录的 **352 篇**")
L = L.replace("**更新日期**: 2026-11-26（v3.21 增量更新）", "**更新日期**: 2026-11-27（v3.22 增量更新）")
L = L.replace("### T2T 论文分布（137 篇）", "### T2T 论文分布（139 篇）")
L = L.replace("### T2I 论文分布（169 篇）", "### T2I 论文分布（173 篇）")
L = L.replace(
    "*最近更新：2026-11-26（v3.21 增量更新），累计论文数 **346**（T2T: **137** 篇，T2I: **169** 篇，Agentic Search: **40** 篇）。*",
    "*最近更新：2026-11-27（v3.22 增量更新），累计论文数 **352**（T2T: **139** 篇，T2I: **173** 篇，Agentic Search: **40** 篇）。*")

hot34 = """### 🔥 热点三十四：把「一个增益」拆开 —— RL 涨点、加速比、置信阈值、安全标签全都装错了单位（2026-11-27 新增）

热点三十三把「一个总数」拆成按部件、按栏、按仪器。这一轮六篇再往下一层：**连「涨了多少」本身都被当成了一个数**。

| 论文 | 被当成的一个数 | 拆成的单位 | 实测 |
|---|---|---|---|
| **Flow-GRPO 解剖** | GenEval 0.63→0.95 | 按**技能**分「锐化 / 解锁」 | 四技能 k*=4–10、pass@32 动 ≤0.013、best-of-4 回收 76%；关系技能 Δceiling **+0.31**、零覆盖 93% 被救、**128 个 base 样本仍买不到** |
| **RL = Activation Steering** | RL 的奖励增益 | 按**参数自由度**拆 | 0.29M = LoRA 的 **1/65**、拟合不含奖励，恢复 **90.0–96.3%**；只训向量反超权重 RL 104.6% |
| **PreserveReward** | 一个一致性分 | 按**证据**分三栏 | 局部/全局/意图对齐；奖励器跨集方向反转（GEdit-v1 反不如 Base 而 KRIS 涨） |
| **T2ISpec** | 一个 Overall 加速比 | 按 **topic × 难度**拆 | AR ±20%；**−42.0% work → 1.0889×**；Overall 0.0000 掩盖 +0.0233/−0.0242 |
| **Lost in Translation** | 英文上调的一个 τ | 按**语言**拆 | 325/325 pair 掉准确率、301 过度自信上升；中文 **93.1%**、泰米尔 **90.0%**；ECE 可修而准确率不回 |
| **What/Who/When** | 一个 unsafe 标签 | 按 **what/who/when** 三轴 + 判定/处置两层 | 权重外映射表可热更新；when 轴一致率 0.53 vs what/who >89% |

**由此提炼四条新纪律**：① **「安全率上涨 ≠ 改写策略变强」获得独立双证据**——一个从样本覆盖（锐化/解锁）、一个从参数自由度（常数向量恢复 90%+）。动训练前必须报 `k*`、Δceiling、零覆盖拯救率、常数臂解释率；锐化就把预算转 best-of-k + verifier，解锁才动训练配比。② **阈值有适用范围**——英文校准的 τ 在中文只有 93.1%，且语言 60% + 底座 34% 解释全部准确率损失方差、与排行榜名次无关；per-category threshold 之前要补「语言 × 难度」体检，且**校准合格 ≠ 安全合格**。③ **奖励器 / 阈值 / 加速比都属「验收装置」，须先被验收**——PreserveReward Table 2 给出同一 reward 跨评测集方向反转的公开实例。④ **策略与权重解耦让「能改则不拒」有了承载层**——`t14_policy_guard` 连续六周零可迁移后首次实质命中，换处置策略不重训、不重标注，5.2% / 3.42% 双约束可在不改模型的前提下按类目灰度调。

**输入改写有效性上界归因补第六栏「GRPO 增益机制」**：3,000 条 case 的五栏（文本仍有害 / 生成过程改写 / 执行环境漂移 / 表示层残留与代理量 / 改写引入的表示层漂移）之外，若本轮「锐化或常数可解释」占比 >20%，则「改写还不够严」与「继续加 GRPO 训练」**同时作废**。**重心仍不在加严输入改写**：2,700+ 条源于出图侧内生风险，投入留在生成过程干预（A2 六臂，新增局部反事实调制臂并报 safety-adjacent benign 误伤率）与验收单位重构。

**供给侧**：网页端十分类串行全批 **4338 篇**（2056 带摘要），公告批次 11-20→11-26（717/562/1440/844/**775**），复用 1982 条摘要缓存回填 1671、仅新抓 385 篇；主题 **26 路** + 形态 **12 路**本地正则复现、零第二次检索请求。`t2_prompt_rewrite` 严格 3 命中全误（**空窗第 20 周**），但三条长期空窗通道同日补齐：GRPO 奖励解剖 / 跨语言阈值 / 策略可配置护栏 ⇒ 「零命中不得判为供给为零」连续第二周兑现。机构核验 6/6 HTTP 200、HTML affiliation 全空由 PDF 首页 pypdf 回退（**第 14 次连续生效**）；工业界作者机构 **3 篇**（JD.com、IBM Research、Sword Health），被测/被优化主干含阿里 Qwen-Image-2.1。**仍无一篇为头部公司发布的安全改写器技术报告**；I2I 安全改写方法 / 统一生成-编辑改写面 / NSFW 图审 SFT / i2v-t2v 生成安全本轮零供给。

"""
if "热点三十四" not in L:
    L = L.replace("### 🔥 热点三十三：", hot34 + "### 🔥 热点三十三：", 1)

v322 = """*本次 v3.22 更新：新增 4 篇 T2I/T+I2I（2611.33316 Flow-GRPO 按技能 pass@k 把 0.63→0.95 拆成四锐化一解锁、关系技能 Δceiling +0.31 且 128 个 base 样本仍买不到；2611.26627 常数 steering vectors 0.29M 参数 = LoRA 1/65、拟合不含奖励恢复 90.0–96.3% RL 增益、只训向量反超权重 RL 104.6%；2611.34446 PreserveReward 双教师 OPSD + minimum-KL 校准 + 梯度路由双负跳过，JD.com 主干 Qwen-Image-2.1，84.70% 人类偏好对齐，且 Table 2 证明三个 reward model 做 RL 后 GEdit-v1 反不如 Base 而 KRIS 涨；2611.29029 T2ISpec −42.0% work 只换 1.0889×、Overall 0.0000 掩盖 text +0.0233 / commonsense −0.0242、阈值跨难度方向相反）与 2 篇方法论迁移（2611.33307 跨语言置信度滞后，325/325 pair 掉准确率、英文 95% 阈值中文 93.1% 泰米尔 90.0%、温度缩放修 ECE 4.1%→2.9% 而准确率不回；2611.33263 what/who/when 三元组 + 权重外可热更新策略映射 + 3WS 分维加权 + 短 CoT 低 10× 延迟、FPR 0.02–0.09，`t14_policy_guard` 六周零供给终结），并新增一条范式信号（热点三十四）：**把「一个增益」拆开**。「安全率上涨 ≠ 策略变强」获两条独立证据；D2 启动训练前必须先过 `k*` / Δceiling / 常数臂解释率零训练闸门；动训练之前先修尺子（奖励器跨集方向、阈值语言与难度适用范围、judge 配置指纹）。输入改写优化预算继续冻结，投入留在出图侧生成过程干预与验收单位重构。*
"""
if "v3.22 更新" not in L:
    L = L.replace("*本次 v3.21 更新：", v322 + "*本次 v3.21 更新：", 1)
wr("insights/AI_Security_Landscape_2026.md", L)
print("Landscape: v3.22 / 352 / 热点三十四")

print("=== SYNC DONE ===")
