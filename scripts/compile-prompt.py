#!/usr/bin/env python3
"""
Skill → API Prompt 编译器

SKILL.md 是为 Claude Code CLI 设计的（模型能读文件、按步骤执行、调用工具）。
但 Web API 调用时，system prompt 需要短、直接、让模型"成为"这个人而不是"阅读说明书"。

编译逻辑：
1. 提取身份卡 → 变成第一人称自我定义
2. 提取核心信念 → 变成"我相信什么"
3. 提取心智模型 → 只保留名称+一句话+推理步骤（去掉证据、触发条件等元数据）
4. 提取反模式 → 变成"我绝不会做什么"
5. 提取表达DNA → 变成风格指令
6. 去掉所有框架说明、角色扮演规则、退出指令等 CLI 专用内容
"""

import re
import json
import sys
from pathlib import Path


def extract_section(content, header_pattern, next_header=r'^## '):
    """提取某个 ## section 的内容"""
    match = re.search(rf'^{header_pattern}.*$', content, re.MULTILINE)
    if not match:
        return ''
    start = match.end()
    # 找下一个同级 header
    rest = content[start:]
    next_match = re.search(rf'^{next_header}', rest, re.MULTILINE)
    if next_match:
        return rest[:next_match.start()].strip()
    return rest.strip()


def extract_models_compact(content):
    """提取心智模型，只保留名称+一句话+推理步骤"""
    section = extract_section(content, r'## 核心心智模型')
    if not section:
        return ''

    models = []
    # 找所有 ### 模型N: XXX
    parts = re.split(r'^### ', section, flags=re.MULTILINE)
    for part in parts[1:]:  # skip first empty
        lines = part.strip().split('\n')
        name = lines[0].strip().rstrip(':')

        # 提取一句话
        one_line = ''
        m = re.search(r'\*\*一句话\*\*[：:]\s*(.+)', part)
        if m:
            one_line = m.group(1).strip()

        # 提取推理步骤
        steps = []
        in_steps = False
        for line in lines:
            if '**推理步骤**' in line:
                in_steps = True
                continue
            if in_steps:
                if line.strip().startswith(('**证据**', '**局限**', '**触发条件**', '---')):
                    break
                step_match = re.match(r'\s*\d+\.\s*\*\*(.+?)\*\*[：:]?\s*(.*)', line)
                if step_match:
                    steps.append(f"{step_match.group(1)}: {step_match.group(2)}")
                elif re.match(r'\s*\d+\.\s*', line):
                    steps.append(line.strip())

        if one_line:
            model_text = f"【{name.split(':')[-1].strip()}】{one_line}"
            if steps:
                model_text += '\n  步骤：' + ' → '.join(steps[:4])  # 最多4步
            models.append(model_text)

    return '\n'.join(models)


def extract_antipatterns_compact(content):
    """提取反模式，只保留要点"""
    section = extract_section(content, r'## 反模式')
    if not section:
        section = extract_section(content, r'## 价值观与反模式')
    if not section:
        return ''

    # 找表格行
    patterns = []
    for m in re.finditer(r'\|\s*\*\*(.+?)\*\*\s*\|.*?\|.*?\|', section):
        patterns.append(m.group(1))

    # 或者找 **我拒绝的**
    reject = re.search(r'\*\*我拒绝的\*\*[：:]\s*\n((?:[-*].+\n?)+)', section)
    if reject:
        for line in reject.group(1).strip().split('\n'):
            line = re.sub(r'^[-*]\s*', '', line).strip()
            if line:
                patterns.append(line)

    return '、'.join(patterns[:6])


def extract_beliefs(content):
    """提取核心信念"""
    section = extract_section(content, r'## 价值观与核心信念')
    if not section:
        section = extract_section(content, r'## 价值观与反模式')
    if not section:
        return ''

    beliefs = []
    for m in re.finditer(r'\d+\.\s*\*\*(.+?)\*\*\s*[——–-]+\s*(.+)', section):
        beliefs.append(f"{m.group(1)}: {m.group(2)[:60]}")

    return '\n'.join(beliefs[:5])


def extract_expression_dna(content):
    """提取表达风格，精简为几条规则"""
    section = extract_section(content, r'## 表达DNA')
    if not section:
        return ''

    rules = []
    for m in re.finditer(r'\*\*(.+?)\*\*[：:]\s*(.+)', section):
        key = m.group(1)
        val = m.group(2).strip()[:80]
        rules.append(f"{key}: {val}")

    return '\n'.join(rules[:5])


def extract_identity(content):
    """提取身份卡"""
    section = extract_section(content, r'## 身份卡')
    if not section:
        return ''

    parts = []
    for m in re.finditer(r'\*\*(.+?)\*\*[：:]\s*(.+)', section):
        parts.append(m.group(2).strip())

    return ' '.join(parts)


def compile_skill_to_prompt(skill_path):
    """把 SKILL.md 编译为 API 专用的精简 prompt"""
    content = Path(skill_path).read_text()

    # 提取人物名
    name_match = re.search(r'^# (.+?)$', content, re.MULTILINE)
    person_name = name_match.group(1) if name_match else '未知人物'

    identity = extract_identity(content)
    beliefs = extract_beliefs(content)
    models = extract_models_compact(content)
    antipatterns = extract_antipatterns_compact(content)
    expression = extract_expression_dna(content)

    # 组装编译后的 prompt
    prompt = f"""你是{person_name.split('·')[0].strip()}。以下是你的思维方式，用它来回答所有问题。

{identity}

## 我的核心信念
{beliefs}

## 我分析问题的方式
{models}

## 我绝不会做的事
{antipatterns}

## 我说话的方式
{expression}

重要：直接以第一人称回答，不要提及"思维模型"、"框架"这些meta概念。像真人对话一样自然地运用上面的思维方式。用中文回答。"""

    return prompt


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 compile-prompt.py <SKILL.md路径>")
        sys.exit(1)

    prompt = compile_skill_to_prompt(sys.argv[1])
    print(f"编译完成: {len(prompt)} chars")
    print("=" * 50)
    print(prompt)
