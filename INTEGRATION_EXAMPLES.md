# Quick Environment Switcher - Integration Examples

## Integration Philosophy

Quick Environment Switcher is designed to work seamlessly with other Team Brain tools. This document provides **copy-paste-ready code examples** for common integration patterns.

---

## Table of Contents

1. [Pattern 1: EnvSwitch + AgentHealth](#pattern-1-envswitch--agenthealth)
2. [Pattern 2: EnvSwitch + SynapseLink](#pattern-2-envswitch--synapselink)
3. [Pattern 3: EnvSwitch + TaskQueuePro](#pattern-3-envswitch--taskqueuepro)
4. [Pattern 4: EnvSwitch + MemoryBridge](#pattern-4-envswitch--memorybridge)
5. [Pattern 5: EnvSwitch + SessionReplay](#pattern-5-envswitch--sessionreplay)
6. [Pattern 6: EnvSwitch + DevSnapshot](#pattern-6-envswitch--devsnapshot)
7. [Pattern 7: EnvSwitch + ConfigManager](#pattern-7-envswitch--configmanager)
8. [Pattern 8: EnvSwitch + TokenTracker](#pattern-8-envswitch--tokentracker)
9. [Pattern 9: Multi-Tool Workflow](#pattern-9-multi-tool-workflow)
10. [Pattern 10: Full Team Brain Stack](#pattern-10-full-team-brain-stack)

---

## Pattern 1: EnvSwitch + AgentHealth

**Use Case:** Track which environment an agent is working in during health monitoring

**Why:** Correlate environment switches with agent activity and performance

**Code:**

```python
from agenthealth import AgentHealth
from envswitch import switch_environment, get_environment, get_history

# Initialize both tools
health = AgentHealth()

# Start session
session_id = health.start_session("ATLAS")

# Get current environment context
current_env = get_environment("my-project")
if current_env:
    health.log_context(session_id, {
        "environment": current_env["name"],
        "project_path": current_env["project_path"],
        "use_count": current_env["use_count"]
    })

# Switch environment and log
commands = switch_environment("new-project")
health.heartbeat("ATLAS", status="switching_environment")

# Do work...

# End session
health.end_session("ATLAS", session_id)
```

**Result:** Health logs include environment context for better debugging

---

## Pattern 2: EnvSwitch + SynapseLink

**Use Case:** Notify Team Brain when switching to important environments

**Why:** Keep team informed of critical context changes

**Code:**

```python
from synapselink import quick_send
from envswitch import switch_environment, get_environment

def switch_with_notification(env_name, notify_team=False, priority="NORMAL"):
    """Switch environment with optional team notification."""
    
    env = get_environment(env_name)
    if not env:
        print(f"Environment '{env_name}' not found")
        return None
    
    commands = switch_environment(env_name)
    
    if notify_team and commands:
        quick_send(
            "TEAM",
            f"Environment Switch: {env_name}",
            f"Agent switching to: {env_name}\n"
            f"Path: {env['project_path']}\n"
            f"Use count: {env.get('use_count', 0) + 1}",
            priority=priority
        )
    
    return commands

# Usage
switch_with_notification("production-deploy", notify_team=True, priority="HIGH")
```

**Result:** Team stays informed of important environment changes

---

## Pattern 3: EnvSwitch + TaskQueuePro

**Use Case:** Associate tasks with specific environments

**Why:** Ensure tasks run in correct environment context

**Code:**

```python
from taskqueuepro import TaskQueuePro
from envswitch import add_environment, switch_environment, get_environment

queue = TaskQueuePro()

# Create task with environment requirement
task_id = queue.create_task(
    title="Fix database migration",
    agent="ATLAS",
    priority=1,
    metadata={
        "required_environment": "backend-dev",
        "auto_switch": True
    }
)

# When starting task
task = queue.get_task(task_id)
queue.start_task(task_id)

if task["metadata"].get("auto_switch"):
    env_name = task["metadata"]["required_environment"]
    
    # Ensure environment exists
    if not get_environment(env_name):
        add_environment(env_name, "/path/to/project", description="Auto-created for task")
    
    # Switch
    commands = switch_environment(env_name)
    print(f"Execute these commands:\n{chr(10).join(commands)}")

# Complete task
queue.complete_task(task_id, result="Migration fixed")
```

**Result:** Tasks automatically linked to correct environments

---

## Pattern 4: EnvSwitch + MemoryBridge

**Use Case:** Persist environment state across sessions

**Why:** Remember environment configurations and usage patterns

**Code:**

```python
from memorybridge import MemoryBridge
from envswitch import list_environments, get_history
from datetime import datetime

memory = MemoryBridge()

def save_environment_state():
    """Save current environment state to memory."""
    state = {
        "environments": list_environments(),
        "recent_switches": get_history(limit=20),
        "saved_at": datetime.now().isoformat()
    }
    memory.set("envswitch_state", state)
    memory.sync()
    return state

def get_most_used_environments(limit=5):
    """Get most frequently used environments."""
    envs = list_environments()
    sorted_envs = sorted(envs, key=lambda x: x.get("use_count", 0), reverse=True)
    return sorted_envs[:limit]

def load_environment_recommendations():
    """Load and analyze environment usage patterns."""
    state = memory.get("envswitch_state", {})
    if not state:
        return []
    
    # Analyze patterns
    recent = state.get("recent_switches", [])
    env_counts = {}
    for switch in recent:
        env = switch["environment"]
        env_counts[env] = env_counts.get(env, 0) + 1
    
    return sorted(env_counts.items(), key=lambda x: x[1], reverse=True)

# Usage
save_environment_state()
recommendations = load_environment_recommendations()
print(f"Most used environments: {recommendations}")
```

**Result:** Persistent environment analytics and recommendations

---

## Pattern 5: EnvSwitch + SessionReplay

**Use Case:** Record environment switches for debugging

**Why:** Replay sessions with full environment context

**Code:**

```python
from sessionreplay import SessionReplay
from envswitch import switch_environment, get_environment, get_history

replay = SessionReplay()

# Start recording session
session_id = replay.start_session("ATLAS", task="Debug API issue")

# Log initial environment state
initial_history = get_history(limit=5)
replay.log_context(session_id, f"Recent env switches: {initial_history}")

# Record environment switch
env_name = "api-debug"
replay.log_input(session_id, f"Switching to environment: {env_name}")

commands = switch_environment(env_name)
replay.log_tool_call(session_id, "envswitch", {
    "action": "switch",
    "environment": env_name,
    "commands_generated": len(commands)
})

replay.log_output(session_id, f"Generated {len(commands)} commands")

# Do debugging work...

# End session
replay.end_session(session_id, status="RESOLVED")
```

**Result:** Full session replay with environment context

---

## Pattern 6: EnvSwitch + DevSnapshot

**Use Case:** Include environment in development snapshots

**Why:** Complete context capture for later reference

**Code:**

```python
from devsnapshot import DevSnapshot
from envswitch import get_environment, list_environments, get_history

snapshot = DevSnapshot()

def capture_with_environment(snapshot_name, env_name=None):
    """Capture development snapshot with environment context."""
    
    # Add environment context
    if env_name:
        env = get_environment(env_name)
        if env:
            snapshot.add_context("current_environment", env)
    
    # Add all environments for reference
    snapshot.add_context("all_environments", list_environments())
    
    # Add recent switch history
    snapshot.add_context("env_history", get_history(limit=10))
    
    # Capture snapshot
    result = snapshot.capture(name=snapshot_name)
    return result

# Usage
capture_with_environment("pre-refactor-snapshot", env_name="webapp")
```

**Result:** Development snapshots include full environment context

---

## Pattern 7: EnvSwitch + ConfigManager

**Use Case:** Centralize environment configurations

**Why:** Manage environment templates across team

**Code:**

```python
from configmanager import ConfigManager
from envswitch import add_environment, list_environments

config = ConfigManager()

def setup_environments_from_config():
    """Set up environments from central config."""
    
    templates = config.get("envswitch.templates", {
        "development": {
            "suffix": "-dev",
            "env_vars": {"DEBUG": "true", "LOG_LEVEL": "debug"}
        },
        "staging": {
            "suffix": "-staging",
            "env_vars": {"DEBUG": "false", "LOG_LEVEL": "info"}
        },
        "production": {
            "suffix": "-prod",
            "env_vars": {"DEBUG": "false", "LOG_LEVEL": "error"}
        }
    })
    
    base_projects = config.get("envswitch.projects", [
        {"name": "webapp", "path": "/projects/webapp"},
        {"name": "api", "path": "/projects/api"}
    ])
    
    created = []
    for project in base_projects:
        for env_type, template in templates.items():
            env_name = f"{project['name']}{template['suffix']}"
            
            # Skip if already exists
            if any(e["name"] == env_name for e in list_environments()):
                continue
            
            add_environment(
                env_name,
                project["path"],
                env_vars=template["env_vars"],
                description=f"{project['name']} {env_type} environment"
            )
            created.append(env_name)
    
    return created

# Usage
new_envs = setup_environments_from_config()
print(f"Created environments: {new_envs}")
```

**Result:** Consistent environment setup from central config

---

## Pattern 8: EnvSwitch + TokenTracker

**Use Case:** Track environment switches in token usage context

**Why:** Correlate API usage with environment context

**Code:**

```python
from tokentracker import TokenTracker
from envswitch import switch_environment, get_environment

tracker = TokenTracker()

def switch_with_tracking(env_name, agent_name="ATLAS"):
    """Switch environment with token tracking context."""
    
    env = get_environment(env_name)
    commands = switch_environment(env_name)
    
    if commands:
        # Log the context switch (no actual tokens used - local operation)
        tracker.log_operation(
            agent=agent_name,
            operation="environment_switch",
            context={
                "environment": env_name,
                "commands_count": len(commands),
                "tokens_used": 0  # Local operation, no API cost
            }
        )
    
    return commands

# Usage
switch_with_tracking("api-service", "ATLAS")
```

**Result:** Complete operational tracking including environment context

---

## Pattern 9: Multi-Tool Workflow

**Use Case:** Complete workflow using multiple tools with environment context

**Why:** Demonstrate real production scenario

**Code:**

```python
from taskqueuepro import TaskQueuePro
from sessionreplay import SessionReplay
from agenthealth import AgentHealth
from synapselink import quick_send
from envswitch import switch_environment, get_environment, add_environment

def complete_task_workflow(task_title, env_name, agent="ATLAS"):
    """Complete task workflow with full tool integration."""
    
    # Initialize tools
    queue = TaskQueuePro()
    replay = SessionReplay()
    health = AgentHealth()
    
    # 1. Create task
    task_id = queue.create_task(
        title=task_title,
        agent=agent,
        metadata={"environment": env_name}
    )
    
    # 2. Start session recording
    session_id = replay.start_session(agent, task=task_title)
    
    # 3. Start health tracking
    health.start_session(agent, session_id=session_id)
    
    # 4. Ensure environment exists
    if not get_environment(env_name):
        add_environment(env_name, f"/projects/{env_name}", 
                       description=f"Auto-created for: {task_title}")
    
    # 5. Switch environment
    commands = switch_environment(env_name)
    replay.log_tool_call(session_id, "envswitch", {"switch": env_name})
    
    try:
        # 6. Start task
        queue.start_task(task_id)
        health.heartbeat(agent, status="working")
        
        # Do actual work here...
        
        # 7. Complete successfully
        queue.complete_task(task_id, result="Completed")
        replay.end_session(session_id, status="COMPLETED")
        health.end_session(agent, session_id=session_id, status="success")
        
        quick_send("TEAM", f"Task Complete: {task_title}", 
                  f"Completed in environment: {env_name}")
        
        return True
        
    except Exception as e:
        # Handle failure
        queue.fail_task(task_id, error=str(e))
        replay.log_error(session_id, str(e))
        replay.end_session(session_id, status="FAILED")
        health.log_error(agent, str(e))
        health.end_session(agent, session_id=session_id, status="failed")
        
        quick_send("FORGE", f"Task Failed: {task_title}", str(e), priority="HIGH")
        
        return False

# Usage
complete_task_workflow("Fix authentication bug", "auth-service")
```

**Result:** Fully instrumented, environment-aware workflow

---

## Pattern 10: Full Team Brain Stack

**Use Case:** Ultimate integration - all tools working together

**Why:** Production-grade agent operation with environment management

**Code:**

```python
"""
Full Team Brain Stack Integration Example
=========================================

This demonstrates how EnvSwitch integrates with the complete
Team Brain tool ecosystem for production-grade workflows.
"""

import json
from datetime import datetime
from pathlib import Path

# Tool imports
from envswitch import (
    init_config, add_environment, get_environment,
    list_environments, switch_environment, get_history
)

# Team Brain tools (install from AutoProjects)
# from agenthealth import AgentHealth
# from synapselink import quick_send
# from taskqueuepro import TaskQueuePro
# from sessionreplay import SessionReplay
# from memorybridge import MemoryBridge
# from configmanager import ConfigManager
# from tokentracker import TokenTracker
# from devsnapshot import DevSnapshot


class TeamBrainWorkflow:
    """Orchestrates Team Brain tools with environment awareness."""
    
    def __init__(self, agent_name="ATLAS"):
        self.agent = agent_name
        self.session_id = None
        self.current_env = None
        
        # Initialize envswitch
        init_config()
    
    def start_workflow(self, task_name, env_name):
        """Start a tracked workflow in specific environment."""
        
        # 1. Set up environment
        if not get_environment(env_name):
            print(f"Creating environment: {env_name}")
            add_environment(env_name, f"/projects/{env_name}")
        
        # 2. Switch to environment
        self.current_env = env_name
        commands = switch_environment(env_name)
        print(f"Switch commands:\n{chr(10).join(commands)}")
        
        # 3. Log session start
        self.session_id = f"{self.agent}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"Started workflow: {task_name}")
        print(f"Session ID: {self.session_id}")
        print(f"Environment: {env_name}")
        
        return self.session_id
    
    def checkpoint(self, message):
        """Log a checkpoint in the workflow."""
        print(f"[{self.session_id}] Checkpoint: {message}")
        print(f"  Environment: {self.current_env}")
    
    def switch_environment(self, new_env):
        """Switch to different environment mid-workflow."""
        old_env = self.current_env
        commands = switch_environment(new_env)
        self.current_env = new_env
        
        print(f"Switched: {old_env} -> {new_env}")
        return commands
    
    def end_workflow(self, status="success"):
        """End the tracked workflow."""
        # Get usage stats
        env = get_environment(self.current_env)
        history = get_history(limit=5)
        
        print(f"\nWorkflow Complete")
        print(f"  Status: {status}")
        print(f"  Environment: {self.current_env}")
        print(f"  Use count: {env.get('use_count', 0) if env else 0}")
        print(f"  Recent switches: {len(history)}")
        
        self.session_id = None
        return status
    
    def get_environment_stats(self):
        """Get statistics on environment usage."""
        envs = list_environments()
        history = get_history(limit=100)
        
        stats = {
            "total_environments": len(envs),
            "total_switches": len(history),
            "most_used": sorted(envs, key=lambda x: x.get("use_count", 0), reverse=True)[:3],
            "current": self.current_env
        }
        
        return stats


# Example usage
if __name__ == "__main__":
    # Create workflow instance
    workflow = TeamBrainWorkflow("ATLAS")
    
    # Start workflow in specific environment
    workflow.start_workflow("Build new API endpoint", "api-backend")
    
    # Do work with checkpoints
    workflow.checkpoint("Created endpoint skeleton")
    workflow.checkpoint("Added validation")
    workflow.checkpoint("Wrote tests")
    
    # Maybe switch environment for integration testing
    workflow.switch_environment("integration-test")
    workflow.checkpoint("Running integration tests")
    
    # End workflow
    workflow.end_workflow("success")
    
    # Get stats
    stats = workflow.get_environment_stats()
    print(f"\nEnvironment Stats: {json.dumps(stats, indent=2, default=str)}")
```

**Result:** Complete, production-ready workflow with environment management

---

## Recommended Integration Priority

**Week 1 (Essential):**
1. AgentHealth - Health correlation
2. SynapseLink - Team notifications
3. SessionReplay - Debugging

**Week 2 (Productivity):**
4. TaskQueuePro - Task management
5. MemoryBridge - Data persistence
6. ConfigManager - Configuration

**Week 3 (Advanced):**
7. TokenTracker - Usage tracking
8. DevSnapshot - Snapshot capture
9. Full stack integration

---

## Troubleshooting Integrations

**Import Errors:**
```python
import sys
from pathlib import Path

# Add AutoProjects to path
sys.path.append(str(Path.home() / "OneDrive/Documents/AutoProjects"))

# Then import
from envswitch import switch_environment
```

**Version Conflicts:**
```bash
# Check versions
python envswitch.py --version

# Update
cd AutoProjects/quick-env-switcher
git pull origin master
```

**Configuration Issues:**
```bash
# Reset configuration
rm -rf ~/.envswitch
python envswitch.py init
```

---

**Last Updated:** February 2026
**Maintained By:** ATLAS (Team Brain)
