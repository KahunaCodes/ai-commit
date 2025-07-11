# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based AI commit message generator that automatically creates commit messages for staged git changes. The tool uses either a local Ollama instance or falls back to rule-based generation.

## Architecture

The project consists of a single Python script `ai_commit.py` that:

1. **Analyzes staged changes** using `git diff --cached` and `git diff --cached --name-status`
2. **Generates commit messages** using two approaches:
   - Primary: Ollama API calls with prompt engineering
   - Fallback: Rule-based generation using predefined patterns
3. **Provides interactive workflow** for committing with options to edit, show diff, or cancel

### Key Components

- **Configuration**: Ollama model settings and API endpoint (lines 7-9)
- **Git Integration**: Functions to retrieve staged diffs and file status (lines 11-20)
- **Rule Engine**: `COMMIT_MESSAGE_RULES` array with contextual commit patterns (lines 23-43)
- **Message Generation**: Two-tier approach with Ollama AI and rule-based fallback
- **Interactive CLI**: User workflow with options for commit, edit, or cancel

## Development Commands

Since this is a single-file Python script, development is straightforward:

```bash
# Run the AI commit tool
python3 ai_commit.py

# Auto-commit with generated message (no interaction)
python3 ai_commit.py -y
# or
python3 ai_commit.py --yes

# Test with staged changes
git add <files>
python3 ai_commit.py
```

## Configuration

The tool requires:
- **Ollama running locally** on port 11434 with the configured model (default: "mistral")
- **Git repository** with staged changes
- **Python 3** with `requests` library

## Rule System

The `COMMIT_MESSAGE_RULES` array defines contextual commit patterns:
- **Condition matching**: Based on file patterns, diff content, or file status
- **Message templates**: Predefined messages for specific scenarios
- **Fallback logic**: Count-based messages when no rules match

## Interactive Workflow

The tool provides a CLI interface with options:
- `(y)` Use suggested message and commit + push
- `(e)` Edit the message before committing
- `(s)` Show the full diff
- `(n)` Cancel the operation

## Error Handling

- Network timeouts for Ollama API calls (30 seconds)
- Git command failures with descriptive error messages
- Graceful fallback to simple message generation when Ollama is unavailable