# Deployment Guide

## Deployment Options

### Option 1: Quick Installation (Recommended)

```bash
# Make the installation script executable and run it
chmod +x install.sh
./install.sh
```

This will:
- Install Python dependencies
- Make the script executable
- Optionally create a system-wide symlink
- Verify Ollama installation

### Option 2: Manual Installation

```bash
# Install dependencies
pip3 install -r requirements.txt

# Make script executable
chmod +x ai_commit.py

# Run from current directory
python3 ai_commit.py
```

### Option 3: Package Installation

```bash
# Install as a Python package
pip3 install .

# Now you can run 'ai-commit' from anywhere
ai-commit
```

## Deployment Verification

After deployment, verify the installation:

```bash
# Test basic functionality
ai-commit --help

# Test with staged changes
git add some_file.py
ai-commit
```

## System Requirements

- Python 3.7+
- Git repository
- `requests` Python library
- Ollama (optional, for AI-powered messages)

## Ollama Setup (Optional)

For AI-powered commit messages:

1. Install Ollama from https://ollama.ai
2. Pull the model: `ollama pull mistral`
3. Ensure Ollama is running: `ollama serve`

## Usage After Deployment

```bash
# Interactive mode
ai-commit

# Auto-commit with generated message
ai-commit -y

# Show help
ai-commit --help
```

## Rollback

To uninstall:

```bash
# Remove symlink (if created)
sudo rm /usr/local/bin/ai-commit

# Remove Python package (if installed)
pip3 uninstall ai-commit

# Remove dependencies (if no longer needed)
pip3 uninstall requests
```

## Environment-Specific Notes

- **Development**: Use `python3 ai_commit.py` directly
- **Production**: Use the package installation or symlink method
- **CI/CD**: Not applicable for this CLI tool

## Troubleshooting

- **Permission denied**: Ensure script is executable with `chmod +x`
- **Python not found**: Install Python 3.7+ and ensure it's in PATH
- **Ollama errors**: Check if Ollama is running and model is downloaded
- **Git errors**: Ensure you're in a git repository with staged changes