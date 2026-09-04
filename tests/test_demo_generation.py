import re
import struct
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "demo" / "index.html"
LOGO = ROOT / "demo" / "assets" / "xingfu-yizhan-logo.png"
ROOT_INDEX = ROOT / "index.html"
PAGES_WORKFLOW = ROOT / ".github" / "workflows" / "pages.yml"


class DemoGenerationTest(unittest.TestCase):
    def test_demo_contains_five_themes_and_fourteen_days_each(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertIn("董事长（孩子）长成记 群发助手", html)
        for theme in ["我能自己做主", "学习不靠硬撑", "情绪来了我不炸", "输一次也没关系", "会说话也会相处"]:
            self.assertIn(theme, html)
        self.assertEqual(html.count("\"subtitle\":"), 5)
        self.assertEqual(html.count("\"title\":"), 70)

    def test_demo_has_copyable_group_message_parts(self):
        html = DEMO.read_text(encoding="utf-8")
        for label in ["今日小角色", "今天签到", "今天 1 分钟", "5 个可以聊的话题", "群里互动小游戏", "今天小作业", "教练收口"]:
            self.assertIn(label, html)
        self.assertRegex(html, re.compile(r"copyFull|复制当天全文"))

    def test_demo_uses_logo_asset(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertTrue(LOGO.exists())
        self.assertIn("assets/xingfu-yizhan-logo.png", html)
        with LOGO.open("rb") as logo_file:
            logo_file.seek(16)
            width, height = struct.unpack(">II", logo_file.read(8))
        self.assertGreater(width, height * 2)

    def test_demo_links_each_source_to_dachun_audio_detail(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertEqual(html.count('"sourceUrl":'), 70)
        self.assertIn("https://www.dachun.tv/pages/home/audioDetail/audioDetail?audioId=", html)
        self.assertIn("去听原文", html)
        self.assertIn("source-link", html)

    def test_demo_has_polished_mobile_visual_shell(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertIn("brand-card", html)
        self.assertIn("quick-actions", html)
        self.assertIn("backdrop-filter", html)

    def test_demo_mobile_layout_prioritizes_phone_use(self):
        html = DEMO.read_text(encoding="utf-8")
        for expected in [
            "touch-action: manipulation",
            "scroll-margin-top: 12px",
            "grid-template-columns: repeat(7, minmax(36px, 1fr))",
            "#copyFull",
            "grid-column: 1 / -1",
            "white-space: nowrap",
            "box-shadow: none",
            "display: none",
        ]:
            self.assertIn(expected, html)
        self.assertNotIn("white-space: pre-wrap", html)

    def test_mobile_header_and_actions_focus_on_title_and_full_copy(self):
        html = DEMO.read_text(encoding="utf-8")
        for expected in [
            "width: min(52vw, 180px)",
            "font-size: 22px",
            "font-weight: 800",
            "select-shell",
            "appearance: none",
        ]:
            self.assertIn(expected, html)
        for removed in ["copySignin", "copyGame", "copyHomework"]:
            self.assertNotIn(removed, html)

    def test_demo_header_omits_activity_label(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertNotIn("14 天群发成长活动", html)

    def test_each_message_section_has_copy_button(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertIn("copy-section-btn", html)
        self.assertIn("data-copy-key", html)
        self.assertIn("copySection", html)

    def test_copy_has_local_file_fallback(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertIn("navigator.clipboard", html)
        self.assertIn("document.execCommand", html)

    def test_repo_has_mobile_browsing_entrypoint(self):
        html = ROOT_INDEX.read_text(encoding="utf-8")
        self.assertIn("viewport", html)
        self.assertIn("demo/index.html", html)
        self.assertIn("董事长（孩子）长成记 群发助手", html)

    def test_github_pages_workflow_publishes_static_site(self):
        workflow = PAGES_WORKFLOW.read_text(encoding="utf-8")
        self.assertIn("github-pages", workflow)
        self.assertIn("enablement: true", workflow)
        self.assertIn("upload-pages-artifact", workflow)
        self.assertIn("deploy-pages", workflow)


if __name__ == "__main__":
    unittest.main()
