#!/usr/bin/env python3
"""Skill loader — discovers and loads procedural memory at runtime.

Skills are markdown files with YAML frontmatter:

    ---
    name: x-tweet-via-cloakbrowser
    description: Post tweets via CloakBrowser (bypasses shadow-block)
    triggers: [tweet, post, x.com, twitter]
    ---

    ## Steps
    1. Launch CloakBrowser with persistent profile
    2. Navigate to /compose/post
    ...

The agent scans skill descriptions on every turn and loads matching ones into context.
"""
import os
import re
from pathlib import Path
from typing import Optional

import yaml

SKILLS_DIR = os.environ.get("SKILLS_DIR", "/home/agent/.hermes/skills")


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split YAML frontmatter from body."""
    match = re.match(r"^---\n(.*?)\n---\n(.*)", text, re.DOTALL)
    if not match:
        return {}, text
    return yaml.safe_load(match.group(1)) or {}, match.group(2)


def list_skills() -> list[dict]:
    """Return [{name, description, path}, ...] for all skills."""
    skills = []
    for skill_md in Path(SKILLS_DIR).rglob("SKILL.md"):
        text = skill_md.read_text()
        meta, _ = parse_frontmatter(text)
        skills.append({
            "name": meta.get("name", skill_md.parent.name),
            "description": meta.get("description", ""),
            "triggers": meta.get("triggers", []),
            "path": str(skill_md),
        })
    return skills


def find_relevant(query: str, top_k: int = 3) -> list[dict]:
    """Match user query to skill triggers + descriptions."""
    query_low = query.lower()
    matches = []
    for skill in list_skills():
        score = 0
        for trigger in skill.get("triggers", []):
            if trigger.lower() in query_low:
                score += 10
        # Description keyword overlap
        for word in skill["description"].lower().split():
            if len(word) > 4 and word in query_low:
                score += 1
        if score > 0:
            matches.append((score, skill))
    matches.sort(reverse=True)
    return [m[1] for m in matches[:top_k]]


def load_skill(name: str) -> Optional[str]:
    """Return full SKILL.md content for execution context."""
    for skill in list_skills():
        if skill["name"] == name:
            return Path(skill["path"]).read_text()
    return None


if __name__ == "__main__":
    import json
    print(json.dumps(list_skills(), indent=2))
