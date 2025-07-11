# AI Commit

<div align="center">

[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/ai-commit.svg)](https://badge.fury.io/py/ai-commit)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

**An intelligent CLI tool that generates meaningful commit messages for your staged Git changes using AI**

*Powered by Ollama with smart fallback mechanisms*

</div>

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [🚀 Installation](#-installation)
- [💡 Usage](#-usage)
- [⚙️ Prerequisites](#️-prerequisites)
- [🤖 Ollama Setup](#-ollama-setup)
- [🔧 How It Works](#-how-it-works)
- [📖 Example](#-example)
- [📄 License](#-license)

---

## ✨ Features

- 🤖 **AI-powered**: Uses Ollama with local LLM models (default: Mistral)
- 🔄 **Fallback system**: Works with rule-based generation when Ollama is unavailable
- 📝 **Interactive workflow**: Edit messages before committing
- 🚀 **Auto-commit**: Skip interaction with `-y` flag
- 📋 **Smart rules**: Contextual commit patterns for specific scenarios

## 🚀 Installation

### Quick Install (Recommended)

```bash
git clone https://github.com/m3/ai-commit.git
cd ai-commit
./install.sh
```

### Package Install

```bash
pip install ai-commit
```

### Manual Install

```bash
pip install -r requirements.txt
chmod +x ai_commit.py
```

## 💡 Usage

```bash
# Interactive mode
ai-commit

# Auto-commit with generated message
ai-commit -y

# Get help
ai-commit --help
```

## ⚙️ Prerequisites

- Python 3.7+
- Git repository with staged changes
- Ollama (optional, for AI-powered messages)

## 🤖 Ollama Setup

1. Install Ollama from https://ollama.ai
2. Pull the model: `ollama pull mistral`
3. Ensure Ollama is running: `ollama serve`

## 🔧 How It Works

1. **Stage your changes**: `git add <files>`
2. **Run ai-commit**: The tool analyzes your staged changes
3. **AI generation**: Uses Ollama to create a contextual commit message
4. **Review & commit**: Edit if needed, then commit with automatic push

## 📖 Example

```bash
$ git add src/auth.py
$ ai-commit

📋 Staged files:
  📝 src/auth.py

🤖 Generating commit message...

✅ Suggested commit message:
  Implement user authentication with JWT tokens

Options:
  (y) Use this message
  (e) Edit the message
  (s) Show diff
  (n) Cancel

Choose an option: y
✅ Commit created successfully!
✅ Pushed to remote repository successfully!
```

## 📄 License

MIT License - see LICENSE file for details