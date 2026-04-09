import re
from datetime import datetime

date_str = "2026-04-09"

# Update T2T Survey
with open("insights/t2t-survey.md", "r") as f:
    t2t_content = f.read()

t2t_content = re.sub(r'更新日期: \d{4}-\d{2}-\d{2}', f'更新日期: {date_str}', t2t_content)

new_t2t_attack = """### 2.8 跨模态与推理链攻击的新范式 (2026-04-09 新增)

**MirageBackdoor: A Stealthy Attack that Induces Think-Well-Answer-Wrong Reasoning**（[2604.06840](https://arxiv.org/abs/2604.06840)）：
针对 o1 等推理增强模型的后门植入新范式。
- **机制**：在推理过程（思维链）中表现完全正常，避开所有基于过程监控（Process-based Supervision）的安全检测。只在最后提取答案时发生突变，输出有害/错误结果。
- **意义**：揭示了仅对 LLM 中间推理过程进行安全检查的不足，红队测试需要实现“过程-结果”的交叉一致性校验。

"""

t2t_content = t2t_content.replace('### 3.1 提示注入的演进层级', new_t2t_attack + '### 3.1 提示注入的演进层级')

new_t2t_defense = """### 4.10 联邦对齐中的端侧净化 (2026-04-09 新增)

**FedDetox: Robust Federated SLM Alignment via On-Device Data Sanitization**（[2604.06833](https://arxiv.org/abs/2604.06833)）：
- 核心方法：在边缘设备上使用轻量级安全探针清理毒化数据，上传带有 LDP 保护的“本地健康度证明”。服务端结合证明进行自适应的鲁棒聚合。
- 意义：为小型语言模型（SLM）在联邦学习环境下的安全对齐提供了在不破坏用户隐私前提下的净化方案。

"""

t2t_content = t2t_content.replace('### 5.1 综合安全基准', new_t2t_defense + '### 5.1 综合安全基准')

t2t_content = t2t_content.replace('| H-Node Attack | [2603.26045]', '| MirageBackdoor | [2604.06840](https://arxiv.org/abs/2604.06840) | 2026 | 越狱/后门攻击 | Think-Well-Answer-Wrong 后门范式 |\n| H-Node Attack | [2603.26045]')

t2t_content = t2t_content.replace('| Exclusive Unlearning | [2604.06154]', '| FedDetox | [2604.06833](https://arxiv.org/abs/2604.06833) | 2026 | 联邦对齐防御 | 端侧数据净化与鲁棒聚合 |\n| Exclusive Unlearning | [2604.06154]')

with open("insights/t2t-survey.md", "w") as f:
    f.write(t2t_content)


# Update T2I Survey
with open("insights/t2i-survey.md", "r") as f:
    t2i_content = f.read()

t2i_content = re.sub(r'更新日期: \d{4}-\d{2}-\d{2}', f'更新日期: {date_str}', t2i_content)

new_t2i_watermark = """### 5.5 双重鲁棒水印的崛起 (2026-04-09 新增)

**Towards Robust Content Watermarking Against Removal and Forgery Attacks**（[2604.06662](https://arxiv.org/abs/2604.06662)）：
现有水印容易被 JPEG 压缩洗掉（Removal），也容易被重放攻击利用（Forgery）。
- 机制：频域双频段分离注入冗余水印，结合密码学感知哈希绑定生成图像特征。
- 结论：在抵抗移除与防伪造的综合测试中取得了极高鲁棒性，预示水印安全将向密码学与隐写术的深度融合发展。

"""

t2i_content = t2i_content.replace('## 6. 基准评测', new_t2i_watermark + '## 6. 基准评测')

t2i_content = t2i_content.replace('| FRAP | [2408.11706]', '| RobustWatermark | [2604.06662](https://arxiv.org/abs/2604.06662) | 2026 | 双重鲁棒频域水印 |\n| FRAP | [2408.11706]')

with open("insights/t2i-survey.md", "w") as f:
    f.write(t2i_content)


# Update Agentic Search Survey
with open("insights/agentic-search-survey.md", "r") as f:
    ag_content = f.read()

ag_content = re.sub(r'更新日期: \d{4}-\d{2}-\d{2}', f'更新日期: {date_str}', ag_content)

new_ag_trojan = """| SkillTrojan | [2604.06811](https://arxiv.org/abs/2604.06811) | 2026 | 第三方工具文档描述后门注入 | [详情](../categories/agentic-search/papers/2604.06811v1_SkillTrojan.md) |

**SkillTrojan 核心发现**：
向大模型智能体第三方“技能（Tool）”的自然语言文档描述中注入后门指令。该技术不仅能劫持当前任务，还会引发上下文持久污染（Context Poisoning），而传统代码扫描工具对此束手无策，这确立了第三方工具供应链安全的严峻挑战。
"""

ag_content = ag_content.replace('**TraceSafe 核心发现**：', new_ag_trojan + '\n**TraceSafe 核心发现**：')

new_ag_row = "| 4 | 2604.06811 | SkillTrojan: Backdoor Attacks on Skill-Based Agent Systems | 攻击/供应链后门 | 2026-04-09 | [abs](https://arxiv.org/abs/2604.06811) |\n"
ag_content = ag_content.replace('| 3 | 2604.07223', new_ag_row + '| 3 | 2604.07223')
ag_content = ag_content.replace('覆盖论文数**: 2 篇', '覆盖论文数**: 4 篇')

with open("insights/agentic-search-survey.md", "w") as f:
    f.write(ag_content)

print("Updated surveys successfully.")
