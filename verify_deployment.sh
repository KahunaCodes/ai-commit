#!/bin/bash

# Deployment Verification Script
# Tests that the AI commit tool is properly deployed

echo "🔍 Verifying AI Commit Tool deployment..."

# Check if Python3 is available
if command -v python3 &> /dev/null; then
    echo "✅ Python3 is available"
    python3 --version
else
    echo "❌ Python3 not found"
    exit 1
fi

# Check if the main script exists and is executable
if [[ -x "ai_commit.py" ]]; then
    echo "✅ ai_commit.py is executable"
else
    echo "❌ ai_commit.py is not executable"
    exit 1
fi

# Check if dependencies are installed
if python3 -c "import requests" 2>/dev/null; then
    echo "✅ requests library is installed"
else
    echo "❌ requests library is missing"
    echo "Run: pip3 install -r requirements.txt"
    exit 1
fi

# Check if we're in a git repository
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo "✅ Git repository detected"
else
    echo "⚠️  Not in a git repository (this is okay for deployment verification)"
fi

# Check if symlink exists
if [[ -L "/usr/local/bin/ai-commit" ]]; then
    echo "✅ System-wide symlink exists"
    echo "   You can run 'ai-commit' from anywhere"
else
    echo "ℹ️  No system-wide symlink (you can still run locally)"
fi

# Check Ollama installation
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    if ollama list | grep -q "mistral"; then
        echo "✅ Mistral model is available"
    else
        echo "⚠️  Mistral model not found. Run 'ollama pull mistral' to download it."
    fi
else
    echo "⚠️  Ollama not found. The tool will use fallback message generation."
fi

echo ""
echo "🎉 Deployment verification complete!"
echo ""
echo "Next steps:"
echo "1. Stage some changes: git add <files>"
echo "2. Run the tool: python3 ai_commit.py"
echo "   (or 'ai-commit' if symlink was created)"