def generate_digest(scored_items):
    scored_items = sorted(
        scored_items,
        key=lambda x: x.get("relevance_score", 0), 
        reverse=True,
    )

    lines = ["# Paper Relevance Digest\n"]

    for item in scored_items:
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

    return "\n".join(lines)

