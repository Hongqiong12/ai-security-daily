#!/usr/bin/env python3
"""2026-11-26 门面同步（幂等）：写入本轮 6 篇 + 刷新全部计数锚点。

覆盖：selected_papers.json / _meta.json / README（徽章+今日区块+洞察表+三模态索引）/
两份 Survey（头部+表格行+更新注记）/ 两份 benchmark README（t2i 54→56 / t2t 33→34）/
Landscape（v3.21 + 热点三十三）。

重复执行不会产生重复行：每处按唯一 ID 或唯一串做存在性检查。
"""
import json, re, os

ROOT = "/Users/ageisliu/WorkBuddy/Claw/ai-security-daily"
os.chdir(ROOT)

TODAY = "2026-11-26"
COUNTS = {"t2t": 137, "t2i": 169, "agentic": 40, "total": 346}
MISSING = ["2026-11-%02d" % d for d in range(11, 23)]
IDS = ["2611.31048", "2611.31774", "2611.32407", "2611.27388",
       "2611.30523", "2611.32848"]
SLUG = {
    "2611.31048": "2611.31048_hint_distill_correction_not_rewrite",
    "2611.31774": "2611.31774_bodybench_nudification_defense_audit",
    "2611.32407": "2611.32407_tide_per_instruction_token_budget",
    "2611.27388": "2611.27388_crie_redundant_instruction_final_intent",
    "2611.30523": "2611.30523_veriorigin_watermark_edit_survival",
    "2611.32848": "2611.32848_quantized_eval_instrument_artifacts",
}


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


# ---------- 1. selected_papers.json 114 → 120 ----------
sel = json.load(open("selected_papers.json", encoding="utf-8"))
have = {x["id"].split("v")[0] for x in sel}
pool = json.load(open("/tmp/full_1126.json", encoding="utf-8"))
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
        "t2t-survey": {"date": TODAY, "count": 137},
        "t2i-survey": {"date": TODAY, "count": 169},
        "agentic-search-survey": {"date": "2026-10-30", "version": "v1.9", "count": 40},
        "landscape_2026": {"date": TODAY, "version": "v3.21", "total_papers": 346},
    },
    "benchmark_status": {
        "t2t_benchmark": {"entries": 34, "last_updated": TODAY},
        "t2i_benchmark": {"entries": 56, "last_updated": TODAY},
        "agentic_benchmark": {"entries": 10, "last_updated": "2026-04-30"},
    },
    "daily_reports": {
        "latest": TODAY,
        "this_month_count": 12,
        "missing_dates": MISSING,
    },
    "workflow_version": "2.3",
    "today_selection": {
        "t2i": [SLUG["2611.31048"], SLUG["2611.31774"], SLUG["2611.32407"],
                SLUG["2611.27388"], SLUG["2611.30523"]],
        "t2t_migration": [SLUG["2611.32848"]],
        "theme": "判定的单位错了 —— 六篇把「一个总数」拆成按部件、按栏、按仪器；HinT 首次给出外科式替换风险锚点在表示层不成立的机制级证据",
    },
    "_note": "This file is the single source of truth for all paper counts. Automation must update this file on every run. Never estimate counts — always use search_file to scan papers/ directories.",
}
wr("_meta.json", json.dumps(meta, ensure_ascii=False, indent=2) + "\n")
print("_meta.json: 346 / month_count 12 / missing_dates", len(MISSING))

# ---------- 3. README ----------
r = rd("README.md")
r = r.replace("Papers-340-green.svg", "Papers-346-green.svg")
r = r.replace("Last-Update-2026--11--25-orange.svg", "Last-Update-2026--11--26-orange.svg")
r = r.replace("基于 **340** 篇安全论文萃取的全局视野", "基于 **346** 篇安全论文萃取的全局视野")

TODAY_BLOCK = """## 🔥 今日最具业务价值论文评测 (2026-11-26)

> **今天六篇把「判安全」这件事从「一个总数」拆成按部件、按栏、按仪器。最扎的一刀来自快手可灵：单 slot 的「外科式替换风险锚点」会被文本编码器扩散到全句，59%–74% 的改写还擅自加了场景和光照。**
>
> **✅ 供给侧**：网页端十分类 `/list/<cat>/recent?show=2000` 串行全批扫描，公告批次 **11-19→11-25**（740/718/563/1442/**845**）；全批池 **4308 篇**（1982 篇带摘要），复用昨日 1871 条摘要缓存回填 1566、仅新抓 **416** 篇，主题词 **26 路** + 形态 **12 路**全部本地正则复现、零第二次检索请求。`t2_prompt_rewrite` 严格词表 3 命中**全为误命中**（空窗第 **19** 周），但 ② 全批扫描 + ④ 厂商兜底「捡」出本轮头条 HinT —— **零命中不等于供给为零**最有力的一次验证。
>
> **🎯 头部公司首次命中 2 篇**：**KlingAI Research（快手可灵）** 的 HinT、**Adobe Inc.** 的 TIDE；另有阿里 Qwen-Image-2512 / Qwen-Image-2.1 / Qwen-Image-Edit-2511 作为被测主干出现在 3 篇里。**T2I 占比 83.3%，历史最高。**
>
> **⚠️ 仍零供给**：I2I 安全改写方法 / 统一生成-编辑改写面 / GRPO 安全改写 / 跨语言安全改写 / 风险知识召回护栏（`t14_policy_guard` 5 命中全 RAG、0 可迁移，「有量不等于有供给」**第六次**）/ i2v-t2v 生成安全（主线⑥不给建议）。

| 核心威胁领域 | 🚨 今日优先论文 | 一句话快评 | 深度拆解 |
|---|---|---|---|
| **外科式替换在表示层不成立** | [HinT：蒸馏修正而非改写](./categories/t2i/papers/2611.31048_hint_distill_correction_not_rewrite.md) | **KlingAI Research 快手可灵 + 复旦 + 华南师大 + 浙大**（主干 Qwen-Image-2512 / SD3.5-M / FLUX.2-klein）。critic 把 **10 词 → 22–25 词**，**59%–74%** 修订加了未要求的场景/光照；**单 slot 编辑经文本编码器传播到全句**；改写习惯 **2.2%→98–100%（2 轮内）**而 HinT **<4%**；twin 速度差使 GenEval2 EMA **+11.4/+11.1/+1.9**，比标量奖励 RL 高 **21.6 点**，训练 **+<4%**、推理零开销。⇒ 输入改写有效性上界补第五栏「表示层漂移」，但**修法是换监督单位，不是加严改写**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **防护成功率几乎全是假的** | [BODYBENCH](./categories/t2i/papers/2611.31774_bodybench_nudification_defense_audit.md) | **密歇根 + 普林斯顿**（11-25 新批次）。648 合成主体 × 11 掩码；三种 harm-aligned 判据（性化/自然度/可辨认性）替代 PSNR。四种防护仅 **AdvPaint 一个配置**达 DefenseScore **0.951** 且要求掩码**精确对齐**；dilation d=7 掉 **0.739**，d=15/31 全崩；**PSNR/SSIM 与裸体化防护基本不相关**。⇒ 「掩码精确对齐」在结构上等价于评测集重叠；图审 AB 必须补三栏判据 + 扰动格。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **一个阈值先杀掉最细的编辑** | [TIDE：每部件自己的预算](./categories/t2i/papers/2611.32407_tide_per_instruction_token_budget.md) | **IIT Delhi + Adobe Inc.**（主干 Qwen-Image-Edit-2511）。**Theorem 2 证明 part-agnostic 规则无法保证异构预算**；单一全局阈值在 **89%** 的 MICE-Bench 图上破坏至少一个编辑；per-part 少丢 **48%/最高 77%** 且 **2.09×→2.20× 更快**。⇒ 「改写强度分级下沉」第一次有可证伪定理与「分档不牺牲延迟」实测；I2I 0/0% 的**第八种**归因。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **完整成功率 0.0% 是判据坏了** | [CRIE-Agent / CRIE-S](./categories/t2i/papers/2611.27388_crie_redundant_instruction_final_intent.md) | **中山大学**（主干 Qwen-Image-2.1 / FLUX.2-klein-4B）。10,000 条冗余/撤销编辑指令；五个后端直接编辑 O. 54–58 / A. 69–84 / R. 57–70 而**完整成功全部 0.0%**；CRIE-Agent 折叠成最终编辑目标 + 从源图重执行，抬到 **27.5–50.0%**。⇒ 0/0% 的**第九种**归因：验收判据没有可判的正例；报「方向覆盖数」而非 0/1。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **编辑后水印存活率有基线了** | [VeriOrigin](./categories/t2i/papers/2611.30523_veriorigin_watermark_edit_survival.md) | **北理工 + 澳门理工 + 深北理莫斯科 + 宁大 + 深大 + 中关村实验室**（兑现 11-25 优先精读）。XOnet 可逆 CNN + 两阶段训练；clean 定位 F1 **0.995**、JPEG70 payload **0.949**、Gaussian σ23 **0.998**、resize 0.35 **0.999**，载荷代价 ≤**2.3 F1 点**，无损通道 **bit-exact 恢复**。⇒ 判定 / 信息 / 事件三栏做进同一框架；属**输出凭证层**，不阻止风险内容生成。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |
| **安全率下降有一半是尺子写的** | [Measurement Artifacts](./categories/t2t/papers/2611.32848_quantized_eval_instrument_artifacts.md) | **COMSATS + Middlesex**（迁移）。$\\Delta_{measured}=\\Delta_{true}+\\Delta_{inst}$：与量化交互的仪器误差能**造出或反转**效应。基线拒答检测器只召回 **33.3%** 的拒答（corrected **80.0%**）；人工校准后 4-bit harmful compliance **+2.6 点**而检测器记的 refusal 降 **4.7 点**；同一模型四种评分给 **+9.8/+0.8/−13.6/−7.3**；**LLM.int8() 非 batch-invariant**（重排 batch 改变答案数达量化本身的 **57–119%**）。⇒ 与 overlap 下界、评测集重叠并列的**第三种读数污染**。 | [📄 立即阅读](./daily-reports/2026-11/2026-11-26_AI安全每日深度情报.md) |

⏱ **今日一句话**：**别再调那个总数了**。先把「五栏归因（含改写表示层漂移）、三栏图审判据、按部件/方向覆盖数的分流输出、检测器人工校准、生成侧+判定侧 serving setup 指纹」补进验收；输入改写优化预算继续冻结，重心留在出图侧生成过程干预与验收单位重构。
"""
start = r.find("## 🔥 今日最具业务价值论文评测 (")
end = r.find("\n---\n\n## 🔭 前沿 Survey", start)
if start != -1 and end != -1:
    r = r[:start] + TODAY_BLOCK + r[end:]

insight = {
    "| 🏆": "| 🏆 **[2026 AI 大模型安全前沿洞察](./insights/AI_Security_Landscape_2026.md)** | **判定的单位错了（热点三十三）**（NEW） · **按部件/按栏/按仪器拆开一个总数**（NEW） · **头部公司首次命中 2 篇：快手可灵 + Adobe**（NEW） | 2026-11-26 |",
    "| 🛡️": "| 🛡️ **[T2T LLM 安全全局图谱](./insights/t2t-survey.md)** | **量化后安全率下降有一半是尺子写的**（NEW） · **拒答检测器只召回 33.3% 的拒答**（NEW） · **第三种读数污染：测量仪器交互可造出/反转效应**（NEW） | 2026-11-26 |",
    "| 🖼️": "| 🖼️ **[T2I 文生图安全七年演进](./insights/t2i-survey.md)** | **HinT：单 slot 外科替换扩散到全句、改写 59–74% 加未要求场景**（NEW） · **BODYBENCH：掩码精确对齐才 0.951**（NEW） · **TIDE Theorem 2 分级是数学必要**（NEW） · **CRIE-S 完整成功 0.0%**（NEW） | 2026-11-26 |",
}
lines = r.split("\n")
for i, ln in enumerate(lines):
    for k, v in insight.items():
        if ln.startswith(k):
            lines[i] = v
            break
r = "\n".join(lines)

IDX = [
    ("- **Defense (安全加固):**", "GuideCache",
     "[HinT 蒸馏修正而非改写](./categories/t2i/papers/2611.31048_hint_distill_correction_not_rewrite.md) (单 slot 扩散到全句 / 改写习惯 2.2%→98% 而 HinT <4% / KlingAI) | "
     "[TIDE 每部件预算](./categories/t2i/papers/2611.32407_tide_per_instruction_token_budget.md) (Theorem 2 / 89% 破坏预算 / 2.09×→2.20× / Adobe) | "
     "[VeriOrigin 编辑后水印](./categories/t2i/papers/2611.30523_veriorigin_watermark_edit_survival.md) (JPEG70 0.949 / 定位 F1 0.995 / bit-exact 恢复)",
     "2611.31048", "t2i"),
    ("- **Benchmark:**", "SAE-Audit",
     "[BODYBENCH 裸体化防护审计](./categories/t2i/papers/2611.31774_bodybench_nudification_defense_audit.md) (0.951 仅在掩码精确对齐 / PSNR 不相关 / 三栏判据) | "
     "[CRIE-S 冗余指令编辑](./categories/t2i/papers/2611.27388_crie_redundant_instruction_final_intent.md) (完整成功 0.0%→27.5–50.0% / 10,000 条)",
     "2611.31774", "t2i"),
    ("- **Benchmark:**", "Latent Safety Filter",
     "[Measurement Artifacts 量化评测仪器项](./categories/t2t/papers/2611.32848_quantized_eval_instrument_artifacts.md) (检测器召回 33.3%→80.0% / +2.6 vs 4.7 点 / 8-bit 非 batch-invariant)",
     "2611.32848", "t2t"),
]
for st, disc, payload, marker, mod in IDX:
    # 用「模态专属判别词」避免 t2i/t2t 同名 bullet 串台
    hits = [ln for ln in r.split("\n") if ln.startswith(st) and disc in ln]
    if not hits:
        raise RuntimeError("bullet not found: " + st + " / " + disc)
    # 找到目标 bullet 所在行（按 disc 唯一），再加插入
    target_line = hits[0]
    if marker in target_line:
        continue
    out, done = [], False
    for ln in r.split("\n"):
        if not done and ln == target_line:
            head, sep, rest = ln.partition("** ")
            if not sep:
                head, sep, rest = ln.partition(": ")
            ln = head + sep + payload + " | " + rest
            done = True
        out.append(ln)
    r = "\n".join(out)

wr("README.md", r)
print("README: badge 346 / date 11-26 / 今日区块 / 洞察表 / 索引 6 篇")

# ---------- 4. t2i-survey ----------
s = rd("insights/t2i-survey.md")
s = s.replace("本项目收录的 **164** 篇 T2I 安全论文", "本项目收录的 **169** 篇 T2I 安全论文")
s = s.replace("**更新日期**: 2026-11-25", "**更新日期**: 2026-11-26")
t2i_rows = [
 " | **HinT / Distill the Correction, Not the Rewrite** | [2611.31048](https://arxiv.org/abs/2611.31048) | 2026 (**KlingAI Research 快手可灵 + 复旦 + 华南师大 + 浙大**；主干 Qwen-Image-2512 / SD3.5-M / FLUX.2-klein) | **「外科式替换风险锚点」在表示层不成立**：critic 把 10 词中位 prompt 扩成 **22–25 词**、**59%–74%** 修订加了未要求的场景/光照；**单 slot 编辑经文本编码器传播到全句 token**；1,146 条 re-noised 失败样本的速度分解显示整句改写更新方向与 $\\Delta_{drift}$ 对齐。Hindsight Twins 用同一 slotted 模板填「修复 / 观测错误」两版、只蒸馏速度差并对齐槽位外 token states；sunset 习惯基线 **2.2%→98–100%（2 轮内）**而 HinT **<4%**；GenEval2 EMA **+11.4/+11.1/+1.9**、Tab.3 **49.0(+17.2)**、比标量奖励 DiffusionNFT 高 **21.6 点**、训练 **+<4%** / 推理零开销。⇒ 输入改写有效性上界补第五栏「改写引入的表示层漂移」，修法是换监督单位而非加严改写 (NEW) |",
 " | **BODYBENCH / Nudification Defense Audit** | [2611.31774](https://arxiv.org/abs/2611.31774) | 2026 (**密歇根大学 + 普林斯顿大学**) | **防护成功率读数几乎全是假的**：648 全合成着衣成年主体 × 11 掩码 = 7,128 张；三 harm-aligned 指标 sexualization / naturalness / recognizability（三者都低才算成功，`DefenseScore=1−S/2`）替代 PSNR/SSIM。审计 PhotoGuard / DiffusionGuard / AdvPaint / DiffVax：**仅 AdvPaint body 在掩码精确对齐时达 0.951**，body+context → **0.385**、dilation d=7 → **0.739**、BBox → **0.384**；PhotoGuard/DiffusionGuard 最好 0.403/0.420；DiffVax 0.725 但产生可见噪声（OOD + 无界扰动）。**PSNR/SSIM 与裸体化防护基本不相关**；多数方法 R 降到 0.09–0.24 而 S 仍 ≥1.0 ⇒ 图里仍被换成裸体。⇒ 掩码精确对齐在结构上等价于评测集重叠 (NEW) |",
 " | **TIDE / Every Edit Its Own Budget** | [2611.32407](https://arxiv.org/abs/2611.32407) | 2026 (**IIT Delhi + Adobe Inc.**；主干 FLUX.2 Klein / **Qwen-Image-Edit-2511**) | **分级下沉第一次有可证伪定理**：**Theorem 1** 全局阈值必然先破坏 drift 最小部件、**Theorem 2** part-agnostic 规则**无法保证**异构 per-part 预算、**Theorem 3** 非平衡最优传输保住 argmax 丢掉的弱部件；诊断「token 的 drift 不 reveal 它服务于哪个 edit」。单一全局阈值在 **89%** 的 MICE-Bench 图上破坏至少一个编辑；per-part 在 matched speed 少丢 **48%（384→200）/ 最高 77%** 且 **2.09×→2.20× 更快**，六个 benchmark 全最快（2.20–2.24×）；LPIPS 0.291 vs 0.320、报 seed noise floor。⇒ 改写强度分级不是调参偏好而是数学必要；I2I 0/0% 第八种归因 (NEW) |",
 " | **CRIE-Agent / CRIE-S** | [2611.27388](https://arxiv.org/abs/2611.27388) | 2026 (**中山大学**；主干 Qwen-Image-Edit 2511 / **Qwen-Image-2.1** / FLUX.2-klein-4B) | **0.0% 是判据无分辨率，不是模型全坏**：10,000 条带精确最终意图标注的冗余/撤销编辑指令；三个后端直接编辑 O. 54–58 / A. 69–84 / R. 57–70，而**完整成功 S. 全部 0.0%**（既有编辑 agent 0–1.0%）。Qwen3-VL-8B Intent Agent 把修订历史折叠成 object-level final intent + reference-first blocks（$k=2$）+ 验证引导**从源图完整重执行**，把完整成功抬到 **27.5–50.0%**（Qwen-Image-2.1 50.0% / FLUX.2 27.5%）。⇒ 整体-分层背离的镜像；I2I 0/0% 第九种归因，报「方向覆盖数」而非 0/1 (NEW) |",
 " | **VeriOrigin / 主动图像保护** | [2611.30523](https://arxiv.org/abs/2611.30523) | 2026 (**北理工 + 澳门理工 + 深北理莫斯科 + 宁大 + 深大 + 中关村实验室**) | **编辑后水印存活率有了分档公开基线**：XOnet（Xnet/Onet cross residual prediction 可逆 CNN）+ 两阶段训练（水印分支→篡改定位分支）；clean 定位 F1/IoU **0.995/0.990**（CocoGlide）/ **0.995/0.991**（COVERAGE）/ 0.974/0.950（CASIA v2.0），优于 GenPTW 0.961/0.954、EditGuard 0.899/0.947；TGIF2 JPEG QF90 **0.960/0.929** → QF70 0.869/0.793；**Table 4 payload 位准确率** tampered **1.000** / JPEG70 **0.949** / noise σ23 0.998 / resize 0.35 0.999；`w/o wm` 对照显示载荷代价 ≤**2.3 F1 点**；无损通道 **bit-exact 恢复**。⇒ 判定/信息/事件三栏统一，属输出凭证层 (NEW) |",
]
t2i_rows = [x.lstrip() for x in t2i_rows]
s = rows_after(s, "| **HOSE / Hierarchical Orthogonal Subspace Erasure**", t2i_rows, "2611.31048")
note = "*本次 Survey 更新：2026-11-26（新增 5 篇 T2I/T+I2I：2611.31048 HinT 单 slot 外科替换扩散到全句 / 改写 59–74% 加未要求场景 / twin 速度差；2611.31774 BODYBENCH 掩码精确对齐才 0.951 且 PSNR 不相关；2611.32407 TIDE Theorem 2 分级是数学必要 / 89% 破坏预算 / 分档更快；2611.27388 CRIE-S 完整成功 0.0%→27.5–50.0%；2611.30523 VeriOrigin 编辑后水印三栏 + bit-exact 恢复；现为 **169** 篇）。*"
if "本次 Survey 更新：2026-11-26" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-25（新增 4 篇：2611.25382",
                  note + "\n*上次 Survey 更新：2026-11-25（新增 4 篇：2611.25382", 1)
wr("insights/t2i-survey.md", s)
print("t2i-survey: 169 / +5 rows / 更新注记")

# ---------- 5. t2t-survey ----------
s = rd("insights/t2t-survey.md")
s = s.replace("本项目收录的 **136** 篇 T2T 安全论文", "本项目收录的 **137** 篇 T2T 安全论文")
s = s.replace("**更新日期**: 2026-11-25", "**更新日期**: 2026-11-26")
t2t_rows = [
 "| **Measurement Artifacts in Trustworthiness Evaluations of Quantized Small LMs** | [2611.32848](https://arxiv.org/abs/2611.32848) | 2026 (**COMSATS University Islamabad + Middlesex University London**) | 量化不劣化验收 / 误杀率读数审计 / 判定装置校准 | **量化后「安全率下降」有一半是尺子写的**：$\\Delta_{measured}=\\Delta_{true}+\\Delta_{inst}$，与量化交互的仪器误差能**造出或反转**效应。8 个 135M–1.7B 模型 × float16/LLM.int8()/NF4 配对；两名标注者 100 条（κ=0.380/0.425）下 baseline keyword detector 只召回 **33.3%** 的拒答（印刷体撇号 / 长前言两种失败模式），corrected **80.0%/80.0%**；人工校准后 4-bit harmful compliance **+2.6 点**（WildGuard +3.0）而 detector 记的 refusal 降 **4.7 点**；2,000 条 HaluEval 上同一模型同一精度四种评分给 **+9.8/+0.8/−13.6/−7.3**、cloze vs lettered **ρ=0.10**（天花板 ≈0.77）；NF4 在 **8/8** 模型改首选位置率（最多 +59.5 点）；**LLM.int8() 确定性但非 batch-invariant**（重排 batch 改变答案数达量化本身的 **57–119%**、仅 padding 就改答案），NF4 batch-invariant。⇒ 与 overlap 下界、评测集重叠并列的**第三种读数污染**；顺序固定「审计评测集→体检表示→**体检尺子**→约束式选点」 (NEW) |",
]
s = rows_after(s, "| **Contamination at the Operating Point**", t2t_rows, "2611.32848")
note_t = "*本次 Survey 更新：2026-11-26（新增 1 篇方法论迁移：2611.32848 量化评测的仪器交互项 / 拒答检测器召回 33.3%→80.0% / 8-bit 非 batch-invariant，作为量化不劣化验收与误杀率读数审计协议；现为 **137** 篇）。*"
if "本次 Survey 更新：2026-11-26" not in s:
    s = s.replace("*本次 Survey 更新：2026-11-25（新增 2 篇方法论迁移：2611.23685",
                  note_t + "\n*上次 Survey 更新：2026-11-25（新增 2 篇方法论迁移：2611.23685", 1)
wr("insights/t2t-survey.md", s)
print("t2t-survey: 137 / +1 row / 更新注记")

# ---------- 6. benchmark README ----------
b = rd("categories/t2i/benchmark/README.md")
b = b.replace("最后回填: 2026-11-25 | 共 **54** 条", "最后回填: 2026-11-26 | 共 **56** 条")
newrows = [
 "| **BODYBENCH（AI 裸体化 inpainting 防护评测）** | [2611.31774](https://arxiv.org/abs/2611.31774) | 2026 arXiv（**密歇根 + 普林斯顿**） | **问题定义失败**：648 合成主体 × 11 掩码，性化/自然度/可辨认性三栏判据替代 PSNR；四防护仅 1 配置达 **0.951** 且需掩码精确对齐，dilation d=7 掉 **0.739**；PSNR/SSIM 与防护基本不相关 (NEW) |",
 "| **CRIE-S（复杂冗余指令编辑评测）** | [2611.27388](https://arxiv.org/abs/2611.27388) | 2026 arXiv（**中山大学**） | **完整成功率 0.0% 是判据无分辨率**：10,000 条带精确最终意图标注；O./A./R. 54–84 而 S.=0.0，折叠意图 + 从源图重执行后 **27.5–50.0%** ⇒ 报方向覆盖数而非 0/1 (NEW) |",
]
tail = "\n[← 返回文生图目录](../README.md)"
if "2611.31774" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2i/benchmark/README.md", b)

b = rd("categories/t2t/benchmark/README.md")
b = b.replace("最后回填: 2026-11-25 | 共 **33** 条", "最后回填: 2026-11-26 | 共 **34** 条")
newrows = [
 "| **Measurement Artifacts（量化评测仪器项审计）** | [2611.32848](https://arxiv.org/abs/2611.32848) | 2026 arXiv（**COMSATS + Middlesex**） | **与量化交互的仪器误差能造出/反转效应**：拒答检测器召回 **33.3%→80.0%**；人工校准 4-bit harmful compliance **+2.6 点** vs detector 记 4.7 点；四种评分协议 **ρ=0.10**（天花板 0.77）；**LLM.int8() 非 batch-invariant**（57–119%）⇒ 量化不劣化验收协议 (NEW) |",
]
tail = "\n[← 返回文生文目录](../README.md)"
if "2611.32848" not in b:
    b = b.replace(tail, "\n" + "\n".join(newrows) + tail, 1)
wr("categories/t2t/benchmark/README.md", b)
print("benchmark: t2i 56 / t2t 34")

# ---------- 7. Landscape ----------
L = rd("insights/AI_Security_Landscape_2026.md")
L = L.replace("基于本项目收录的 **340 篇**", "基于本项目收录的 **346 篇**")
L = L.replace("**更新日期**: 2026-11-25（v3.20 增量更新）", "**更新日期**: 2026-11-26（v3.21 增量更新）")
L = L.replace("### T2T 论文分布（136 篇）", "### T2T 论文分布（137 篇）")
L = L.replace("### T2I 论文分布（164 篇）", "### T2I 论文分布（169 篇）")
L = L.replace(
    "*最近更新：2026-11-25（v3.20 增量更新），累计论文数 **340**（T2T: **136** 篇，T2I: **164** 篇，Agentic Search: **40** 篇）。*",
    "*最近更新：2026-11-26（v3.21 增量更新），累计论文数 **346**（T2T: **137** 篇，T2I: **169** 篇，Agentic Search: **40** 篇）。*")

hot33 = """### 🔥 热点三十三：判定的单位错了 —— 把「一个总数」拆成按部件、按栏、按仪器（2026-11-26 新增）

热点三十二把「出图侧」拆成四条机制。这一轮六篇再往下一层：**连「用一个数判安全」这个动作本身都装错了单位**。

| 论文 | 被换掉的单位 | 换成的单位 | 实测 |
|---|---|---|---|
| **HinT** | 整句 rewrite 后的文本 | 同一 slotted 模板下「修复/观测错误」两 twin 的**速度差** + 槽位外 token states 对齐 | critic **59%–74%** 修订加未要求场景；**单 slot 编辑扩散到全句**；改写习惯 **2.2%→98–100%** 而 HinT **<4%**；比标量奖励 RL 高 **21.6 点** |
| **BODYBENCH** | PSNR/SSIM 单一像素代理量 | **性化 × 自然度 × 可辨认性**三栏 | 四防护仅 **1 配置**达 0.951 且需掩码精确对齐，dilation d=7 → **0.739**；PSNR 与防护不相关 |
| **TIDE** | 全图一个跳过阈值 | **每个指令部件自己的 compute budget** | **Theorem 2**：part-agnostic 规则无法保证异构预算；89% 破坏至少一个部件；per-part 少丢 **48%/77%** 且 **更快 2.09×→2.20×** |
| **CRIE-S** | 0/1 完整成功 | **最终编辑目标 + 四要件方向覆盖数** | 五后端完整成功**全 0.0%** 而单维 54–84；折叠意图后 **27.5–50.0%** |
| **VeriOrigin** | 单一水印判定 | **判定 / 信息（定位 F1）/ 事件（bit-exact 恢复）**三栏 | JPEG70 payload **0.949** / clean F1 **0.995** / 载荷代价 ≤**2.3 F1** |
| **Measurement Artifacts** | 基准分的变化 | **真实变化 + 仪器交互项** | 检测器召回 **33.3%→80.0%**；+2.6 vs 4.7 点；四种评分 +9.8/+0.8/−13.6/−7.3；8-bit 非 batch-invariant（57–119%） |

**由此提炼三条新纪律**：① **「外科式替换风险锚点」在表示层不成立**——HinT 首次给出机制级证据（单 slot 编辑经注意力传播到全句、整句改写必然引入未要求场景），因此 3,000 条 case 的归因在 11-25 四栏之外补**第五栏「改写引入的表示层漂移」**；但修法是**换监督单位**（twin 速度差 / 槽位外表示对齐），**不是回退去加严输入改写**。② **分级下沉从工程偏好升级为架构要求**——TIDE Theorem 2 证明 part-agnostic 规则无法保证异构预算，BODYBENCH 与 VeriOrigin 证明判定/信息/事件必须分栏；「per-category threshold tuning / 分级处置」不再是可选项。③ **误杀率有三种读数污染，顺序固定**：评测集重叠（乘性）→ 表示 overlap（结构性下界）→ **测量仪器交互（可造出/反转效应）**；「审计评测集 → 体检表示 → 体检尺子 → 约束式选点」四步不可跳步。

**I2I 0/0% 新增两种可证伪归因**：第八种——**单一全局判定粒度**（TIDE Theorem 2，89% 破坏至少一个部件预算）；第九种——**验收判据没有可判的正例**（CRIE-S 五后端完整成功全 0.0%）。二者都零训练可检验：先按指令部件数 $K$ 分档报命中率，再把分流输出从 0/1 改成带分数的多候选排序 + 四要件方向覆盖数（贴 70% 灰度现状，不重训）。

**权重侧/输入侧边界第十三轮**：四层通路升级为**五层**（新增输出凭证层）——输入侧热更新改写 / 权重侧概念擦除 / 生成过程干预 / 输出侧图审与溯源 / **输出凭证层（bit-exact 恢复 + 篡改定位，只证明来源与改动，不阻止生成）**。任一层单独宣称内容安全已解决即判越界。供给侧**头部公司作者机构首次命中 2 篇**（KlingAI Research 快手可灵、Adobe Inc.），另有阿里 Qwen-Image-2512 / Qwen-Image-2.1 / Qwen-Image-Edit-2511 作为被测主干；`t2_prompt_rewrite` 严格词表 3 命中全为误命中（空窗第 **19** 周），但 ② 全批扫描 + ④ 厂商兜底「捡」出本轮头条 HinT ⇒ **「零命中不得判为供给为零」本周最有力的一次验证**。

"""
if "热点三十三" not in L:
    L = L.replace("### 🔥 热点三十二：", hot33 + "### 🔥 热点三十二：", 1)

v321 = """*本次 v3.21 更新：新增 5 篇 T2I/T+I2I 论文（HinT：KlingAI Research 快手可灵，单 slot 外科替换经文本编码器扩散到全句、critic 59%–74% 改写加未要求场景、twin 速度差把改写习惯压到 <4% 而基线 98–100%、比标量奖励 RL 高 21.6 点；BODYBENCH：648 合成主体 × 11 掩码，性化/自然度/可辨认性三栏判据，四防护仅 AdvPaint 掩码精确对齐时 0.951、dilation d=7 掉 0.739、PSNR 与防护不相关；TIDE：IIT Delhi + Adobe，Theorem 2 证明 part-agnostic 规则无法保证异构预算、单一阈值在 89% 图上破坏至少一个编辑、per-part 少丢 48%/77% 且 2.09×→2.20× 更快；CRIE-S：中山大学，10,000 条冗余指令，五后端完整成功全 0.0% 而单维 54–84，折叠意图后 27.5–50.0%；VeriOrigin：XOnet 可逆 CNN，JPEG70 payload 0.949、clean 定位 F1 0.995、载荷代价 ≤2.3 F1 点、无损通道 bit-exact 恢复）与 1 篇方法论迁移（Measurement Artifacts：Δ_measured=Δ_true+Δ_inst，拒答检测器召回 33.3%→80.0%，人工校准 4-bit harmful compliance +2.6 点 vs detector 4.7 点，四种评分协议 ρ=0.10，LLM.int8() 非 batch-invariant 57–119%），并新增一条范式信号（热点三十三）：**判定的单位错了**。供给侧为**供给回暖第三轮**：网页端十分类串行全批 **4308 篇**（1982 篇带摘要），公告批次 11-19→11-25（740/718/563/1442/**845**），复用昨日 1871 条摘要缓存回填 1566、仅新抓 416 篇；主题词 **26 路** + 形态 **12 路**全部本地正则复现、零第二次检索请求；`t2_prompt_rewrite` 严格词表 3 命中全为误命中（空窗第 **19** 周），但全批扫描 + 厂商兜底捡出 HinT ⇒ 零命中≠供给为零最有力验证；I2I 安全改写方法 / 统一生成-编辑改写面 / GRPO 安全改写 / 跨语言安全改写 / 策略护栏混合召回 / i2v-t2v 生成安全本轮全部零供给；`t14_policy_guard` 5 命中全 RAG、逐篇核验 **0 可迁移**（「有量不等于有供给」第六次生效）。机构核验 7/7 HTTP 200、HTML affiliation 全空由 PDF 首页 pypdf 回退（**第 13 次连续生效**）；**头部公司作者机构 2 篇**（快手可灵 / Adobe），T2I 占比 **83.3%** 为历史最高。*
"""
if "v3.21 更新" not in L:
    L = L.replace("*本次 v3.20 更新：", v321 + "*本次 v3.20 更新：", 1)
wr("insights/AI_Security_Landscape_2026.md", L)
print("Landscape: v3.21 / 346 / 热点三十三")
