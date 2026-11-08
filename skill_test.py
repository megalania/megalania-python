import json
import pathlib
import re
import tomllib
import unittest

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COPIES = [HERE / "megalania/skill", HERE / "plugin/skills/megalania"]


class Skill(unittest.TestCase):
    def test_reference_lists_every_mcp_tool_in_order(self):
        tools = [t["name"] for t in json.loads((ROOT / "docs/api/mcp-tools.json").read_text())]
        ref = (COPIES[0] / "reference.md").read_text()
        self.assertEqual(re.findall(r"^## (\w+)$", ref, re.M), tools)

    def test_front_matter_limits(self):
        text = (COPIES[0] / "SKILL.md").read_text()
        head = text.split("---\n")[1]
        meta = dict(line.split(": ", 1) for line in head.strip().splitlines())
        self.assertRegex(meta["name"], r"^[a-z0-9-]{1,64}$")
        self.assertLessEqual(len(meta["description"]), 1024)
        self.assertIn("reference.md", text)

    def test_both_copies_identical(self):
        for name in ("SKILL.md", "reference.md"):
            self.assertEqual((COPIES[0] / name).read_text(), (COPIES[1] / name).read_text(), name)

    def test_plugin_version_equals_sdk_version(self):
        sdk = tomllib.loads((HERE / "pyproject.toml").read_text())["project"]["version"]
        plugin = json.loads((HERE / "plugin/.claude-plugin/plugin.json").read_text())
        market = json.loads((HERE / ".claude-plugin/marketplace.json").read_text())
        self.assertEqual(plugin["version"], sdk)
        self.assertEqual([p["source"] for p in market["plugins"]], ["./plugin"])
        mcp = json.loads((HERE / "plugin/.mcp.json").read_text())
        self.assertEqual(mcp["mcpServers"]["megalania"]["url"], "https://mcp.megalania.io/")


if __name__ == "__main__":
    unittest.main()
