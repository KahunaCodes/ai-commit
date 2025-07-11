#!/bin/bash

# AI Commit Tool Installation Script
# This script deploys the AI commit tool for local use

set -e

echo "🚀 Deploying AI Commit Tool..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed. Please install Python3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is required but not installed. Please install pip3 first."
    exit 1
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Make the script executable
echo "🔧 Making ai_commit.py executable..."
chmod +x ai_commit.py

# Create symlink for system-wide access (optional)
read -p "🔗 Create system-wide symlink? This allows running 'ai-commit' from anywhere (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    SYMLINK_PATH="/usr/local/bin/ai-commit"
    
    if [[ -L "$SYMLINK_PATH" ]]; then
        echo "🗑️  Removing existing symlink..."
        sudo rm "$SYMLINK_PATH"
    fi
    
    echo "🔗 Creating symlink: $SYMLINK_PATH -> $SCRIPT_DIR/ai_commit.py"
    sudo ln -s "$SCRIPT_DIR/ai_commit.py" "$SYMLINK_PATH"
    
    echo "✅ You can now run 'ai-commit' from anywhere!"
else
    echo "ℹ️  You can run the tool with: python3 $(pwd)/ai_commit.py"
fi

# Verify Ollama installation (optional)
echo "🤖 Checking Ollama installation..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama is installed"
    
    # Check if the model is available
    if ollama list | grep -q "mistral"; then
        echo "✅ Mistral model is available"
    else
        echo "⚠️  Mistral model not found. Run 'ollama pull mistral' to download it."
    fi
else
    echo "⚠️  Ollama not found. Install it from https://ollama.ai for AI-powered commit messages."
    echo "   The tool will work with fallback message generation."
fi

echo ""
echo "🎉 Deployment complete!"
echo ""
echo "Usage:"
echo "  ai-commit              # Interactive mode"
echo "  ai-commit -y           # Auto-commit with generated message"
echo "  ai-commit --help       # Show help"
echo ""
echo "Make sure to stage your changes with 'git add' before running ai-commit."