"""Loads prompts/*.md and splits them into SYSTEM / USER_TEMPLATE sections."""

from pathlib import Path

SYSTEM_MARKER = "<!-- SYSTEM -->"
USER_TEMPLATE_MARKER = "<!-- USER_TEMPLATE -->"

PROMPTS_DIR = Path(__file__).resolve().parent.parent / "prompts"


def load_prompt(name: str) -> tuple[str, str]:
    """Returns (system, user_template) for prompts/<name>.md.

    A prompt file may contain either or both sections; missing sections
    return an empty string.
    """
    text = (PROMPTS_DIR / f"{name}.md").read_text()

    system = ""
    user_template = ""

    if SYSTEM_MARKER in text:
        after_system = text.split(SYSTEM_MARKER, 1)[1]
        system = after_system.split(USER_TEMPLATE_MARKER, 1)[0].strip()

    if USER_TEMPLATE_MARKER in text:
        user_template = text.split(USER_TEMPLATE_MARKER, 1)[1].strip()

    return system, user_template


def render_template(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", value if value else "UNKNOWN")
    return rendered
