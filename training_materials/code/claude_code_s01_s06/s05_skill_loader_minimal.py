"""s05 最小示例：按需加载 skill。"""

from __future__ import annotations

from pathlib import Path


SKILLS_DIR = Path(__file__).resolve().parent / "skills_demo"


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """极简 frontmatter 解析器。

    这里只支持最简单的：

    ---
    name: ...
    description: ...
    ---
    正文

    这样的解析能力已经足够拿来讲“manifest + body”的概念。
    """

    if not text.startswith("---"):
        return {}, text

    _, raw_meta, body = text.split("---", 2)
    meta: dict[str, str] = {}
    for line in raw_meta.strip().splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip().strip('"')
    return meta, body.strip()


class SkillRegistry:
    """极简 Skill 注册表。"""

    def __init__(self, skills_dir: Path) -> None:
        self.skills_dir = skills_dir
        self.skills: dict[str, dict[str, str]] = {}
        self._load_all()

    def _load_all(self) -> None:
        for path in self.skills_dir.rglob("SKILL.md"):
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            name = meta.get("name", path.parent.name)
            self.skills[name] = {
                "name": name,
                "description": meta.get("description", ""),
                "body": body,
            }

    def describe_available(self) -> str:
        return "\n".join(
            f"- {skill['name']}: {skill['description']}"
            for skill in self.skills.values()
        )

    def load_full_text(self, name: str) -> str:
        skill = self.skills[name]
        return (
            f"<skill name=\"{skill['name']}\">\n"
            f"{skill['body']}\n"
            f"</skill>"
        )


def demo() -> None:
    registry = SkillRegistry(SKILLS_DIR)

    print("可用 skill 目录：")
    print(registry.describe_available())

    print("\n按需加载 code-review：")
    print(registry.load_full_text("code-review"))


if __name__ == "__main__":
    demo()
