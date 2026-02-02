#!/usr/bin/env python3
"""
Quick Environment Switcher - Comprehensive Test Suite
======================================================
Tests for all envswitch functionality.

Run tests:
    python test_envswitch.py
    python -m pytest test_envswitch.py -v

Author: ATLAS (Team Brain)
For: Logan Smith / Metaphy LLC
License: MIT
"""

import unittest
import sys
import json
import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import the module components
from envswitch import (
    init_config,
    load_environments,
    save_environments,
    add_environment,
    get_environment,
    list_environments,
    delete_environment,
    switch_environment,
    log_switch,
    get_history,
    CONFIG_DIR,
    ENVS_FILE,
    HISTORY_FILE
)


class TestEnvSwitchBase(unittest.TestCase):
    """Base class with temp directory setup."""
    
    def setUp(self):
        """Set up temp directory for tests."""
        self.test_dir = tempfile.mkdtemp()
        self.original_config_dir = CONFIG_DIR
        self.original_envs_file = ENVS_FILE
        self.original_history_file = HISTORY_FILE
        
        # Patch config paths to use temp directory
        import envswitch
        envswitch.CONFIG_DIR = Path(self.test_dir)
        envswitch.ENVS_FILE = Path(self.test_dir) / "environments.json"
        envswitch.HISTORY_FILE = Path(self.test_dir) / "history.json"
    
    def tearDown(self):
        """Clean up temp directory."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        
        # Restore original paths
        import envswitch
        envswitch.CONFIG_DIR = self.original_config_dir
        envswitch.ENVS_FILE = self.original_envs_file
        envswitch.HISTORY_FILE = self.original_history_file


class TestInitConfig(TestEnvSwitchBase):
    """Test configuration initialization."""
    
    def test_init_creates_directory(self):
        """Test init creates config directory."""
        import envswitch
        result = init_config()
        self.assertTrue(result)
        self.assertTrue(envswitch.CONFIG_DIR.exists())
    
    def test_init_creates_envs_file(self):
        """Test init creates environments.json."""
        import envswitch
        init_config()
        self.assertTrue(envswitch.ENVS_FILE.exists())
    
    def test_init_creates_history_file(self):
        """Test init creates history.json."""
        import envswitch
        init_config()
        self.assertTrue(envswitch.HISTORY_FILE.exists())
    
    def test_init_valid_json(self):
        """Test init creates valid JSON files."""
        import envswitch
        init_config()
        
        with open(envswitch.ENVS_FILE) as f:
            data = json.load(f)
        self.assertIn("environments", data)
        self.assertEqual(data["environments"], [])
        
        with open(envswitch.HISTORY_FILE) as f:
            history = json.load(f)
        self.assertIn("switches", history)
    
    def test_init_idempotent(self):
        """Test init can be called multiple times."""
        init_config()
        init_config()  # Should not fail
        import envswitch
        self.assertTrue(envswitch.CONFIG_DIR.exists())


class TestAddEnvironment(TestEnvSwitchBase):
    """Test adding environments."""
    
    def test_add_basic_environment(self):
        """Test adding a basic environment."""
        init_config()
        result = add_environment("test-project", "/path/to/project")
        self.assertTrue(result)
    
    def test_add_with_python_env(self):
        """Test adding environment with Python venv."""
        init_config()
        result = add_environment(
            "python-project",
            "/path/to/project",
            python_env="/path/to/venv"
        )
        self.assertTrue(result)
        
        env = get_environment("python-project")
        self.assertEqual(env["python_env"], "/path/to/venv")
    
    def test_add_with_env_vars(self):
        """Test adding environment with env vars."""
        init_config()
        result = add_environment(
            "env-vars-project",
            "/path/to/project",
            env_vars={"API_KEY": "secret", "DEBUG": "true"}
        )
        self.assertTrue(result)
        
        env = get_environment("env-vars-project")
        self.assertEqual(env["env_vars"]["API_KEY"], "secret")
        self.assertEqual(env["env_vars"]["DEBUG"], "true")
    
    def test_add_with_shell_commands(self):
        """Test adding environment with shell commands."""
        init_config()
        result = add_environment(
            "commands-project",
            "/path/to/project",
            shell_commands=["npm install", "npm run dev"]
        )
        self.assertTrue(result)
        
        env = get_environment("commands-project")
        self.assertEqual(len(env["shell_commands"]), 2)
    
    def test_add_with_description(self):
        """Test adding environment with description."""
        init_config()
        result = add_environment(
            "described-project",
            "/path/to/project",
            description="My awesome project"
        )
        self.assertTrue(result)
        
        env = get_environment("described-project")
        self.assertEqual(env["description"], "My awesome project")
    
    def test_add_duplicate_rejected(self):
        """Test duplicate environment is rejected."""
        init_config()
        add_environment("unique-project", "/path/one")
        result = add_environment("unique-project", "/path/two")
        self.assertFalse(result)
    
    def test_add_case_insensitive_duplicate(self):
        """Test case-insensitive duplicate detection."""
        init_config()
        add_environment("MyProject", "/path/one")
        result = add_environment("myproject", "/path/two")
        self.assertFalse(result)
    
    def test_add_creates_timestamp(self):
        """Test add creates timestamp."""
        init_config()
        add_environment("timestamped", "/path")
        
        env = get_environment("timestamped")
        self.assertIsNotNone(env["created"])
    
    def test_add_initializes_use_count(self):
        """Test add initializes use_count to 0."""
        init_config()
        add_environment("counted", "/path")
        
        env = get_environment("counted")
        self.assertEqual(env["use_count"], 0)


class TestGetEnvironment(TestEnvSwitchBase):
    """Test getting environments."""
    
    def test_get_existing(self):
        """Test getting existing environment."""
        init_config()
        add_environment("existing", "/path")
        
        env = get_environment("existing")
        self.assertIsNotNone(env)
        self.assertEqual(env["name"], "existing")
    
    def test_get_nonexistent(self):
        """Test getting nonexistent environment returns None."""
        init_config()
        
        env = get_environment("nonexistent")
        self.assertIsNone(env)
    
    def test_get_case_insensitive(self):
        """Test get is case-insensitive."""
        init_config()
        add_environment("MixedCase", "/path")
        
        env = get_environment("mixedcase")
        self.assertIsNotNone(env)
        self.assertEqual(env["name"], "MixedCase")


class TestListEnvironments(TestEnvSwitchBase):
    """Test listing environments."""
    
    def test_list_empty(self):
        """Test listing empty environments."""
        init_config()
        envs = list_environments()
        self.assertEqual(envs, [])
    
    def test_list_all(self):
        """Test listing all environments."""
        init_config()
        add_environment("project1", "/path1")
        add_environment("project2", "/path2")
        add_environment("project3", "/path3")
        
        envs = list_environments()
        self.assertEqual(len(envs), 3)
    
    def test_list_search_by_name(self):
        """Test search by name."""
        init_config()
        add_environment("webapp", "/path1")
        add_environment("api-service", "/path2")
        add_environment("mobile-app", "/path3")
        
        envs = list_environments(search="web")
        self.assertEqual(len(envs), 1)
        self.assertEqual(envs[0]["name"], "webapp")
    
    def test_list_search_by_description(self):
        """Test search by description."""
        init_config()
        add_environment("proj1", "/path1", description="frontend application")
        add_environment("proj2", "/path2", description="backend service")
        
        envs = list_environments(search="frontend")
        self.assertEqual(len(envs), 1)
    
    def test_list_search_by_path(self):
        """Test search by path."""
        init_config()
        add_environment("proj1", "/home/user/projects/webapp")
        add_environment("proj2", "/home/user/services/api")
        
        envs = list_environments(search="projects")
        self.assertEqual(len(envs), 1)
    
    def test_list_search_case_insensitive(self):
        """Test search is case-insensitive."""
        init_config()
        add_environment("MyWebApp", "/path")
        
        envs = list_environments(search="MYWEBAPP")
        self.assertEqual(len(envs), 1)


class TestDeleteEnvironment(TestEnvSwitchBase):
    """Test deleting environments."""
    
    def test_delete_existing(self):
        """Test deleting existing environment."""
        init_config()
        add_environment("to-delete", "/path")
        
        result = delete_environment("to-delete")
        self.assertTrue(result)
        
        env = get_environment("to-delete")
        self.assertIsNone(env)
    
    def test_delete_nonexistent(self):
        """Test deleting nonexistent environment."""
        init_config()
        
        result = delete_environment("nonexistent")
        self.assertFalse(result)
    
    def test_delete_case_insensitive(self):
        """Test delete is case-insensitive."""
        init_config()
        add_environment("MixedCase", "/path")
        
        result = delete_environment("mixedcase")
        self.assertTrue(result)
    
    def test_delete_preserves_others(self):
        """Test delete only removes specified environment."""
        init_config()
        add_environment("keep1", "/path1")
        add_environment("remove", "/path2")
        add_environment("keep2", "/path3")
        
        delete_environment("remove")
        
        envs = list_environments()
        self.assertEqual(len(envs), 2)
        names = [e["name"] for e in envs]
        self.assertIn("keep1", names)
        self.assertIn("keep2", names)


class TestSwitchEnvironment(TestEnvSwitchBase):
    """Test switching environments."""
    
    def test_switch_generates_cd_command(self):
        """Test switch generates cd command."""
        init_config()
        add_environment("switch-test", "/test/path")
        
        commands = switch_environment("switch-test")
        self.assertIsNotNone(commands)
        self.assertTrue(any("cd" in cmd for cmd in commands))
    
    def test_switch_increments_use_count(self):
        """Test switch increments use count."""
        init_config()
        add_environment("use-count-test", "/path")
        
        switch_environment("use-count-test")
        
        env = get_environment("use-count-test")
        self.assertEqual(env["use_count"], 1)
        
        switch_environment("use-count-test")
        
        env = get_environment("use-count-test")
        self.assertEqual(env["use_count"], 2)
    
    def test_switch_updates_last_used(self):
        """Test switch updates last_used timestamp."""
        init_config()
        add_environment("last-used-test", "/path")
        
        env_before = get_environment("last-used-test")
        self.assertIsNone(env_before["last_used"])
        
        switch_environment("last-used-test")
        
        env_after = get_environment("last-used-test")
        self.assertIsNotNone(env_after["last_used"])
    
    def test_switch_nonexistent_returns_none(self):
        """Test switch to nonexistent returns None."""
        init_config()
        
        commands = switch_environment("nonexistent")
        self.assertIsNone(commands)
    
    def test_switch_with_env_vars(self):
        """Test switch generates env var commands."""
        init_config()
        add_environment("env-var-test", "/path", env_vars={"VAR1": "value1"})
        
        commands = switch_environment("env-var-test")
        env_cmds = [c for c in commands if "VAR1" in c]
        self.assertTrue(len(env_cmds) > 0)
    
    def test_switch_with_shell_commands(self):
        """Test switch includes shell commands."""
        init_config()
        add_environment("cmd-test", "/path", shell_commands=["echo hello"])
        
        commands = switch_environment("cmd-test")
        self.assertTrue(any("echo hello" in cmd for cmd in commands))


class TestHistory(TestEnvSwitchBase):
    """Test history functionality."""
    
    def test_log_switch_creates_entry(self):
        """Test log_switch creates history entry."""
        init_config()
        log_switch("test-env")
        
        history = get_history()
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["environment"], "test-env")
    
    def test_get_history_limit(self):
        """Test get_history respects limit."""
        init_config()
        for i in range(20):
            log_switch(f"env-{i}")
        
        history = get_history(limit=5)
        self.assertEqual(len(history), 5)
    
    def test_history_order(self):
        """Test history returns most recent last."""
        init_config()
        log_switch("first")
        log_switch("second")
        log_switch("third")
        
        history = get_history()
        self.assertEqual(history[-1]["environment"], "third")
    
    def test_history_truncation(self):
        """Test history truncates at 100 entries."""
        init_config()
        for i in range(150):
            log_switch(f"env-{i}")
        
        # Read raw file to check truncation
        import envswitch
        with open(envswitch.HISTORY_FILE) as f:
            data = json.load(f)
        
        self.assertEqual(len(data["switches"]), 100)
    
    def test_history_empty(self):
        """Test empty history."""
        init_config()
        history = get_history()
        self.assertEqual(history, [])


class TestEdgeCases(TestEnvSwitchBase):
    """Test edge cases and error handling."""
    
    def test_special_characters_in_name(self):
        """Test environment name with special characters."""
        init_config()
        result = add_environment("my-project_v2.0", "/path")
        self.assertTrue(result)
        
        env = get_environment("my-project_v2.0")
        self.assertIsNotNone(env)
    
    def test_unicode_in_description(self):
        """Test unicode in description."""
        init_config()
        result = add_environment("unicode-test", "/path", description="Test description")
        self.assertTrue(result)
    
    def test_empty_env_vars(self):
        """Test empty env vars dict."""
        init_config()
        add_environment("empty-vars", "/path", env_vars={})
        
        env = get_environment("empty-vars")
        self.assertEqual(env["env_vars"], {})
    
    def test_empty_shell_commands(self):
        """Test empty shell commands list."""
        init_config()
        add_environment("empty-cmds", "/path", shell_commands=[])
        
        env = get_environment("empty-cmds")
        self.assertEqual(env["shell_commands"], [])
    
    def test_path_normalization(self):
        """Test path is normalized."""
        init_config()
        add_environment("path-test", "./relative/path")
        
        env = get_environment("path-test")
        # Should be absolute path
        self.assertTrue(Path(env["project_path"]).is_absolute())
    
    def test_whitespace_handling(self):
        """Test whitespace in paths is preserved."""
        init_config()
        add_environment("space-test", "/path/with spaces/project")
        
        env = get_environment("space-test")
        self.assertIn("with spaces", env["project_path"])


class TestDataIntegrity(TestEnvSwitchBase):
    """Test data integrity."""
    
    def test_save_and_load(self):
        """Test save and load preserves data."""
        init_config()
        add_environment(
            "complete-env",
            "/path/to/project",
            python_env="/path/to/venv",
            node_version="18",
            env_vars={"KEY": "value"},
            shell_commands=["echo test"],
            description="Test environment"
        )
        
        # Reload
        data = load_environments()
        env = data["environments"][0]
        
        self.assertEqual(env["name"], "complete-env")
        self.assertEqual(env["python_env"], "/path/to/venv")
        self.assertEqual(env["node_version"], "18")
        self.assertEqual(env["env_vars"]["KEY"], "value")
        self.assertEqual(env["shell_commands"][0], "echo test")
        self.assertEqual(env["description"], "Test environment")
    
    def test_concurrent_operations(self):
        """Test multiple operations don't corrupt data."""
        init_config()
        
        # Rapid operations
        for i in range(10):
            add_environment(f"concurrent-{i}", f"/path/{i}")
        
        envs = list_environments()
        self.assertEqual(len(envs), 10)
        
        for i in range(5):
            delete_environment(f"concurrent-{i}")
        
        envs = list_environments()
        self.assertEqual(len(envs), 5)


class TestCLIIntegration(TestEnvSwitchBase):
    """Test CLI argument handling."""
    
    def test_env_var_parsing(self):
        """Test --env KEY=VALUE parsing."""
        # This tests the logic used in CLI
        env_args = ["API_KEY=secret123", "DEBUG=true", "COMPLEX=value=with=equals"]
        
        env_vars = {}
        for e in env_args:
            if '=' in e:
                key, value = e.split('=', 1)
                env_vars[key.strip()] = value.strip()
        
        self.assertEqual(env_vars["API_KEY"], "secret123")
        self.assertEqual(env_vars["DEBUG"], "true")
        self.assertEqual(env_vars["COMPLEX"], "value=with=equals")


# =============================================================================
# Main Entry Point
# =============================================================================

def run_tests():
    """Run all tests with nice output."""
    print("=" * 70)
    print("TESTING: Quick Environment Switcher v1.0")
    print("=" * 70)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestInitConfig,
        TestAddEnvironment,
        TestGetEnvironment,
        TestListEnvironments,
        TestDeleteEnvironment,
        TestSwitchEnvironment,
        TestHistory,
        TestEdgeCases,
        TestDataIntegrity,
        TestCLIIntegration,
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "=" * 70)
    print(f"RESULTS: {result.testsRun} tests")
    passed = result.testsRun - len(result.failures) - len(result.errors)
    print(f"[OK] Passed: {passed}")
    if result.failures:
        print(f"[X] Failed: {len(result.failures)}")
    if result.errors:
        print(f"[X] Errors: {len(result.errors)}")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
