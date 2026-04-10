#!/usr/bin/env python3
"""
自动检查生成的SKILL.md是否通过质量标准。
包含女娲原版6项检查 + 仓颉升级5项检查（Harness Engine相关）。

用法:
    python3 quality_check.py <SKILL.md路径>

示例:
    python3 quality_check.py .claude/skills/elon-musk-perspective/SKILL.md
"""

import sys
import re
from pathlib import Path


# ============================================================
# 女娲原版检查项（6项）
# ============================================================

def check_mental_models(content: str) -> tuple[bool, str]:
    """检查心智模型/思维习惯数量（3-7个）"""
    # v3模板用"我看问题的方式"，女娲用"心智模型"
    models = re.findall(r'^###\s+(?:模型|Model|心智模型)\s*\d', content, re.MULTILINE)
    if not models:
        in_section = False
        count = 0
        for line in content.split('\n'):
            if re.match(r'^##\s+.*(心智模型|Mental Model|我看问题的方式)', line, re.IGNORECASE):
                in_section = True
                continue
            if in_section and re.match(r'^##\s+', line) and '心智模型' not in line and '我看问题' not in line:
                break
            if in_section and re.match(r'^###\s+', line):
                count += 1
        if count > 0:
            passed = 3 <= count <= 7
            return passed, f"{count}个思维模型/习惯 {'✅' if passed else '❌ (应为3-7个)'}"

    count = len(models)
    if count == 0:
        return False, "未检测到心智模型/思维习惯section"
    passed = 3 <= count <= 7
    return passed, f"{count}个心智模型 {'✅' if passed else '❌ (应为3-7个)'}"


def check_limitations(content: str) -> tuple[bool, str]:
    """检查每个模型是否有局限性"""
    has_limitation = bool(re.search(r'局限|失效|不适用|盲区|limitation|blind spot', content, re.IGNORECASE))
    return has_limitation, "有局限性标注 ✅" if has_limitation else "❌ 未找到局限性描述"


def check_expression_dna(content: str) -> tuple[bool, str]:
    """检查表达DNA辨识度"""
    dna_section = bool(re.search(r'表达DNA|Expression DNA|表达风格|我说话的方式', content, re.IGNORECASE))
    if not dna_section:
        return False, "❌ 未找到表达DNA section"

    style_markers = len(re.findall(r'句式|词汇|语气|幽默|节奏|确定性|引用|口头禅', content))
    passed = style_markers >= 3
    return passed, f"表达DNA特征: {style_markers}项 {'✅' if passed else '❌ (应≥3项)'}"


def check_honest_boundary(content: str) -> tuple[bool, str]:
    """检查诚实边界（至少3条）"""
    boundary_match = re.search(r'(?:##\s+.*(?:诚实边界|我明确不懂|Honest Boundary))(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE)
    if not boundary_match:
        return False, "❌ 未找到诚实边界section"

    boundary_text = boundary_match.group(1)
    items = re.findall(r'^[-*]\s+', boundary_text, re.MULTILINE)
    count = len(items)
    passed = count >= 3
    return passed, f"诚实边界: {count}条 {'✅' if passed else '❌ (应≥3条)'}"


def check_tensions(content: str) -> tuple[bool, str]:
    """检查内在张力（至少2对）"""
    tension_markers = len(re.findall(r'张力|矛盾|tension|paradox|一方面.*另一方面|既.*又|没想清楚', content, re.IGNORECASE))
    passed = tension_markers >= 2
    return passed, f"内在张力: {tension_markers}处 {'✅' if passed else '❌ (应≥2处)'}"


def check_primary_sources(content: str) -> tuple[bool, str]:
    """检查一手来源占比"""
    source_section = re.search(r'(?:##\s+.*来源|## Source|## Reference)(.*?)(?=\n##\s|\Z)', content, re.DOTALL | re.IGNORECASE)
    if not source_section:
        return True, "未找到来源section（跳过检查）"

    source_text = source_section.group(1)
    primary = len(re.findall(r'一手|primary|本人著作|原始', source_text, re.IGNORECASE))
    secondary = len(re.findall(r'二手|secondary|转述|评论', source_text, re.IGNORECASE))
    total = primary + secondary
    if total == 0:
        return True, "未标记来源类型（跳过检查）"

    ratio = primary / total
    passed = ratio > 0.5
    return passed, f"一手来源占比: {primary}/{total} ({ratio:.0%}) {'✅' if passed else '❌ (应>50%)'}"


# ============================================================
# 仓颉升级检查项（5项）— Harness Engine 相关
# ============================================================

def check_trigger_conditions(content: str) -> tuple[bool, str]:
    """检查心智模型是否有触发条件"""
    triggers = re.findall(r'触发条件|触发信号|trigger|什么时候用|什么情况下.*激活', content, re.IGNORECASE)
    # 也检查模型section中的结构化触发条件
    structured_triggers = re.findall(r'\*\*触发条件\*\*', content)

    count = len(structured_triggers) if structured_triggers else len(triggers)
    passed = count >= 3
    return passed, f"触发条件: {count}个模型有标注 {'✅' if passed else '❌ (应≥3个模型有触发条件)'}"


def check_reasoning_steps(content: str) -> tuple[bool, str]:
    """检查心智模型是否有推理步骤"""
    # 检查结构化推理步骤
    step_patterns = re.findall(r'\*\*推理步骤\*\*|推理步骤：|reasoning steps', content, re.IGNORECASE)
    # 也检查编号步骤（在模型section中）
    numbered_steps = re.findall(r'^\s+\d+\.\s+', content, re.MULTILINE)

    has_steps = len(step_patterns) >= 2 or len(numbered_steps) >= 6
    return has_steps, f"推理步骤: {'✅ 有结构化步骤' if has_steps else '❌ 未找到推理步骤（模型应包含可操作的分步推理）'}"


def check_reasoning_traces(content: str) -> tuple[bool, str]:
    """检查是否有推理示例链（至少2个）"""
    # 检查推理示例/推理链section
    trace_section = bool(re.search(r'推理示例|推理链|reasoning.*(?:trace|example|chain)|示例链', content, re.IGNORECASE))
    if not trace_section:
        return False, "❌ 未找到推理示例链section"

    # 计算示例数量
    examples = re.findall(r'^###\s+示例\s*\d|^###\s+Example\s*\d|^###\s+推理示例\s*\d', content, re.MULTILINE)
    if not examples:
        # fallback: 看有没有"问题：" + "推理过程："的配对
        examples = re.findall(r'(?:问题|匹配模型|模型匹配).*?(?:推理|结论)', content, re.DOTALL)

    count = len(examples)
    passed = count >= 2
    return passed, f"推理示例链: {count}个 {'✅' if passed else '❌ (应≥2个完整推理链)'}"


def check_anti_pattern_guardrail(content: str) -> tuple[bool, str]:
    """检查反模式是否集成为推理护栏（不只是列表）"""
    # 检查是否有"护栏"、"检查"、"扫描反模式"等集成性描述
    guardrail_markers = re.findall(
        r'护栏|guardrail|反模式检查|反模式护栏|扫描.*反模式|检查.*反模式|step.*3\.3|踩中',
        content, re.IGNORECASE
    )
    passed = len(guardrail_markers) >= 2
    return passed, f"反模式护栏: {'✅ 已集成到推理流程' if passed else '❌ 反模式只是列出来了，未集成到推理流程中'}"


def check_harness_engine(content: str) -> tuple[bool, str]:
    """检查是否有 Harness Engine / 运行时推理引擎"""
    has_engine = bool(re.search(
        r'Harness Engine|运行时推理|推理引擎|问题路由|模型匹配.*推理.*输出',
        content, re.IGNORECASE
    ))
    if not has_engine:
        # fallback: 检查是否有结构化的多步推理流程
        has_engine = bool(re.search(r'Step\s*1.*路由|Step\s*2.*研究|Step\s*3.*推理', content, re.IGNORECASE | re.DOTALL))

    return has_engine, f"Harness Engine: {'✅ 有运行时推理引擎' if has_engine else '❌ 缺少运行时推理引擎（模型提取了但没有运行机制）'}"


def main():
    if len(sys.argv) < 2:
        print("用法: python3 quality_check.py <SKILL.md路径>")
        sys.exit(1)

    skill_path = Path(sys.argv[1])
    if not skill_path.exists():
        print(f"❌ 文件不存在: {skill_path}")
        sys.exit(1)

    content = skill_path.read_text(encoding='utf-8')

    nuwa_checks = [
        ("心智模型数量", check_mental_models),
        ("模型局限性", check_limitations),
        ("表达DNA辨识度", check_expression_dna),
        ("诚实边界", check_honest_boundary),
        ("内在张力", check_tensions),
        ("一手来源占比", check_primary_sources),
    ]

    cangjie_checks = [
        ("触发条件", check_trigger_conditions),
        ("推理步骤", check_reasoning_steps),
        ("推理示例链", check_reasoning_traces),
        ("反模式护栏", check_anti_pattern_guardrail),
        ("Harness Engine", check_harness_engine),
    ]

    print(f"质量检查: {skill_path.name}")
    print("=" * 60)

    passed_count = 0
    total = 0

    print("  ── 女娲基础项 ──")
    for name, check_fn in nuwa_checks:
        passed, detail = check_fn(content)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:<14} {status}  {detail}")
        if passed:
            passed_count += 1
        total += 1

    print()
    print("  ── 仓颉升级项 ──")
    cangjie_passed = 0
    for name, check_fn in cangjie_checks:
        passed, detail = check_fn(content)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {name:<14} {status}  {detail}")
        if passed:
            passed_count += 1
            cangjie_passed += 1
        total += 1

    print("=" * 60)
    print(f"结果: {passed_count}/{total} 通过（女娲 {passed_count - cangjie_passed}/6 + 仓颉 {cangjie_passed}/5）")

    if passed_count == total:
        print("🎉 全部通过，可以交付")
    elif passed_count >= total - 2:
        print("⚠️ 基本通过，建议修复不通过项后交付")
    else:
        print("❌ 多项不通过，建议回到Phase 2迭代")

    sys.exit(0 if passed_count == total else 1)


if __name__ == '__main__':
    main()
