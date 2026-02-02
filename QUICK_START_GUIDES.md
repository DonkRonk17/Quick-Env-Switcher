# Quick Environment Switcher - Quick Start Guides

## About These Guides

Each Team Brain agent has a **5-minute quick-start guide** tailored to their role and workflows.

**Choose your guide:**
- [Forge (Orchestrator)](#forge-quick-start)
- [Atlas (Executor)](#atlas-quick-start)
- [Clio (Linux Agent)](#clio-quick-start)
- [Nexus (Multi-Platform)](#nexus-quick-start)
- [Bolt (Free Executor)](#bolt-quick-start)

---

## Forge Quick Start

**Role:** Orchestrator / Reviewer  
**Time:** 5 minutes  
**Goal:** Learn to use Quick Environment Switcher for context management

### Step 1: Installation Check
```bash
# Verify tool is available
cd C:\Users\logan\OneDrive\Documents\AutoProjects\quick-env-switcher
python envswitch.py --help

# Initialize (first time only)
python envswitch.py init
```

### Step 2: First Use - Project Context Switching
```bash
# Add your main projects
python envswitch.py add bch-review D:\BEACON_HQ\PROJECTS\00_ACTIVE\BCH_APPS --desc "BCH project review"
python envswitch.py add tools-review C:\Users\logan\OneDrive\Documents\AutoProjects --desc "Tool review workspace"

# List environments
python envswitch.py list
```

### Step 3: Switching for Reviews
```bash
# When starting BCH review
python envswitch.py switch bch-review
# Copy and paste the generated commands

# When switching to tool review
python envswitch.py switch tools-review
```

### Step 4: Common Forge Commands
```bash
# See all environments
python envswitch.py list

# Get details on specific project
python envswitch.py get bch-review

# Check recent switches
python envswitch.py history
```

### Next Steps for Forge
1. Add environments for each major project you review
2. Use before starting reviews to ensure correct context
3. Check history to track work patterns

---

## Atlas Quick Start

**Role:** Executor / Builder  
**Time:** 5 minutes  
**Goal:** Learn to use Quick Environment Switcher for tool building

### Step 1: Installation Check
```bash
cd C:\Users\logan\OneDrive\Documents\AutoProjects\quick-env-switcher
python envswitch.py init
python envswitch.py --help
```

### Step 2: First Use - Tool Development Environments
```bash
# Add environment for current tool build
python envswitch.py add current-tool C:\Users\logan\OneDrive\Documents\AutoProjects\CurrentTool \
    --desc "Current tool in development"

# Add with Python venv
python envswitch.py add tool-with-venv /path/to/tool \
    --python /path/to/tool/.venv \
    --desc "Tool with virtual environment"
```

### Step 3: Tool Build Workflow
```python
# In your build session
from envswitch import add_environment, switch_environment

# Create environment for new tool
add_environment(
    "new-tool",
    "C:/Users/logan/OneDrive/Documents/AutoProjects/NewTool",
    description="Building NewTool - Day 1"
)

# Get switch commands
commands = switch_environment("new-tool")
print(commands)  # Execute these in shell
```

### Step 4: Common Atlas Commands
```bash
# Add new tool environment quickly
python envswitch.py add TOOLNAME /path/to/tool --desc "Description"

# Switch to tool
python envswitch.py switch TOOLNAME

# Delete when tool is complete
python envswitch.py delete TOOLNAME -y
```

### Next Steps for Atlas
1. Create environment at start of each tool build
2. Include in session logs which environment was used
3. Delete environment when tool is complete (optional)

---

## Clio Quick Start

**Role:** Linux / Ubuntu Agent  
**Time:** 5 minutes  
**Goal:** Learn to use Quick Environment Switcher in Linux environment

### Step 1: Linux Installation
```bash
# Clone from GitHub
git clone https://github.com/DonkRonk17/quick-env-switcher.git
cd quick-env-switcher

# Make executable (optional)
chmod +x envswitch.py

# Initialize
python3 envswitch.py init
```

### Step 2: First Use - Linux Project Setup
```bash
# Add ABIOS environment
python3 envswitch.py add abios ~/ABIOS \
    --python ~/ABIOS/.venv \
    --env ENVIRONMENT=development \
    --desc "ABIOS development"

# Add with shell commands
python3 envswitch.py add backend ~/backend \
    --python ~/backend/.venv \
    --cmd "docker-compose up -d" \
    --desc "Backend with Docker"
```

### Step 3: Auto-Execute Switching
```bash
# Add to ~/.bashrc for auto-execute
function sw() {
    eval "$(python3 ~/quick-env-switcher/envswitch.py switch $1)"
}

# Then use:
sw abios  # Switches instantly!
```

### Step 4: Common Clio Commands
```bash
# List all environments
python3 envswitch.py list

# Search for specific ones
python3 envswitch.py list -s docker

# Check history
python3 envswitch.py history -n 20
```

### Platform-Specific Tips for Clio
- Use `python3` explicitly
- Add shell function to `.bashrc` for auto-execute
- Environment variables use `export` syntax
- Paths are case-sensitive

### Next Steps for Clio
1. Add to `.bashrc` for persistent aliases
2. Create environments for each major project
3. Use `--cmd` for project-specific startup scripts

---

## Nexus Quick Start

**Role:** Multi-Platform Agent  
**Time:** 5 minutes  
**Goal:** Learn cross-platform usage of Quick Environment Switcher

### Step 1: Platform Detection
```python
import platform
print(f"Current platform: {platform.system()}")  # Windows, Linux, or Darwin

# The tool works the same on all platforms
from envswitch import init_config, add_environment
init_config()
```

### Step 2: First Use - Cross-Platform Projects
```python
import platform
from pathlib import Path
from envswitch import add_environment

# Platform-aware path handling
if platform.system() == "Windows":
    project_path = Path("C:/Projects/webapp")
    venv_path = project_path / ".venv"
else:
    project_path = Path.home() / "projects" / "webapp"
    venv_path = project_path / ".venv"

add_environment(
    "webapp",
    str(project_path),
    python_env=str(venv_path) if venv_path.exists() else None,
    description="Web application project"
)
```

### Step 3: Cross-Platform Considerations
```python
from envswitch import switch_environment

commands = switch_environment("webapp")
# Commands are platform-appropriate:
# - Windows: uses 'set' for env vars
# - Linux/Mac: uses 'export' for env vars
# - Windows: uses Scripts/activate.bat
# - Linux/Mac: uses bin/activate
```

### Step 4: Common Nexus Commands
```bash
# Same commands work on all platforms
python envswitch.py list
python envswitch.py switch webapp
python envswitch.py get webapp
```

### Platform-Specific Notes

**Windows:**
- Use forward slashes in paths (works in Python)
- PowerShell: `python envswitch.py switch name | Invoke-Expression`

**Linux/Mac:**
- Use `python3` if needed
- Bash/Zsh: `eval "$(python envswitch.py switch name)"`

### Next Steps for Nexus
1. Test on all target platforms
2. Use Python API for platform-independent code
3. Report any platform-specific issues

---

## Bolt Quick Start

**Role:** Free Executor (Cline + Grok)  
**Time:** 5 minutes  
**Goal:** Learn to use Quick Environment Switcher without API costs

### Step 1: Verify Free Access
```bash
# No API key required!
# No external dependencies!
python envswitch.py --version
python envswitch.py init
```

### Step 2: First Use - Batch Operations
```bash
# Add multiple environments in batch
python envswitch.py add project1 /path/to/project1 --desc "Project 1"
python envswitch.py add project2 /path/to/project2 --desc "Project 2"
python envswitch.py add project3 /path/to/project3 --desc "Project 3"
```

### Step 3: Batch Scripting
```bash
# Create multiple microservice environments
#!/bin/bash
for service in users orders products payments; do
    python envswitch.py add "${service}-svc" ~/services/$service \
        --python ~/services/$service/.venv \
        --env SERVICE_NAME=$service \
        --desc "Microservice: $service"
done

echo "Created $(python envswitch.py list | grep -c 'svc') service environments"
```

### Step 4: Common Bolt Commands
```bash
# Bulk list
python envswitch.py list

# Bulk delete (with confirmation skip)
python envswitch.py delete old-project -y

# Export current config (for backup)
cat ~/.envswitch/environments.json
```

### Cost Considerations for Bolt
- Tool is 100% free - no API calls
- Runs locally, no cloud required
- Can be used for unlimited operations

### Next Steps for Bolt
1. Use for repetitive setup tasks
2. Create batch scripts for common patterns
3. Back up `~/.envswitch/` periodically

---

## Additional Resources

**For All Agents:**
- Full Documentation: [README.md](README.md)
- Examples: [EXAMPLES.md](EXAMPLES.md)
- Integration Plan: [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md)
- Cheat Sheet: [CHEAT_SHEET.txt](CHEAT_SHEET.txt)

**Support:**
- GitHub Issues: https://github.com/DonkRonk17/quick-env-switcher/issues
- Synapse: Post in THE_SYNAPSE/active/
- Direct: Message ATLAS

---

**Last Updated:** February 2026
**Maintained By:** ATLAS (Team Brain)
