"""Test report escaping, record coverage and preservation of existing outputs."""

from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from reports import write_reports


class ReportParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paper_rows = []
        self.active_tags = []
        self.external_resources = []
        self.all_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "tr" and attrs.get("class") == "paper-summary":
            self.paper_rows.append(attrs.get("data-paper-id"))
        if tag in {"script", "iframe", "object", "embed", "img", "video", "audio"}:
            self.active_tags.append(tag)
        for key in ("src", "href"):
            if key in attrs and not attrs[key].startswith("#"):
                self.external_resources.append(attrs[key])

    def handle_data(self, data):
        self.all_text.append(data)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="auditor reports ")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def report(self, papers):
        return {
            "run_type": "offline evidence audit",
            "created_at": "2026-11-19T12:00:00+08:00",
            "summary": {"paper_count": len(papers)},
            "papers": papers,
        }

    def parse(self, path):
        parser = ReportParser()
        parser.feed(path.read_text(encoding="utf-8"))
        return parser

    def test_untrusted_fields_are_text_and_have_no_external_resources(self):
        payload = '<script>alert("paper")</script><img src="https://example.org/private">'
        paper = {
            "id": '\"><iframe src="https://example.org"></iframe>',
            "title": payload,
            "source": payload,
            "verdict": "insufficient_evidence",
            "notes": [payload],
            "stages": [{"name": payload, "status": payload, "details": payload}],
            "evidence": [{"excerpt": payload}],
        }
        paths = write_reports(self.report([paper]), self.directory)
        parser = self.parse(paths["html"])
        self.assertEqual(parser.active_tags, [])
        self.assertEqual(parser.external_resources, [])
        self.assertEqual(parser.paper_rows, [paper["id"]])
        self.assertIn(payload, "".join(parser.all_text))
        self.assertIn("&lt;script&gt;", paths["html"].read_text())
        self.assertIn("&lt;script&gt;", paths["markdown"].read_text())

    def test_exactly_one_main_row_per_paper_despite_multiple_stages(self):
        papers = [{
            "id": f"paper_{i}",
            "title": f"论文 {i}",
            "verdict": "inconsistent",
            "has_confirmed_inconsistency": True,
            "stages": [{"name": "提取", "status": "completed"}, {"name": "判定", "status": "completed"}],
            "evidence": [{"reference": "line 10"}, {"reference": "line 20"}],
        } for i in range(3)]
        paths = write_reports(self.report(papers), self.directory)
        self.assertEqual(self.parse(paths["html"]).paper_rows, [p["id"] for p in papers])
        markdown = paths["markdown"].read_text()
        main_table = markdown.split("## 论文结果\n", 1)[1].split("## 逐篇测试过程", 1)[0]
        self.assertEqual(len([line for line in main_table.splitlines() if line.startswith("| ")]), 5)

    def test_empty_failed_pending_and_insufficient_records_are_all_retained(self):
        papers = [
            {},
            {"id": "failed", "status": "failed", "error": {"message": "source unavailable"}},
            {"id": "pending", "status": "pending"},
            {"id": "uncertain", "verdict": "insufficient_evidence", "has_confirmed_inconsistency": False},
        ]
        paths = write_reports(self.report(papers), self.directory)
        parser = self.parse(paths["html"])
        self.assertEqual(parser.paper_rows, ["paper-1", "failed", "pending", "uncertain"])
        text = "".join(parser.all_text)
        for label in ("尚未运行", "运行失败", "待运行", "证据不足", "source unavailable"):
            self.assertIn(label, text)
            self.assertIn(label, paths["markdown"].read_text())

    def test_empty_report_still_produces_readable_outputs(self):
        paths = write_reports(self.report([]), self.directory)
        self.assertEqual(self.parse(paths["html"]).paper_rows, [])
        self.assertIn("没有论文记录", paths["markdown"].read_text())

    def test_errors_take_precedence_over_a_provisional_verdict(self):
        report = self.report([{
            "id": "broken", "verdict": "insufficient_evidence", "error": "Could not parse PDF",
        }])
        paths = write_reports(report, self.directory)
        html = paths["html"].read_text()
        main_table = html.split('<table id="paper-results">', 1)[1].split("</table>", 1)[0]
        self.assertIn("运行错误", main_table)
        self.assertNotIn("证据不足", main_table)

    def test_markdown_fences_cannot_be_closed_by_paper_content(self):
        payload = "```\n<script>active()</script>\n````\n[remote](https://example.org)"
        report = self.report([{"id": "fences", "title": "name | [link](https://example.org)", "notes": [payload]}])
        paths = write_reports(report, self.directory)
        markdown = paths["markdown"].read_text()
        self.assertIn("`````json", markdown)
        self.assertIn("name &#124; \\[link\\]\\(https://example\\.org\\)", markdown)
        # The complete original record remains JSON-readable inside its fence.
        full_record = markdown.split("#### 完整论文记录 JSON\n\n", 1)[1]
        fence, content = full_record.split("\n", 1)
        raw_json = content.rsplit("\n" + fence.removesuffix("json"), 1)[0]
        self.assertEqual(json.loads(raw_json)["notes"], [payload])

    def test_refuse_overwrite_either_file_before_writing_the_other(self):
        for existing_name, absent_name in (("report.html", "report.md"), ("report.md", "report.html")):
            with self.subTest(existing=existing_name):
                directory = self.directory / existing_name
                directory.mkdir()
                existing = directory / existing_name
                existing.write_text("preserve this exact content", encoding="utf-8")
                with self.assertRaises(FileExistsError):
                    write_reports(self.report([]), directory)
                self.assertEqual(existing.read_text(), "preserve this exact content")
                self.assertFalse((directory / absent_name).exists())

    def test_repeat_generation_does_not_change_reports(self):
        paths = write_reports(self.report([{"id": "first"}]), self.directory)
        before = {key: path.read_bytes() for key, path in paths.items()}
        with self.assertRaises(FileExistsError):
            write_reports(self.report([{"id": "second"}]), self.directory)
        self.assertEqual({key: path.read_bytes() for key, path in paths.items()}, before)


if __name__ == "__main__":
    unittest.main()
