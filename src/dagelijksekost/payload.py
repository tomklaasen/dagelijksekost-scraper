"""Extract recipe instructions from the Next.js RSC payload of a dagelijksekost.vrt.be page.

The page's JSON-LD only lists the first two HowToSteps; the full set sits in the streamed
Next.js payload under "recipeParts". recipe-scrapers has a fallback for this, but it still
expects the site's older {"0": "...", "1": "..."} format instead of today's step objects.
"""

import json
import re

CHUNK_RE = re.compile(r'self\.__next_f\.push\(\[\d+,("(?:[^"\\]|\\.)*")\]\)')


def directions(html: str) -> str | None:
    """All instruction steps of the recipe page, one per line, or None when the payload is absent.

    A step's tip, when it has one, follows it on its own "Tip: ..." line.
    """
    chunks = []
    for chunk in CHUNK_RE.findall(html):
        try:
            chunks.append(json.loads(chunk))
        except json.JSONDecodeError:
            continue
    stream = "".join(chunks)

    decoder = json.JSONDecoder()
    for match in re.finditer(r'"recipeParts":', stream):
        try:
            parts, _ = decoder.raw_decode(stream, match.end())
        except (json.JSONDecodeError, ValueError):
            continue
        if not isinstance(parts, list):
            continue

        lines = []
        for part in parts:
            steps = part.get("instructions") or []
            for step in sorted(steps, key=lambda s: (s.get("part") or 0, s.get("step") or 0)):
                description = (step.get("description") or "").strip()
                if description:
                    lines.append(description)
                tip = (step.get("tip") or "").strip()
                if tip:
                    lines.append(f"Tip: {tip}")
        if lines:
            return "\n".join(lines)
    return None
