"""
HunyuanImage 3.0 架构诊断脚本
=============================
运行此脚本获取 TRCE Stage 2 实现所需的层信息

使用方法:
    cd /apdcephfs_gy7/share_304660203/
    python3 diagnose_hunyuan3.py

输出:
    1. 主 transformer 层结构
    2. 第一个 DecoderLayer 的详细参数
    3. MoE 层的结构
    4. generate_image() 的 denoising hook 点
"""

import sys
import torch

# TODO: 替换为实际的模型加载方式
# from hunyuan_image_3 import HunyuanImage3ForCausalMM
# model = HunyuanImage3ForCausalMM.from_pretrained("path/to/model")

print("=" * 70)
print("HunyuanImage 3.0 架构诊断")
print("=" * 70)

def print_structure(name, module, indent=0):
    """递归打印模型结构"""
    prefix = "  " * indent
    module_type = type(module).__name__

    info = f"{prefix}{name}: {module_type}"

    # 尝试获取参数信息
    num_params = sum(p.numel() for p in module.parameters() if p.requires_grad)
    if num_params > 0:
        info += f" ({num_params:,} params)"

    print(info)

    # 递归打印子模块
    for child_name, child_module in module.named_children():
        print_structure(child_name, child_module, indent + 1)


# ============================================================================
# 1. 主模型结构概览
# ============================================================================
print("\n[1] 主模型结构 (model.model)")
print("-" * 70)
try:
    for name, module in model.model.named_children():
        num_params = sum(p.numel() for p in module.parameters())
        print(f"  {name}: {type(module).__name__} ({num_params:,} params)")
except NameError:
    print("  [ERROR] model 未定义，请先加载模型")

# ============================================================================
# 2. wte 详细验证
# ============================================================================
print("\n[2] Word Embedding 层验证")
print("-" * 70)
try:
    wte = model.model.wte
    print(f"  类型: {type(wte).__name__}")
    print(f"  形状: {wte.weight.shape}")
    print(f"  数据类型: {wte.weight.dtype}")
    print(f"  设备: {wte.weight.device}")
    print(f"  vocab_size: {wte.weight.shape[0]}")
    print(f"  hidden_dim: {wte.weight.shape[1]}")
except Exception as e:
    print(f"  [ERROR] {e}")

# ============================================================================
# 3. Transformer Layers 结构
# ============================================================================
print("\n[3] Transformer Layers 结构")
print("-" * 70)
try:
    layers = model.model.layers
    print(f"  层数: {len(layers)}")
    print(f"  层类型: {type(layers).__name__}")

    # 打印第一层详细结构
    if len(layers) > 0:
        print(f"\n  [First Layer: layers.0]")
        first_layer = layers[0]
        for name, module in first_layer.named_children():
            num_params = sum(p.numel() for p in module.parameters())
            print(f"    {name}: {type(module).__name__} ({num_params:,} params)")

            # 递归打印子模块
            for subname, submodule in module.named_children():
                sub_params = sum(p.numel() for p in submodule.parameters())
                print(f"      {subname}: {type(submodule).__name__} ({sub_params:,} params)")

except Exception as e:
    print(f"  [ERROR] {e}")

# ============================================================================
# 4. MoE 层详细结构
# ============================================================================
print("\n[4] MoE (Mixture of Experts) 层详细结构")
print("-" * 70)
try:
    moe_found = False
    for name, module in model.named_modules():
        if 'moe' in name.lower():
            moe_found = True
            print(f"  MoE 模块: {name}")
            print(f"    类型: {type(module).__name__}")

            # 尝试获取 MoE 参数
            for pname, param in module.named_parameters():
                print(f"    {pname}: {param.shape}")

    if not moe_found:
        print("  [INFO] 未找到 MoE 模块，请检查模块名称")

except Exception as e:
    print(f"  [ERROR] {e}")

# ============================================================================
# 5. 第一个 DecoderLayer 完整参数列表
# ============================================================================
print("\n[5] 第一个 DecoderLayer 的完整参数 (layers.0)")
print("-" * 70)
try:
    first_layer = model.model.layers[0]
    for name, param in first_layer.named_parameters():
        print(f"  {name:<50} {str(param.shape):<20} {param.dtype}")
except Exception as e:
    print(f"  [ERROR] {e}")

# ============================================================================
# 6. qkv_proj 参数验证
# ============================================================================
print("\n[6] Self-Attention qkv_proj 参数 (第一个 layer)")
print("-" * 70)
try:
    first_layer = model.model.layers[0]

    # 查找 self_attn
    for name, module in first_layer.named_children():
        if 'attn' in name.lower() or 'self' in name.lower():
            print(f"  注意力模块: {name} ({type(module).__name__})")

            for pname, param in module.named_parameters():
                print(f"    {pname}: {param.shape}")

            # 查找 qkv_proj
            for subname, submodule in module.named_children():
                if 'qkv' in subname.lower():
                    print(f"    [Found qkv_proj]: {subname}")
                    for pname, param in submodule.named_parameters():
                        print(f"      {pname}: {param.shape}")

except Exception as e:
    print(f"  [ERROR] {e}")

# ============================================================================
# 7. ln_f 结构
# ============================================================================
print("\n[7] ln_f (Final LayerNorm)")
print("-" * 70)
try:
    ln_f = model.model.ln_f
    print(f"  类型: {type(ln_f).__name__}")
    for name, param in ln_f.named_parameters():
        print(f"  {name}: {param.shape}")
except Exception as e:
    print(f"  [ERROR] {e}")

# ============================================================================
# 8. 模型总参数量
# ============================================================================
print("\n[8] 模型总参数量统计")
print("-" * 70)
try:
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)

    print(f"  总参数量: {total_params:,} ({total_params/1e9:.2f}B)")
    print(f"  可训练参数量: {trainable_params:,} ({trainable_params/1e9:.2f}B)")
except Exception as e:
    print(f"  [ERROR] {e}")

print("\n" + "=" * 70)
print("诊断完成")
print("=" * 70)
