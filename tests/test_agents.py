import importlib.util
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


CLI = Path(__file__).resolve().parents[1] / "tools" / "agents.py"
SPEC = importlib.util.spec_from_file_location("agents", CLI)
agents = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(agents)


class AgentsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()

    def put(self, path, content):
        destination = self.root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        return destination

    def skill(self, role, name="example", body="SELECTED_SKILL_BODY"):
        return self.put(f".AGENTS/{role}/skills/{name}/SKILL.md",
                        f"---\nname: {name}\ndescription: A useful test skill.\n---\n\n{body}\n")

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(CLI), "--root", str(self.root), *args],
                              capture_output=True, text=True, encoding="utf-8")

    def test_initialize_and_check_real_cli(self):
        result = self.run_cli("init")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(agents.check(self.root), ["developer", "reviewer"])
        self.assertEqual([p.name for p in (self.root / ".AGENTS/developer/memory").iterdir()], ["MEMORY.md"])
        self.assertEqual(self.run_cli("check").returncode, 0)

    def test_init_preserves_existing_bytes_and_custom_role(self):
        entry = self.put("AGENTS.md", "# 用户约定\nKeep me.\n")
        role = self.put(".AGENTS/developer/AGENTS.md", "CUSTOM_ROLE_INSTRUCTIONS\n")
        memory = self.put(".AGENTS/developer/memory/MEMORY.md", "CUSTOM_MEMORY\n")
        before = {p: p.read_bytes() for p in (entry, role, memory)}
        for _ in range(2):
            result = self.run_cli("init", "--roles", "developer", "qa")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("AGENTS.md preserved", result.stdout)
        for path, content in before.items():
            self.assertEqual(path.read_bytes(), content)
        self.assertEqual(agents.check(self.root), ["developer", "qa"])
        self.assertIn("CUSTOM_ROLE_INSTRUCTIONS", agents.context(self.root, "developer"))

    def test_role_isolation_and_progressive_loading(self):
        agents.init(self.root, ["developer", "reviewer"])
        self.skill("developer")
        self.skill("reviewer", body="OTHER_ROLE_SKILL")
        self.put(".AGENTS/reviewer/memory/MEMORY.md", "OTHER_ROLE_MEMORY")
        self.put(".AGENTS/developer/memory/MEMORY.md", "SELECTED_ROLE_MEMORY")
        default = agents.context(self.root, "developer")
        self.assertIn("example: A useful test skill.", default)
        self.assertIn("SELECTED_ROLE_MEMORY", default)
        for marker in ("SELECTED_SKILL_BODY", "OTHER_ROLE_MEMORY", "OTHER_ROLE_SKILL"):
            self.assertNotIn(marker, default)
        selected = agents.context(self.root, "developer", ["example"])
        self.assertIn("SELECTED_SKILL_BODY", selected)
        self.assertIn("SELECTED_ROLE_MEMORY", selected)
        self.assertNotIn("OTHER_ROLE_MEMORY", selected)
        self.assertNotIn("OTHER_ROLE_SKILL", selected)

    def test_invalid_names_rejected_before_init_writes(self):
        for name in ("../escape", "a/b", "a\\b", "UPPER", "_shared", "", "-role", "role-", "nul", "com1", "a" * 64):
            with self.subTest(name=name), self.assertRaises(ValueError):
                agents.init(self.root, ["developer", name])
        self.assertEqual(list(self.root.iterdir()), [])

    def test_missing_role_and_skill_are_errors(self):
        agents.init(self.root, ["developer"])
        for args in (("context", "missing"), ("context", "developer", "--skill", "missing")):
            result = self.run_cli(*args)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("error:", result.stderr)
            self.assertEqual(result.stdout, "")

    def test_check_catches_missing_and_empty_required_files(self):
        agents.init(self.root, ["developer"])
        role = self.root / ".AGENTS/developer/AGENTS.md"
        role.write_text(" \n", encoding="utf-8")
        self.assertNotEqual(self.run_cli("check").returncode, 0)
        role.unlink()
        self.assertNotEqual(self.run_cli("check").returncode, 0)

    def test_skill_metadata_errors(self):
        agents.init(self.root, ["developer"])
        path = self.skill("developer")
        for content in ("No frontmatter", "---\nname: wrong\ndescription: Test\n---\nBody",
                        "---\nname: example\ndescription: ''\n---\nBody",
                        "---\nname: example\nname: example\ndescription: Test\n---\nBody"):
            path.write_text(content, encoding="utf-8")
            with self.subTest(content=content), self.assertRaises(ValueError):
                agents.check(self.root)

    def test_empty_memory_fails_check(self):
        agents.init(self.root, ["developer"])
        self.put(".AGENTS/developer/memory/MEMORY.md", "")
        with self.assertRaises(ValueError):
            agents.check(self.root)

    def test_linked_directory_is_not_read_or_written(self):
        with tempfile.TemporaryDirectory() as outside:
            external = Path(outside).resolve()
            marker = external / "CONTEXT.md"
            marker.write_text("OUTSIDE_SECRET", encoding="utf-8")
            base = self.root / ".AGENTS"
            base.mkdir()
            link = base / "_shared"
            try:
                link.symlink_to(external, target_is_directory=True)
            except OSError:
                if sys.platform != "win32":
                    self.skipTest("Symlinks are unavailable")
                result = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(external)],
                                        capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
            self.addCleanup(link.unlink if link.is_symlink() else link.rmdir)
            with self.assertRaises(ValueError):
                agents.init(self.root, ["developer"])
            self.assertEqual(marker.read_text(encoding="utf-8"), "OUTSIDE_SECRET")
            self.assertEqual(sorted(p.name for p in external.iterdir()), ["CONTEXT.md"])
            with self.assertRaises(ValueError):
                agents.read(self.root, ".AGENTS/_shared/CONTEXT.md")

    def test_single_file_can_initialize_new_project_from_elsewhere(self):
        with tempfile.TemporaryDirectory() as folder:
            copied = Path(folder) / "agents.py"
            copied.write_bytes(CLI.read_bytes())
            target = Path(folder) / "new project"
            result = subprocess.run([sys.executable, str(copied), "--root", str(target), "init"],
                                    cwd=folder, capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(agents.check(target), ["developer", "reviewer"])

    @unittest.skipUnless(sys.platform == "win32", "Windows short-path aliases")
    def test_windows_short_path_root(self):
        import ctypes
        long_path = self.root / "project directory with spaces"
        long_path.mkdir()
        buffer = ctypes.create_unicode_buffer(32768)
        size = ctypes.windll.kernel32.GetShortPathNameW(str(long_path), buffer, len(buffer))
        if not size or size >= len(buffer) or buffer.value == str(long_path):
            self.skipTest("8.3 short names are unavailable on this volume")
        short_root = Path(buffer.value) / "new project"
        agents.init(short_root, ["developer"])
        self.assertEqual(agents.check(short_root), ["developer"])
        self.assertTrue((long_path / "new project/AGENTS.md").is_file())


if __name__ == "__main__":
    unittest.main()
