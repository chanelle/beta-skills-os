#!/usr/bin/env python3
"""Dependency-free static validator for Beta Skills OS skill definitions."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
REQUIRED_GROUPS = (
    ("## Trigger", "## When to invoke"),
    ("## Inputs", "## Required inputs"),
    ("## Procedure", "## Workflow"),
    ("## Output contract", "## Output schema"),
)
EXPECTED = {
    "agent-authority-audit", "brain-to-skill", "chanelle-voice",
    "deep-research", "design-director", "publish-pipeline",
    "ssot-guardian", "usage-observatory", "ux-copy", "verify-gate",
    "case-executor", "squeaky-wheel", "council-protocol",
}


def validate():
    errors = []
    found = set()
    for path in sorted(SKILLS.glob("*/SKILL.md")):
        slug = path.parent.name
        found.add(slug)
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---\n"):
            errors.append(f"{slug}: missing YAML frontmatter")
            continue
        pieces = content.split("---", 2)
        if len(pieces) < 3:
            errors.append(f"{slug}: unclosed frontmatter")
            continue
        front = pieces[1]
        match = re.search(r"(?m)^name:\s*(.+)$", front)
        if not match or match.group(1).strip() != slug:
            errors.append(f"{slug}: name does not match folder")
        if not re.search(r"(?m)^description:\s*\S+", front):
            errors.append(f"{slug}: missing description")
        for aliases in REQUIRED_GROUPS:
            if not any(section in content for section in aliases):
                errors.append(f"{slug}: missing one of {aliases}")
        if not re.search(r"\*\*Version:\*\*\s*\d+\.\d+\.\d+", content):
            errors.append(f"{slug}: missing semantic version")
    for missing in sorted(EXPECTED - found):
        errors.append(f"missing expected skill: {missing}")
    for unexpected in sorted(found - EXPECTED):
        print(f"NOTICE: unregistered new skill: {unexpected}")
    if not (ROOT / "assets" / "hero.png").is_file():
        errors.append("missing assets/hero.png")
    if not (ROOT / "README.md").is_file():
        errors.append("missing README.md")
    if errors:
        print("FAIL:\n" + "\n".join(f"- {error}" for error in errors))
        return 1
    print(f"PASS: {len(found)} skill definitions, frontmatter, sections, versions and core assets")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
