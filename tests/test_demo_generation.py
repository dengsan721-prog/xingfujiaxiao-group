import re
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
        self.assertRegex(html, re.compile(r"copySignin|只复制签到"))
        self.assertRegex(html, re.compile(r"copyGame|只复制小游戏"))
        self.assertRegex(html, re.compile(r"copyHomework|只复制作业"))

    def test_demo_uses_logo_asset(self):
        html = DEMO.read_text(encoding="utf-8")
        self.assertTrue(LOGO.exists())
        self.assertIn("assets/xingfu-yizhan-logo.png", html)

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
        self.assertIn("upload-pages-artifact", workflow)
        self.assertIn("deploy-pages", workflow)


if __name__ == "__main__":
    unittest.main()
