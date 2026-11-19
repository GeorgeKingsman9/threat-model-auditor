"""Render offline, self-contained reports without interpreting paper text as HTML."""

import html
import json
from pathlib import Path
import re


STATE_LABELS = {
    "not_applicable": "不适用（非 IPI 论文）",
    "inconsistent": "有已确认的不一致",
    "consistent_within_scope": "审计范围内一致",
    "insufficient_evidence": "证据不足",
    "error": "运行错误",
    "failed": "运行失败",
    "failure": "运行失败",
    "technical_failure": "技术失败",
    "invalid": "输入或运行无效",
    "blocked": "运行受阻",
    "pending": "待运行",
    "not_run": "尚未运行",
    "not_started": "尚未开始",
    "queued": "已排队",
    "planned": "已计划，尚未运行",
    "running": "运行中",
    "skipped": "已跳过",
    "completed": "已完成",
    "success": "已完成",
    "passed": "已通过",
    "unknown": "未记录状态",
}
ERROR_STATES = {"error", "failed", "failure", "technical_failure", "invalid", "blocked"}
INCOMPLETE_STATES = {"pending", "not_run", "not_started", "queued", "planned", "running", "skipped"}


def _json(value):
    return json.dumps(value, ensure_ascii=False, indent=2)


def _text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _html(value):
    return html.escape(_text(value), quote=True)


def _md(value):
    # Escape raw HTML, Markdown syntax and table separators in untrusted text.
    value = html.escape(_text(value), quote=False)
    value = re.sub(r"([\\`*_{}\[\]()#+.!~\-])", r"\\\1", value)
    return value.replace("|", "&#124;").replace("\r\n", "\n").replace("\r", "\n").replace("\n", "<br>")


def _fenced_json(value):
    text = _json(value)
    # A paper excerpt can itself contain Markdown fences; never let it end ours.
    longest = max((len(match.group()) for match in re.finditer(r"`+", text)), default=0)
    fence = "`" * max(3, longest + 1)
    return f"{fence}json\n{text}\n{fence}"


def _paper_state(paper):
    status = _text(paper.get("status", paper.get("state"))).strip()
    if paper.get("error"):
        return status if status in ERROR_STATES else "error"
    if status in ERROR_STATES | INCOMPLETE_STATES:
        return status
    return _text(paper.get("verdict")).strip() or status or "not_run"


def _state_label(state):
    return STATE_LABELS.get(state, state or STATE_LABELS["unknown"])


def _confirmed(paper):
    value = paper.get("has_confirmed_inconsistency")
    if value is True:
        return "有"
    if value is False:
        return "未确认"
    return "未给出"


def _comparison(paper):
    matched = paper.get("matches_gold")
    label = "匹配" if matched is True else "不匹配" if matched is False else "未评分"
    if "expected" in paper:
        label += f"；预期：{_state_label(_text(paper['expected']))}"
    return label


def _identity(paper, index):
    paper_id = _text(paper.get("id")) or f"paper-{index + 1}"
    return paper_id, _text(paper.get("title")) or paper_id


def _stages(paper):
    stages = paper.get("stages", [])
    if not isinstance(stages, list):
        return [stages]
    return stages


def _stage_parts(stage, index):
    if not isinstance(stage, dict):
        return f"步骤 {index + 1}", "unknown", stage
    name = next((stage[key] for key in ("name", "stage", "step", "title", "id") if key in stage), f"步骤 {index + 1}")
    state = next((stage[key] for key in ("status", "state", "verdict") if key in stage), "unknown")
    # Keep every field in the detail cell even when its name appears elsewhere.
    return _text(name), _text(state), stage


def _badge(state):
    if state in ERROR_STATES or state == "inconsistent":
        category = "attention"
    elif state == "consistent_within_scope" or state in {"completed", "success", "passed"}:
        category = "complete"
    else:
        category = "pending"
    return f'<span class="badge {category}">{_html(_state_label(state))}</span>'


def _pre(value):
    return f"<pre>{_html(_json(value))}</pre>"


def _render_html(report, papers):
    rows = []
    sections = []
    for index, paper in enumerate(papers):
        paper_id, title = _identity(paper, index)
        rows.append(
            f'<tr class="paper-summary" data-paper-id="{_html(paper_id)}">'
            f'<th scope="row"><a href="#paper-{index}">{_html(title)}</a><small>{_html(paper_id)}</small></th>'
            f"<td>{_badge(_paper_state(paper))}</td>"
            f"<td>{_html(_confirmed(paper))}</td>"
            f"<td>{_html(_comparison(paper))}</td>"
            f"<td>{_html(paper.get('source', '未记录'))}</td></tr>"
        )
        stages = _stages(paper)
        stage_rows = []
        for step_index, stage in enumerate(stages):
            name, state, detail = _stage_parts(stage, step_index)
            stage_rows.append(f"<tr><th scope=\"row\">{_html(name)}</th><td>{_badge(state)}</td><td>{_pre(detail)}</td></tr>")
        stage_html = (
            '<div class="table-scroll"><table class="stages"><thead><tr><th>步骤</th><th>状态</th><th>记录</th></tr></thead>'
            f"<tbody>{''.join(stage_rows)}</tbody></table></div>"
            if stages else "<p>未记录执行步骤。</p>"
        )
        sections.append(
            f'<details class="paper-detail" id="paper-{index}">'
            f"<summary>{_html(title)} · {_html(_state_label(_paper_state(paper)))}</summary>"
            f"<p>论文 ID：<code>{_html(paper_id)}</code></p>"
            f"<h3>测试过程</h3>{stage_html}"
            f"<h3>证据</h3>{_pre(paper.get('evidence', []))}"
            f"<h3>备注</h3>{_pre(paper.get('notes', []))}"
            f"<details><summary>完整论文记录 JSON</summary>{_pre(paper)}</details>"
            "</details>"
        )
    if not papers:
        rows.append('<tr class="empty-report"><td colspan="5">本次报告没有论文记录。</td></tr>')
    return """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>论文审计：测试过程与结果</title>
<style>
:root{color-scheme:light;--ink:#172638;--muted:#526377;--border:#d9e1e9;--surface:#f4f7fa}
*{box-sizing:border-box}body{margin:0;background:var(--surface);color:var(--ink);font:16px/1.6 system-ui,sans-serif}
main{max-width:1250px;margin:auto;padding:32px 24px 60px}h1{font-size:30px;line-height:1.25;margin:0 0 12px}
h2{margin:28px 0 12px}h3{font-size:17px;margin:20px 0 8px}p{margin:10px 0}.metadata,small{color:var(--muted)}
small{display:block;font-weight:normal;margin-top:4px}a{color:#145a9a;text-decoration:underline;text-underline-offset:3px}
.table-scroll{overflow-x:auto;background:white;border:1px solid var(--border);border-radius:8px}
table{border-collapse:collapse;width:100%;text-align:left}th,td{padding:13px 14px;border-bottom:1px solid var(--border);vertical-align:top;overflow-wrap:anywhere}
thead{background:#eaf0f6}tbody tr:last-child>*{border-bottom:0}th{font-weight:600}.stages td:last-child{min-width:260px}
.badge{display:inline-block;padding:3px 9px;border-radius:5px;font-size:14px;white-space:nowrap}.attention{background:#ffe5df;color:#8c2b18}
.complete{background:#e0f1e6;color:#1f6643}.pending{background:#fff0cf;color:#735013}
details{background:white;border:1px solid var(--border);border-radius:8px;padding:14px 18px;margin:12px 0}
summary{cursor:pointer;font-weight:600}pre{background:#f1f4f8;border:1px solid var(--border);border-radius:6px;padding:12px;white-space:pre-wrap;overflow-wrap:anywhere;font:13px/1.55 ui-monospace,monospace;margin:8px 0}
td pre{max-height:360px;overflow:auto}code{font-family:ui-monospace,monospace}.explanation{color:var(--muted);max-width:88ch}
@media(max-width:650px){main{padding:24px 12px}h1{font-size:25px}th,td{padding:10px}details{padding:12px}}
@media print{body{background:white}main{max-width:none}.table-scroll{overflow:visible}pre,td pre{max-height:none;overflow:visible}}
</style>
</head><body><main>
<h1>论文审计：测试过程与结果</h1>
""" + (
        f'<p class="metadata">运行类型：{_html(report.get("run_type", "未记录"))} · '
        f'生成时间：{_html(report.get("created_at", "未记录"))} · 论文记录：{len(papers)}</p>'
        '<p class="explanation">主表每篇论文一行，展开下方记录查看执行步骤和证据。'
        '“未确认”表示本次记录没有确认发现，需结合运行状态和审计范围阅读。运行错误、待运行与证据不足分别显示。</p>'
        f'<details><summary>本次运行汇总</summary>{_pre(report.get("summary", {}))}</details>'
        '<h2>论文结果</h2><div class="table-scroll"><table id="paper-results">'
        '<thead><tr><th>论文</th><th>运行 / 判定</th><th>已确认不一致</th><th>标签对照</th><th>来源</th></tr></thead>'
        f'<tbody>{"".join(rows)}</tbody></table></div>'
        '<h2>逐篇测试过程</h2>' + "".join(sections)
        + '</main></body></html>\n'
    )


def _render_markdown(report, papers):
    lines = [
        "# 论文审计：测试过程与结果", "",
        f'运行类型：{_md(report.get("run_type", "未记录"))}  ',
        f'生成时间：{_md(report.get("created_at", "未记录"))}  ',
        f"论文记录：{len(papers)}", "",
        "主表每篇论文一行。“未确认”表示本次记录没有确认发现，需结合运行状态和审计范围阅读。运行错误、待运行与证据不足分别显示。", "",
        "## 本次运行汇总", "", _fenced_json(report.get("summary", {})), "",
        "## 论文结果", "",
        "| 论文 ID | 论文 | 运行 / 判定 | 已确认不一致 | 标签对照 | 来源 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for index, paper in enumerate(papers):
        paper_id, title = _identity(paper, index)
        values = (paper_id, title, _state_label(_paper_state(paper)), _confirmed(paper), _comparison(paper), paper.get("source", "未记录"))
        lines.append("| " + " | ".join(_md(value) for value in values) + " |")
    if not papers:
        lines.extend(["", "本次报告没有论文记录。"])
    lines.extend(["", "## 逐篇测试过程", ""])
    for index, paper in enumerate(papers):
        paper_id, title = _identity(paper, index)
        lines.extend([f"### {index + 1}. {_md(title)}", "", f"论文 ID：{_md(paper_id)}  ", f"运行 / 判定：{_md(_state_label(_paper_state(paper)))}", "", "#### 测试过程", ""])
        stages = _stages(paper)
        if stages:
            lines.extend(["| 步骤 | 状态 | 记录 |", "| --- | --- | --- |"])
            for step_index, stage in enumerate(stages):
                name, state, detail = _stage_parts(stage, step_index)
                lines.append("| " + " | ".join(_md(value) for value in (name, _state_label(state), detail)) + " |")
        else:
            lines.append("未记录执行步骤。")
        lines.extend(["", "#### 证据", "", _fenced_json(paper.get("evidence", [])), "", "#### 备注", "", _fenced_json(paper.get("notes", [])), "", "#### 完整论文记录 JSON", "", _fenced_json(paper), ""])
    return "\n".join(lines).rstrip() + "\n"


def write_reports(report: dict, output_dir: Path):
    """Write report.html and report.md, returning their Path values.

    All records, including empty, failed and pending records, are retained.
    Neither output is overwritten. Rendering completes before any file is opened;
    if creating the pair fails, only new files created by this call are removed.
    """
    if not isinstance(report, dict):
        raise ValueError("report must be an object")
    papers = report.get("papers", [])
    if not isinstance(papers, list) or any(not isinstance(paper, dict) for paper in papers):
        raise ValueError("report papers must be a list of objects")
    rendered = {"html": _render_html(report, papers), "markdown": _render_markdown(report, papers)}
    output_dir = Path(output_dir)
    paths = {"html": output_dir / "report.html", "markdown": output_dir / "report.md"}
    for path in paths.values():
        if path.exists() or path.is_symlink():
            raise FileExistsError(f"refusing to overwrite existing report: {path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        for kind, path in paths.items():
            with path.open("x", encoding="utf-8") as stream:
                created.append(path)
                stream.write(rendered[kind])
    except BaseException:
        for path in reversed(created):
            path.unlink(missing_ok=True)
        raise
    return paths
