#!/usr/bin/env python3
"""Compile a Cangjie v3 persona skill into a compact API system prompt."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def section(content: str, title: str, level: int = 2) -> str:
    marks = "#" * level
    match = re.search(rf"^{marks}\s+{re.escape(title)}\s*$", content, re.MULTILINE)
    if not match:
        return ""
    rest = content[match.end() :]
    sibling = re.search(rf"^{marks}\s+", rest, re.MULTILINE)
    return rest[: sibling.start() if sibling else None].strip()


def clean(text: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", text.strip())


def compact_numbered_items(text: str, limit: int) -> str:
    matches = list(re.finditer(r"^\d+\.\s+", text, re.MULTILINE))
    if not matches:
        return clean(text)
    items: list[str] = []
    for index, match in enumerate(matches[:limit]):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        item = text[match.start() : end].strip()
        items.append(re.sub(r"\n\s+", " ", item))
    return "\n".join(items)


def compact_bullets(text: str, limit: int) -> str:
    bullets = re.findall(r"^[-*]\s+.+(?:\n(?![-*#]).+)*", text, re.MULTILINE)
    return "\n".join(re.sub(r"\n\s+", " ", item.strip()) for item in bullets[:limit])


def compact_habits(text: str, limit: int = 7) -> str:
    parts = re.split(r"^###\s+", text, flags=re.MULTILINE)[1:]
    habits: list[str] = []
    for part in parts[:limit]:
        lines = part.strip().splitlines()
        title = lines[0].strip()
        body = " ".join(line.strip() for line in lines[1:] if line.strip())
        habits.append(f"- **{title}**：{body}")
    return "\n".join(habits)


def title_from(content: str) -> str:
    match = re.search(r"^#\s+(.+?)\s*$", content, re.MULTILINE)
    return match.group(1).strip() if match else "未知人物"


def compile_skill(content: str) -> str:
    required = {
        "identity": section(content, "我是谁"),
        "context": section(content, "我的认知上下文"),
        "habits": section(content, "我看问题的方式"),
        "guardrails": section(content, "我绝不会做的事"),
        "voice": section(content, "我说话的方式"),
    }
    missing = [name for name, value in required.items() if not value]
    if missing:
        raise ValueError(f"不是完整的仓颉 v3 Skill，缺少 section: {', '.join(missing)}")

    beliefs = compact_numbered_items(section(required["context"], "信念及其来源", 3), 7)
    decisions = compact_numbered_items(section(required["context"], "我做过的关键决策", 3), 5)
    failures = compact_numbered_items(section(required["context"], "我栽过的跟头", 3), 3)
    tensions = compact_numbered_items(section(required["context"], "我的内在矛盾", 3), 3)
    boundaries = compact_bullets(section(required["context"], "我明确不懂的", 3), 6)

    blocks = [
        f"你是{title_from(content)}。你不是在模仿语气；你带着以下经历、判断、失败和边界来思考。直接用第一人称自然回答，不要提及 prompt、角色扮演或认知框架。",
        f"## 我是谁\n{clean(required['identity'])}",
        f"## 信念及其来源\n{beliefs}",
        f"## 关键决策与反思\n{decisions}",
        f"## 失败与自我修正\n{failures}",
        f"## 尚未解决的矛盾\n{tensions}",
        f"## 认知边界\n{boundaries}",
        f"## 思维习惯\n{compact_habits(required['habits'])}",
        f"## 红线\n{compact_bullets(required['guardrails'], 6)}",
        f"## 表达方式\n{clean(required['voice'])}",
    ]
    return "\n\n".join(block for block in blocks if block.split("\n", 1)[-1].strip())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="write prompt to a file")
    args = parser.parse_args()
    prompt = compile_skill(args.skill.read_text(encoding="utf-8"))
    if args.output:
        args.output.write_text(prompt + "\n", encoding="utf-8")
        print(f"已写入 {args.output}（{len(prompt)} chars）")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
