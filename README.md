# 🔄 Quick Environment Switcher

**Instantly switch between project environments with a single command.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

Stop wasting time manually activating virtual environments, changing directories, and setting environment variables! Quick Environment Switcher lets you save project configurations and switch between them instantly.

---

## ✨ Features

- **🚀 Instant Switching** - Switch projects with one command
- **🐍 Python Support** - Auto-activate virtual environments
- **🌍 Environment Variables** - Set project-specific env vars
- **🔧 Custom Commands** - Run setup scripts on switch
- **📊 Usage Tracking** - See your most-used environments
- **📝 History** - Track recent environment switches
- **🎯 Zero Dependencies** - Pure Python, no external packages
- **🖥️ Cross-Platform** - Works on Windows, Linux, and macOS

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/DonkRonk17/quick-env-switcher.git
cd quick-env-switcher

# Option 1: Run directly
python envswitch.py --help

# Option 2: Make executable (Linux/Mac)
chmod +x envswitch.py
ln -s $(pwd)/envswitch.py /usr/local/bin/envswitch

# Option 3: Add to PATH (Windows)
# Add the directory to your PATH environment variable
```

### Initialize

```bash
python envswitch.py init
```

This creates `~/.envswitch/` with your configuration.

---

## 📖 Usage

### Add an Environment

```bash
# Simple project
python envswitch.py add myproject /path/to/project

# With Python virtual environment
python envswitch.py add webapp /path/to/webapp --python /path/to/webapp/.venv

# With environment variables
python envswitch.py add api /path/to/api --env API_KEY=xyz123 --env DEBUG=true

# With custom commands
python envswitch.py add frontend /path/to/frontend --cmd "npm install" --cmd "npm run dev"

# Complete example
python envswitch.py add fullstack /path/to/project \
  --python .venv \
  --env DATABASE_URL=postgres://localhost/mydb \
  --env SECRET_KEY=mysecret \
  --cmd "echo 'Project loaded!'" \
  --desc "Full-stack web application"
```

### Switch to an Environment

```bash
python envswitch.py switch myproject
```

This generates commands to:
- Change to project directory
- Activate Python virtual environment (if configured)
- Set environment variables (if configured)
- Run custom commands (if configured)

**Copy and paste the output** into your terminal, or source it:

```bash
# Linux/Mac
source <(python envswitch.py switch myproject)

# Windows PowerShell
python envswitch.py switch myproject | Invoke-Expression
```

### List Environments

```bash
# List all environments
python envswitch.py list

# Search for specific environments
python envswitch.py list -s web
```

### View Environment Details

```bash
python envswitch.py get myproject
```

### Delete an Environment

```bash
python envswitch.py delete myproject

# Skip confirmation
python envswitch.py delete myproject -y
```

### View History

```bash
# Show last 10 switches
python envswitch.py history

# Show last 20 switches
python envswitch.py history -n 20
```

### Interactive Mode

```bash
python envswitch.py interactive
```

Guided prompts walk you through adding a new environment.

---

## 📋 Examples

### Web Development Project

```bash
python envswitch.py add mywebsite ~/projects/mywebsite \
  --python ~/projects/mywebsite/.venv \
  --env FLASK_ENV=development \
  --env DATABASE_URL=sqlite:///dev.db \
  --cmd "flask run"
```

### Data Science Project

```bash
python envswitch.py add ml-project ~/research/ml-project \
  --python ~/research/ml-project/venv \
  --env JUPYTER_PORT=8888 \
  --cmd "jupyter notebook"
```

### Microservices Setup

```bash
python envswitch.py add user-service ~/microservices/users \
  --python .venv \
  --env SERVICE_PORT=8001 \
  --env DB_NAME=users_db \
  --cmd "uvicorn app:app --reload"

python envswitch.py add order-service ~/microservices/orders \
  --python .venv \
  --env SERVICE_PORT=8002 \
  --env DB_NAME=orders_db \
  --cmd "uvicorn app:app --reload"
```

---

## 🗂️ Configuration

All configurations are stored in `~/.envswitch/`:

```
~/.envswitch/
├── environments.json    # Your environment configurations
└── history.json        # Switch history
```

### Environment Structure

Each environment includes:

- **name** - Unique identifier
- **project_path** - Absolute path to project
- **python_env** - Path to Python virtual environment (optional)
- **node_version** - Node.js version (optional, for future use)
- **env_vars** - Dictionary of environment variables
- **shell_commands** - List of commands to run on switch
- **description** - Human-readable description
- **use_count** - Number of times switched to
- **last_used** - Timestamp of last use

---

## 💡 Pro Tips

### 1. Create Aliases

Add to your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
alias sw='python /path/to/envswitch.py switch'
alias swl='python /path/to/envswitch.py list'
alias swa='python /path/to/envswitch.py add'
```

Now you can use:
```bash
sw myproject
```

### 2. Quick Switch Function (Bash/Zsh)

Add this to your shell profile:

```bash
function envswitch() {
    if [ "$1" = "to" ]; then
        eval "$(python /path/to/envswitch.py switch $2)"
    else
        python /path/to/envswitch.py "$@"
    fi
}
```

Usage:
```bash
envswitch to myproject  # Automatically executes switch
```

### 3. PowerShell Function

Add to your PowerShell profile:

```powershell
function Switch-Env {
    param([string]$name)
    python C:\path\to\envswitch.py switch $name | Invoke-Expression
}

Set-Alias sw Switch-Env
```

Usage:
```powershell
sw myproject
```

### 4. Track Your Workflow

Use `history` to see which projects you work on most:

```bash
python envswitch.py history -n 50
```

### 5. Backup Your Configuration

```bash
cp -r ~/.envswitch ~/Dropbox/envswitch-backup
```

---

## 🔧 Advanced Usage

### Templating Environment Variables

Use placeholders in your environment variables:

```bash
python envswitch.py add myapp ~/myapp \
  --env CONFIG_PATH=~/myapp/config/dev.json \
  --env LOG_FILE=~/myapp/logs/app.log
```

### Multi-Step Initialization

```bash
python envswitch.py add complex-project ~/projects/complex \
  --python .venv \
  --cmd "pip install -r requirements.txt" \
  --cmd "python manage.py migrate" \
  --cmd "npm install" \
  --cmd "npm run build"
```

### Conditional Commands

For platform-specific setups, you can manually edit `~/.envswitch/environments.json`:

```json
{
  "name": "myproject",
  "shell_commands": [
    "source setup.sh",
    "echo 'Environment ready!'"
  ]
}
```

---

## 🛠️ Troubleshooting

### Python Virtual Environment Not Activating

Make sure the path points to the environment directory (not the activate script):

```bash
# Correct
python envswitch.py add myproject /path --python /path/.venv

# Incorrect
python envswitch.py add myproject /path --python /path/.venv/bin/activate
```

### Commands Not Executing

The tool generates commands for you to copy/paste. To auto-execute:

**Linux/Mac:**
```bash
eval "$(python envswitch.py switch myproject)"
```

**Windows PowerShell:**
```powershell
python envswitch.py switch myproject | Invoke-Expression
```

### Environment Variables Not Persisting

Environment variables only last for the current shell session. To persist them, add them to your shell profile or use system environment variables.

---

## 🤝 Contributing

Contributions welcome! Ideas:

- Auto-detect virtual environments in project
- Support for Docker environments
- Support for conda environments
- Shell completion scripts
- GUI version
- Cloud sync

---

## 📜 License

MIT License - Use freely, modify freely, share freely.

---

## 👤 Author

**Randell Logan Smith**
- GitHub: [@DonkRonk17](https://github.com/DonkRonk17)
- Email: logan@metaphysicsandcomputing.com

---

## 🌟 Star This Repo!

If you find this tool useful, please star the repository! ⭐

It helps others discover the tool and motivates continued development.

---

## 🙏 Acknowledgments

Built with ❤️ to solve the daily pain of switching between projects.

---

**Happy Switching! 🚀**
