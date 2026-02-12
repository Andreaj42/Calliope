import json
from logging import getLogger

logger = getLogger(__name__)


def generate_digest(scored_items, min_score=30):
    logger.info(
        f"Generating digest with {len(scored_items)} scored items, min_score={min_score}"
    )

    pretty = json.dumps(
        scored_items,
        ensure_ascii=False,
        indent=2,
        sort_keys=False,
    )

    logger.info("Scored items (pretty):\n%s", pretty)

    filtered_items = [
        item for item in scored_items if item.get("relevance_score", 0) >= min_score
    ]
    if len(filtered_items) == 0:
        return "", 0

    filtered_items = sorted(
        filtered_items,
        key=lambda x: x.get("relevance_score", 0),
        reverse=True,
    )

    lines = ["# Daily Article Suggestions\n"]

    for item in filtered_items:
        title = item.get("title", "Untitled")
        url = item.get("url", "")
        score = item.get("relevance_score", "N/A")
        reasons = item.get("reasons", [])

        lines.append(f"## Score: {score}")
        lines.append(f"**{title}**")
        lines.append(f"- URL: {url}")

        if reasons:
            lines.append("- Reasons:")
            for r in reasons:
                lines.append(f"  - {r}")
            lines.append("")

    return "\n".join(lines), len(filtered_items)
