# Modifier Unlocked: Jailbreaking Text-to-Image Models Through Prompts

## 📄 论文信息

| 属性 | 内容 |
|------|------|
| **标题** | Modifier Unlocked: Jailbreaking Text-to-Image Models Through Prompts |
| **年份** | 2025 |
| **会议/期刊** | IEEE S&P 2025 |
| **PDF** | [IEEE Xplore](https://ieeexplore.ieee.org/abstract/document/11023413) |
| **分类** | cs.CR, cs.LG |

---

## 🎯 核心贡献

本文揭示了T2I模型中"修饰符"机制的安全漏洞，提出通过精心设计的提示词来解锁并滥用这些修饰符，从而绕过安全过滤生成有害内容。

### 主要贡献点

1. **修饰符机制分析**: 深入分析T2I模型中修饰符的工作原理
2. **绕过攻击方法**: 利用修饰符解锁机制绕过安全过滤
3. **系统性评估**: 对多种T2I模型和修饰符组合进行测试

---

## 🔧 技术方法

### 修饰符机制

T2I模型使用修饰符来增强或修改生成内容的特定属性：
- 风格修饰符（艺术风格、渲染引擎等）
- 质量修饰符（分辨率、光照等）
- 内容修饰符（场景、对象等）

### 攻击原理

1. **识别可用修饰符**: 发现模型支持的各类修饰符
2. **构造解锁提示**: 将有害内容包装在合法修饰符中
3. **绕过安全过滤**: 利用修饰符的优先级绕过内容过滤

---

## 📚 引用信息

```bibtex
@inproceedings{modifier2025,
  title={Modifier Unlocked: Jailbreaking Text-to-Image Models Through Prompts},
  booktitle={IEEE Symposium on Security and Privacy (Oakland)},
  year={2025}
}
```

---

[← 返回攻击类目录](../attack/README.md) | [← 返回主目录](../../README.md)
