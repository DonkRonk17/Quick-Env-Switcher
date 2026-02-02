# Quick Environment Switcher - Integration Plan

## Overview

This document outlines how Quick Environment Switcher integrates with:
1. Team Brain agents (Forge, Atlas, Clio, Nexus, Bolt)
2. Existing Team Brain tools
3. BCH (Beacon Command Hub) - future integration
4. Logan's development workflows

---

## BCH Integration

### Current Status
**Not yet integrated with BCH** - Quick Environment Switcher operates at the shell level, outside of BCH's command structure.

### Future Integration Potential

```
@envswitch list                    # List all environments
@envswitch switch myproject        # Switch to environment
@envswitch add name path           # Add new environment
```

### Implementation Notes
- BCH could call envswitch.py directly via subprocess
- Environment switches affect the shell, not BCH session
- Better suited as a standalone CLI tool

---

## AI Agent Integration

### Integration Matrix

| Agent | Use Case | Integration Method | Priority |
|-------|----------|-------------------|----------|
| **Forge** | Orchestrate project contexts | CLI/Python API | HIGH |
| **Atlas** | Switch to tool build environments | CLI/Python API | HIGH |
| **Clio** | Linux project switching | CLI (bash) | HIGH |
| **Nexus** | Cross-platform switching | CLI/Python API | MEDIUM |
| **Bolt** | Batch environment operations | CLI | MEDIUM |

### Agent-Specific Workflows

#### Forge (Orchestrator / Reviewer)

**Primary Use Case:** Switch between different project contexts when reviewing or orchestrating work.

**Integration Steps:**
1. Create environments for each major project
2. Switch when changing context
3. Log switches for session tracking

**Example Workflow:**
```python
from envswitch import switch_environment, list_environments

# Review what environments are available
envs = list_environments()
print(f"Available: {[e['name'] for e in envs]}")

# Switch to BCH project for review
commands = switch_environment("bch-backend")
# Commands would be executed in shell
```

#### Atlas (Executor / Builder)

**Primary Use Case:** Switch to appropriate environment when building/testing tools.

**Integration Steps:**
1. Create environment for each tool in development
2. Switch when starting new tool build
3. Track which environment was used for which tool

**Example Workflow:**
```python
from envswitch import add_environment, switch_environment

# Add new tool environment
add_environment(
    "new-tool-dev",
    "/path/to/AutoProjects/NewTool",
    python_env="/path/to/AutoProjects/NewTool/.venv",
    env_vars={"DEBUG": "true"},
    description="NewTool development environment"
)

# Switch to it
commands = switch_environment("new-tool-dev")
```

#### Clio (Linux / Ubuntu Agent)

**Primary Use Case:** Manage multiple Linux project environments.

**Platform Considerations:**
- Uses bash/zsh shells
- May have multiple Python versions
- Docker environments common

**Example:**
```bash
# Add environment
python envswitch.py add abios-dev ~/ABIOS \
    --python ~/ABIOS/.venv \
    --env ENVIRONMENT=development \
    --cmd "echo 'ABIOS development ready'"

# Switch (auto-execute)
eval "$(python envswitch.py switch abios-dev)"
```

#### Nexus (Multi-Platform Agent)

**Primary Use Case:** Manage environments across Windows, Linux, macOS.

**Cross-Platform Notes:**
- Use Python API for consistency
- Path normalization handled automatically
- Environment variables use platform-appropriate syntax

**Example:**
```python
import platform
from envswitch import add_environment

# Platform-aware environment setup
if platform.system() == "Windows":
    venv_path = "C:/Projects/webapp/.venv"
else:
    venv_path = "/home/user/projects/webapp/.venv"

add_environment("webapp", "/path/to/webapp", python_env=venv_path)
```

#### Bolt (Cline / Free Executor)

**Primary Use Case:** Batch operations, repetitive environment setups.

**Cost Considerations:**
- No API costs for CLI usage
- Can process multiple environments in batch

**Example:**
```bash
# Batch add multiple microservices
for service in users orders products payments; do
    python envswitch.py add "$service-svc" ~/microservices/$service \
        --python ~/microservices/$service/.venv \
        --env SERVICE_NAME=$service
done
```

---

## Integration with Other Team Brain Tools

### With AgentHealth

**Correlation Use Case:** Track which environment an agent is working in during health monitoring.

**Integration Pattern:**
```python
from agenthealth import AgentHealth
from envswitch import switch_environment, get_environment

health = AgentHealth()

# Start session
session_id = health.start_session("ATLAS")

# Get current environment for context
current_env = get_environment("bch-backend")
if current_env:
    health.log_context(session_id, f"Environment: {current_env['name']}")

# Work...

health.end_session("ATLAS", session_id)
```

### With SynapseLink

**Notification Use Case:** Notify team when switching to critical environments.

**Integration Pattern:**
```python
from synapselink import quick_send
from envswitch import switch_environment

env_name = "production-deployment"
commands = switch_environment(env_name)

if commands:
    quick_send(
        "FORGE,LOGAN",
        f"Environment Switch: {env_name}",
        f"ATLAS switching to production environment.\n"
        f"Commands: {len(commands)} to execute.",
        priority="HIGH"
    )
```

### With SessionReplay

**Debugging Use Case:** Record environment switches for session replay.

**Integration Pattern:**
```python
from sessionreplay import SessionReplay
from envswitch import switch_environment, get_history

replay = SessionReplay()
session_id = replay.start_session("ATLAS", "Debugging production issue")

# Log environment context
history = get_history(limit=5)
replay.log_context(session_id, f"Recent switches: {history}")

# Switch and log
commands = switch_environment("debug-env")
replay.log_tool_call(session_id, "envswitch", f"switch debug-env -> {commands}")

replay.end_session(session_id)
```

### With TaskQueuePro

**Task Management Use Case:** Associate tasks with specific environments.

**Integration Pattern:**
```python
from taskqueuepro import TaskQueuePro
from envswitch import switch_environment

queue = TaskQueuePro()

# Create task with environment metadata
task_id = queue.create_task(
    title="Fix authentication bug",
    agent="ATLAS",
    metadata={
        "environment": "auth-service",
        "requires_switch": True
    }
)

# When starting task, switch to correct environment
task = queue.get_task(task_id)
if task["metadata"].get("requires_switch"):
    commands = switch_environment(task["metadata"]["environment"])
    # Execute commands...

queue.start_task(task_id)
```

### With MemoryBridge

**Context Persistence Use Case:** Remember frequently used environments.

**Integration Pattern:**
```python
from memorybridge import MemoryBridge
from envswitch import list_environments, get_history

memory = MemoryBridge()

# Save current environment state for future sessions
env_state = {
    "environments": list_environments(),
    "recent_history": get_history(limit=20),
    "timestamp": datetime.now().isoformat()
}

memory.set("envswitch_state", env_state)
memory.sync()
```

### With ConfigManager

**Configuration Use Case:** Centralize environment configurations.

**Integration Pattern:**
```python
from configmanager import ConfigManager
from envswitch import add_environment

config = ConfigManager()

# Load predefined environments from central config
env_templates = config.get("envswitch.templates", {})

for name, template in env_templates.items():
    add_environment(
        name=name,
        project_path=template["path"],
        python_env=template.get("python"),
        env_vars=template.get("env_vars"),
        description=template.get("description")
    )
```

### With DevSnapshot

**Snapshot Use Case:** Include current environment in development snapshots.

**Integration Pattern:**
```python
from devsnapshot import DevSnapshot
from envswitch import get_environment, get_history

snapshot = DevSnapshot()

# Add environment context to snapshot
current_env = get_environment("current-project")
snapshot.add_context("environment", current_env)
snapshot.add_context("env_history", get_history(limit=5))

snapshot.capture()
```

---

## Adoption Roadmap

### Phase 1: Core Adoption (Week 1)
**Goal:** All agents aware and can use basic features

**Steps:**
1. [x] Tool deployed to GitHub
2. [ ] Quick-start guides sent via Synapse
3. [ ] Each agent tests basic workflow
4. [ ] Feedback collected

**Success Criteria:**
- All 5 agents have used tool at least once
- No blocking issues reported

### Phase 2: Integration (Week 2-3)
**Goal:** Integrated into daily workflows

**Steps:**
1. [ ] Add to agent startup routines
2. [ ] Create integration examples with existing tools
3. [ ] Update agent-specific workflows
4. [ ] Monitor usage patterns

**Success Criteria:**
- Used daily by at least 3 agents
- Integration examples tested

### Phase 3: Optimization (Week 4+)
**Goal:** Optimized and fully adopted

**Steps:**
1. [ ] Collect efficiency metrics
2. [ ] Implement v1.1 improvements
3. [ ] Create advanced workflow examples
4. [ ] Full Team Brain ecosystem integration

**Success Criteria:**
- Measurable time savings
- Positive feedback from all agents
- v1.1 improvements identified

---

## Success Metrics

**Adoption Metrics:**
- Number of agents using tool: Target 5/5
- Daily usage count: Track via history
- Number of environments per agent: Track

**Efficiency Metrics:**
- Time saved per switch: ~30 seconds vs manual
- Context switch errors reduced: Qualitative
- Environment consistency: Track via get_history()

**Quality Metrics:**
- Bug reports: Track in GitHub issues
- Feature requests: Collect from agents
- User satisfaction: Qualitative feedback

---

## Technical Integration Details

### Import Paths
```python
# Standard import
from envswitch import (
    init_config,
    add_environment,
    get_environment,
    list_environments,
    delete_environment,
    switch_environment,
    get_history
)
```

### Configuration Files
**Location:** `~/.envswitch/`

**Shared Config Integration:**
```json
{
  "envswitch": {
    "default_python": "/path/to/default/venv",
    "auto_log_to_synapse": true,
    "max_history": 100
  }
}
```

### Error Handling
**Standardized Exit Codes:**
- 0: Success
- 1: General error
- 2: Environment not found
- 3: Invalid configuration

### Logging Integration
**Log Format:** Compatible with Team Brain standard logging
**Log Location:** Via shell output, not file-based

---

## Maintenance & Support

### Update Strategy
- Minor updates (v1.x): As needed
- Major updates (v2.0+): Quarterly
- Security patches: Immediate

### Support Channels
- GitHub Issues: Bug reports
- Synapse: Team Brain discussions
- Direct: Complex issues

### Known Limitations
- Cannot auto-execute shell commands (generates for copy/paste)
- Environment variables only last for shell session
- No cloud sync (manual backup required)

---

## Additional Resources

- Main Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Quick Start Guides: [QUICK_START_GUIDES.md](QUICK_START_GUIDES.md)
- GitHub: https://github.com/DonkRonk17/quick-env-switcher

---

**Last Updated:** February 2026
**Maintained By:** ATLAS (Team Brain)
