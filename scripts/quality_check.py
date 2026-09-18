#!/usr/bin/env python3
"""Validate a generated Cangjie v3 persona skill."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Result:
    name: str
    passed: bool
    detail: str


def section(content: str, title: str, level: int = 2) -> str:
    marks = "#" * level
    match = re.search(rf"^{marks}\s+{re.escape(title)}\s*$", content, re.MULTILINE)
    if not match:
        return ""
    rest = content[match.end() :]
    sibling = re.search(rf"^{marks}\s+", rest, re.MULTILINE)
    return rest[: sibling.start() if sibling else None].strip()


def count_numbered(text: str) -> int:
    return len(re.findall(r"^\d+\.\s+", text, re.MULTILINE))


def count_bullets(text: str) -> int:
    return len(re.findall(r"^[-*]\s+", text, re.MULTILINE))


def evaluate(content: str) -> list[Result]:
    context = section(content, "我的认知上下文")
    beliefs = section(context, "信念及其来源", 3)
    decisions = section(context, "我做过的关键决策", 3)
    failures = section(context, "我栽过的跟头", 3)
    tensions = section(context, "我的内在矛盾", 3)
    boundaries = section(context, "我明确不懂的", 3)
    habits = section(content, "我看问题的方式")
    guardrails = section(content, "我绝不会做的事")
    voice = section(content, "我说话的方式")
    sources = section(content, "素材来源")

    belief_count = count_numbered(beliefs)
    decision_count = count_numbered(decisions)
    failure_count = count_numbered(failures)
    tension_count = count_numbered(tensions)
    boundary_count = count_bullets(boundaries)
    habit_count = len(re.findall(r"^###\s+", habits, re.MULTILINE))
    guardrail_count = count_bullets(guardrails)
    belief_story_hits = len(re.findall(r"因为|经历|后来|之后|教会|让我|来自", beliefs))
    decision_reflection_hits = len(re.findall(r"事后|回头|学到|教会|意识到|后来", decisions))
    first_person_sections = [beliefs, decisions, failures, tensions, boundaries, habits, guardrails, voice]
    first_person_ok = all(re.search(r"我|我的", value) for value in first_person_sections if value)
    forbidden_steps = bool(re.search(r"(?:^|\n)\s*(?:Step\s*[123]|步骤\s*[123]|第[一二三]步)[：:]?", habits, re.IGNORECASE))
    voice_fields = sum(bool(re.search(rf"^[-*]\s*\*\*?{key}", voice, re.MULTILINE)) for key in ("偏好", "禁忌", "不确定时"))
    source_count = count_bullets(sources)

    return [
        Result("核心结构", bool(context and habits and guardrails and voice), "认知上下文、思维习惯、红线、表达方式齐全"),
        Result("信念形成故事", 5 <= belief_count <= 7 and belief_story_hits >= max(1, belief_count - 1), f"{belief_count} 条信念，{belief_story_hits} 个形成故事信号（目标 5–7）"),
        Result("关键决策反思", 3 <= decision_count <= 5 and decision_reflection_hits >= max(1, decision_count - 1), f"{decision_count} 个决策，{decision_reflection_hits} 个反思信号（目标 3–5）"),
        Result("本人失败", 2 <= failure_count <= 3 and bool(re.search(r"我|本人", failures)), f"{failure_count} 个失败案例（目标 2–3）"),
        Result("内在矛盾", tension_count >= 2, f"{tension_count} 对矛盾（至少 2）"),
        Result("认知边界", boundary_count >= 3, f"{boundary_count} 条边界（至少 3）"),
        Result("思维习惯", 3 <= habit_count <= 9, f"{habit_count} 个习惯（建议 3–7，最多 9）"),
        Result("禁止显式步骤", not forbidden_steps, "未发现 Step 1/2/3" if not forbidden_steps else "发现显式推理步骤"),
        Result("第一人称", first_person_ok, "核心章节使用第一人称" if first_person_ok else "有核心章节缺少第一人称"),
        Result("红线", 4 <= guardrail_count <= 7, f"{guardrail_count} 条红线（目标 4–6）"),
        Result("表达信号", voice_fields == 3, f"偏好/禁忌/不确定时：{voice_fields}/3"),
        Result("素材来源", source_count >= 2, f"{source_count} 条来源（至少 2）"),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill", type=Path)
    args = parser.parse_args()
    results = evaluate(args.skill.read_text(encoding="utf-8"))
    print(f"质量检查: {args.skill}")
    print("=" * 64)
    for result in results:
        print(f"{'✅ PASS' if result.passed else '❌ FAIL'}  {result.name:<10} {result.detail}")
    passed = sum(result.passed for result in results)
    print("=" * 64)
    print(f"结果: {passed}/{len(results)} 通过")
    return 0 if passed == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
