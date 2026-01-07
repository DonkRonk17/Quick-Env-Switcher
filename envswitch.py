#!/usr/bin/env python3
"""
Quick Environment Switcher
==========================
Instantly switch between project environments with a single command.

Author: Randell Logan Smith (DonkRonk17)
License: MIT
Repository: https://github.com/DonkRonk17/quick-env-switcher
"""

import json
import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except:
        pass

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

CONFIG_DIR = Path.home() / ".envswitch"
ENVS_FILE = CONFIG_DIR / "environments.json"
HISTORY_FILE = CONFIG_DIR / "history.json"

# ═══════════════════════════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def init_config():
    """Initialize configuration directory and files."""
    CONFIG_DIR.mkdir(exist_ok=True)
    
    if not ENVS_FILE.exists():
        ENVS_FILE.write_text(json.dumps({"environments": []}, indent=2))
        print(f"✓ Created config at {ENVS_FILE}")
    
    if not HISTORY_FILE.exists():
        HISTORY_FILE.write_text(json.dumps({"switches": []}, indent=2))
    
    return True


def load_environments():
    """Load all saved environments."""
    if not ENVS_FILE.exists():
        init_config()
    return json.loads(ENVS_FILE.read_text())


def save_environments(data):
    """Save environments to disk."""
    ENVS_FILE.write_text(json.dumps(data, indent=2))


def add_environment(name, project_path, python_env=None, node_version=None, 
                    env_vars=None, shell_commands=None, description=""):
    """Add a new environment configuration."""
    data = load_environments()
    
    # Check for duplicates
    for env in data["environments"]:
        if env["name"].lower() == name.lower():
            print(f"✗ Environment '{name}' already exists. Use 'update' to modify.")
            return False
    
    # Resolve absolute path
    project_path = str(Path(project_path).resolve())
    
    environment = {
        "name": name,
        "project_path": project_path,
        "python_env": python_env,
        "node_version": node_version,
        "env_vars": env_vars or {},
        "shell_commands": shell_commands or [],
        "description": description,
        "created": datetime.now().isoformat(),
        "last_used": None,
        "use_count": 0
    }
    
    data["environments"].append(environment)
    save_environments(data)
    print(f"✓ Added environment '{name}'")
    return True


def get_environment(name):
    """Get environment by name."""
    data = load_environments()
    
    for env in data["environments"]:
        if env["name"].lower() == name.lower():
            return env
    
    return None


def list_environments(search=None):
    """List all environments with optional search filter."""
    data = load_environments()
    envs = data["environments"]
    
    if search:
        search_lower = search.lower()
        envs = [e for e in envs if 
                search_lower in e["name"].lower() or
                search_lower in e.get("description", "").lower() or
                search_lower in e["project_path"].lower()]
    
    return envs


def delete_environment(name):
    """Delete an environment."""
    data = load_environments()
    
    for i, env in enumerate(data["environments"]):
        if env["name"].lower() == name.lower():
            env_name = env["name"]
            del data["environments"][i]
            save_environments(data)
            print(f"✓ Deleted environment '{env_name}'")
            return True
    
    print(f"✗ Environment '{name}' not found")
    return False


def switch_environment(name):
    """Generate shell commands to switch to an environment."""
    env = get_environment(name)
    
    if not env:
        print(f"✗ Environment '{name}' not found")
        return None
    
    # Update usage stats
    data = load_environments()
    for e in data["environments"]:
        if e["name"].lower() == name.lower():
            e["last_used"] = datetime.now().isoformat()
            e["use_count"] += 1
            break
    save_environments(data)
    
    # Log to history
    log_switch(name)
    
    # Generate commands
    commands = []
    
    # Change directory
    commands.append(f"cd {env['project_path']}")
    
    # Activate Python environment
    if env.get("python_env"):
        python_path = Path(env["python_env"])
        if python_path.exists():
            if sys.platform == 'win32':
                activate_script = python_path / "Scripts" / "activate.bat"
                if not activate_script.exists():
                    activate_script = python_path / "Scripts" / "Activate.ps1"
            else:
                activate_script = python_path / "bin" / "activate"
            
            if activate_script.exists():
                commands.append(f"# Activate Python environment")
                if sys.platform == 'win32':
                    commands.append(str(activate_script))
                else:
                    commands.append(f"source {activate_script}")
    
    # Set environment variables
    if env.get("env_vars"):
        commands.append("# Set environment variables")
        for key, value in env["env_vars"].items():
            if sys.platform == 'win32':
                commands.append(f'set {key}={value}')
            else:
                commands.append(f'export {key}="{value}"')
    
    # Run custom shell commands
    if env.get("shell_commands"):
        commands.append("# Custom commands")
        commands.extend(env["shell_commands"])
    
    return commands


def log_switch(env_name):
    """Log environment switch to history."""
    if not HISTORY_FILE.exists():
        init_config()
    
    history = json.loads(HISTORY_FILE.read_text())
    history["switches"].append({
        "environment": env_name,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 100 switches
    history["switches"] = history["switches"][-100:]
    
    HISTORY_FILE.write_text(json.dumps(history, indent=2))


def get_history(limit=10):
    """Get recent environment switches."""
    if not HISTORY_FILE.exists():
        return []
    
    history = json.loads(HISTORY_FILE.read_text())
    return history["switches"][-limit:]


# ═══════════════════════════════════════════════════════════════════════════════
# OUTPUT FORMATTING
# ═══════════════════════════════════════════════════════════════════════════════

def print_environment_table(environments):
    """Print environments in a nice table format."""
    if not environments:
        print("\nNo environments found.\n")
        return
    
    print("\nEnvironments:")
    print("─" * 80)
    print(f"{'Name':<20} {'Uses':<8} {'Path':<50}")
    print("─" * 80)
    
    for env in environments:
        name = env["name"][:19]
        uses = env.get("use_count", 0)
        path = env["project_path"]
        if len(path) > 49:
            path = "..." + path[-46:]
        
        print(f"{name:<20} {uses:<8} {path:<50}")
    
    print(f"\nTotal: {len(environments)} environment(s)\n")


def print_environment_detail(env):
    """Print detailed environment information."""
    print("\n" + "═" * 60)
    print(f"  {env['name']}")
    print("═" * 60)
    print(f"  Path:     {env['project_path']}")
    
    if env.get("python_env"):
        print(f"  Python:   {env['python_env']}")
    
    if env.get("node_version"):
        print(f"  Node:     {env['node_version']}")
    
    if env.get("env_vars"):
        print(f"  Env Vars: {len(env['env_vars'])} variable(s)")
        for key, value in env["env_vars"].items():
            print(f"    • {key}={value}")
    
    if env.get("shell_commands"):
        print(f"  Commands: {len(env['shell_commands'])} command(s)")
        for cmd in env["shell_commands"]:
            print(f"    • {cmd}")
    
    if env.get("description"):
        print(f"  Description: {env['description']}")
    
    print(f"  Uses:     {env.get('use_count', 0)}")
    
    if env.get("last_used"):
        print(f"  Last:     {env['last_used'][:19]}")
    
    print("═" * 60 + "\n")


def print_switch_script(commands, name):
    """Print the switch commands."""
    print(f"\n# Switching to environment: {name}")
    print("# Copy and paste these commands or run: envswitch exec {name}\n")
    
    for cmd in commands:
        print(cmd)
    
    print()


# ═══════════════════════════════════════════════════════════════════════════════
# INTERACTIVE MODE
# ═══════════════════════════════════════════════════════════════════════════════

def interactive_add():
    """Interactive environment addition."""
    print("\n📦 Add New Environment")
    print("─" * 40)
    
    name = input("Name: ").strip()
    if not name:
        print("✗ Name is required")
        return
    
    project_path = input("Project path: ").strip()
    if not project_path:
        print("✗ Project path is required")
        return
    
    python_env = input("Python venv path (optional): ").strip() or None
    node_version = input("Node version (optional): ").strip() or None
    description = input("Description (optional): ").strip()
    
    # Environment variables
    env_vars = {}
    print("\nEnvironment variables (press Enter to skip):")
    while True:
        var = input("  Variable name (or Enter to finish): ").strip()
        if not var:
            break
        value = input(f"  Value for {var}: ").strip()
        env_vars[var] = value
    
    # Shell commands
    shell_commands = []
    print("\nShell commands to run on switch (press Enter to skip):")
    while True:
        cmd = input("  Command (or Enter to finish): ").strip()
        if not cmd:
            break
        shell_commands.append(cmd)
    
    add_environment(name, project_path, python_env, node_version, 
                    env_vars if env_vars else None,
                    shell_commands if shell_commands else None,
                    description)


# ═══════════════════════════════════════════════════════════════════════════════
# CLI INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Quick Environment Switcher - Switch between project environments instantly",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  envswitch add myproject /path/to/project --python .venv
  envswitch switch myproject
  envswitch list
  envswitch interactive
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Init command
    subparsers.add_parser("init", help="Initialize configuration")
    
    # Add command
    add_parser = subparsers.add_parser("add", help="Add new environment")
    add_parser.add_argument("name", help="Environment name")
    add_parser.add_argument("path", help="Project path")
    add_parser.add_argument("--python", help="Python venv path")
    add_parser.add_argument("--node", help="Node version")
    add_parser.add_argument("--env", action="append", help="Environment variable KEY=VALUE")
    add_parser.add_argument("--cmd", action="append", help="Shell command to run")
    add_parser.add_argument("--desc", help="Description")
    
    # Switch command
    switch_parser = subparsers.add_parser("switch", help="Switch to environment")
    switch_parser.add_argument("name", help="Environment name")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List environments")
    list_parser.add_argument("-s", "--search", help="Search filter")
    
    # Get command
    get_parser = subparsers.add_parser("get", help="Get environment details")
    get_parser.add_argument("name", help="Environment name")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete environment")
    delete_parser.add_argument("name", help="Environment name")
    delete_parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    
    # History command
    history_parser = subparsers.add_parser("history", help="Show recent switches")
    history_parser.add_argument("-n", "--limit", type=int, default=10, help="Number of entries")
    
    # Interactive command
    subparsers.add_parser("interactive", help="Interactive mode")
    
    args = parser.parse_args()
    
    # Initialize on first run
    if not CONFIG_DIR.exists():
        init_config()
    
    # Handle commands
    if args.command == "init":
        init_config()
        print("✓ Configuration initialized!")
    
    elif args.command == "add":
        env_vars = {}
        if args.env:
            for e in args.env:
                if '=' in e:
                    key, value = e.split('=', 1)
                    env_vars[key.strip()] = value.strip()
        
        add_environment(
            args.name, 
            args.path, 
            python_env=args.python,
            node_version=args.node,
            env_vars=env_vars if env_vars else None,
            shell_commands=args.cmd,
            description=args.desc or ""
        )
    
    elif args.command == "switch":
        commands = switch_environment(args.name)
        if commands:
            print_switch_script(commands, args.name)
    
    elif args.command == "list":
        environments = list_environments(search=args.search)
        print_environment_table(environments)
    
    elif args.command == "get":
        env = get_environment(args.name)
        if env:
            print_environment_detail(env)
        else:
            print(f"✗ Environment '{args.name}' not found")
    
    elif args.command == "delete":
        if not args.yes:
            confirm = input(f"Delete environment '{args.name}'? [y/N]: ")
            if confirm.lower() != 'y':
                print("Cancelled")
                return
        delete_environment(args.name)
    
    elif args.command == "history":
        history = get_history(args.limit)
        if history:
            print("\nRecent switches:")
            print("─" * 60)
            for entry in history:
                print(f"{entry['timestamp'][:19]} - {entry['environment']}")
            print()
        else:
            print("\nNo history yet.\n")
    
    elif args.command == "interactive":
        interactive_add()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
