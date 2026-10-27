import datetime
import html


def escape_text(text):
    return html.escape(text or "")


def line_breaks(text):
    return "<br>".join(escape_text(text or "").splitlines())


def build_report(results, user_prompt, endpoint, model):
    lines = []
    lines.append("# Prompt Test Results")
    lines.append("")
    lines.append(f"- Endpoint: {escape_text(endpoint)}")
    lines.append(f"- Model: {escape_text(model)}")
    lines.append(f"- Generated: {datetime.datetime.now().isoformat()}")
    lines.append("")
    lines.append("## User Prompt")
    lines.append("")
    lines.append("```")
    lines.append(user_prompt)
    lines.append("```")
    lines.append("")
    lines.append("## Side-by-Side Comparison")
    lines.append("")
    lines.append("| System Prompt | Response |")
    lines.append("| --- | --- |")
    for result in results:
        name = escape_text(result.name)
        if result.ok:
            response = line_breaks(result.response)
        else:
            response = f"ERROR: {escape_text(result.error)}"
        lines.append(f"| {name} | {response} |")
    lines.append("")
    lines.append("## Detailed Results")
    lines.append("")
    for result in results:
        lines.append(f"### {escape_text(result.name)}")
        lines.append("")
        lines.append("**System prompt:**")
        lines.append("")
        lines.append("```")
        lines.append(result.system_prompt or "")
        lines.append("```")
        lines.append("")
        if result.ok:
            lines.append("**Response:**")
            lines.append("")
            lines.append("```")
            lines.append(result.response)
            lines.append("```")
        else:
            lines.append(f"**Error:** {escape_text(result.error)}")
        lines.append("")
    return "\n".join(lines)
