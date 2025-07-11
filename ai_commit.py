#!/usr/bin/env python3
import argparse
import subprocess
import requests
import json

# Configuration
OLLAMA_MODEL = "mistral"  # or "phi3", "llama3", etc.
OLLAMA_URL = "http://localhost:11434/api/generate"

def get_staged_diff():
    """Get the diff of staged changes."""
    diff = subprocess.run(["git", "diff", "--cached"], stdout=subprocess.PIPE, text=True)
    return diff.stdout.strip()

def get_staged_files():
    """Get list of staged files with their status."""
    result = subprocess.run(["git", "diff", "--cached", "--name-status"], 
                          stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

# Configuration for contextual commit messages
COMMIT_MESSAGE_RULES = [
    {
        "conditions": {
            "files_contain": ["cli/database_viewer.py"],
            "file_status": "A"
        },
        "message": "Complete CLI modularization with database viewer and claim functions"
    },
    {
        "conditions": {
            "diff_contains": ["modularization"]
        },
        "message": "Complete modularization and fix import issues"
    },
    {
        "conditions": {
            "files_pattern": "cli/"
        },
        "message": "Complete modularization and fix import issues"
    }
]

def check_rule_conditions(rule, files_info, diff):
    """Check if a rule's conditions are met."""
    conditions = rule["conditions"]
    
    # Check files_contain condition
    if "files_contain" in conditions:
        for file_path in conditions["files_contain"]:
            if file_path not in files_info:
                return False
    
    # Check file_status condition
    if "file_status" in conditions:
        required_status = conditions["file_status"]
        if required_status not in files_info:
            return False
    
    # Check diff_contains condition
    if "diff_contains" in conditions:
        for keyword in conditions["diff_contains"]:
            if keyword.lower() not in diff.lower():
                return False
    
    # Check files_pattern condition
    if "files_pattern" in conditions:
        pattern = conditions["files_pattern"]
        if pattern not in files_info:
            return False
    
    return True

def generate_simple_commit_message(files_info, diff):
    """Generate a simple commit message based on file changes."""
    lines = files_info.split('\n')
    if not lines or not lines[0]:
        return "Update files"
    
    # Check for contextual rules first
    for rule in COMMIT_MESSAGE_RULES:
        if check_rule_conditions(rule, files_info, diff):
            return rule["message"]
    
    # Count different types of changes
    added = sum(1 for line in lines if line.startswith('A'))
    modified = sum(1 for line in lines if line.startswith('M'))
    deleted = sum(1 for line in lines if line.startswith('D'))
    
    # Generate message based on changes
    parts = []
    if added > 0:
        parts.append(f"Add {added} file{'s' if added > 1 else ''}")
    if modified > 0:
        parts.append(f"Update {modified} file{'s' if modified > 1 else ''}")
    if deleted > 0:
        parts.append(f"Delete {deleted} file{'s' if deleted > 1 else ''}")
    
    if len(parts) == 0:
        return "Update files"
    
    return " and ".join(parts)

def generate_commit_message_ollama(diff):
    """Generate commit message using Ollama."""
    try:
        prompt = f"""Analyze the following git diff and write a concise, professional commit message that summarizes the changes. The message should be in imperative mood and under 500 characters if possible.

Git diff:
{diff[:2000]}  # Truncate very long diffs

Rules:
- Use imperative mood (e.g., "Add feature" not "Added feature")
- Be concise and specific
- Focus on the main purpose, not implementation details
- Only output the commit message, nothing else

Commit message:"""
        
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=30)

        if response.status_code != 200:
            print(f"❌ Ollama error: {response.text}")
            return None

        data = response.json()
        message = data['response'].strip().strip('"').strip("'")
        
        # Clean up the message
        if message.startswith("Commit message:"):
            message = message.replace("Commit message:", "").strip()
        
        return message
        
    except requests.RequestException as e:
        print(f"❌ Network error connecting to Ollama: {e}")
        return None
    except Exception as e:
        print(f"❌ Error generating commit message: {e}")
        return None

def main():
    # Get staged changes
    diff = get_staged_diff()
    if not diff:
        print("⚠️  No staged changes. Use `git add` first.")
        return
    
    files_info = get_staged_files()
    
    print("📋 Staged files:")
    for line in files_info.split('\n'):
        if line.strip():
            status = line[0]
            filename = line[2:]
            status_emoji = {"A": "➕", "M": "📝", "D": "🗑️"}.get(status, "📄")
            print(f"  {status_emoji} {filename}")
    
    print("\n🤖 Generating commit message...")
    
    # Try Ollama first
    message = generate_commit_message_ollama(diff)
    
    # Fallback to simple message generation
    if not message:
        print("⚠️  Ollama unavailable, using simple message generation...")
        message = generate_simple_commit_message(files_info, diff)
    
    if not message:
        print("❌ Could not generate commit message")
        return
    
    print(f"\n✅ Suggested commit message:")
    print(f"  {message}")

    # Argument parsing
    parser = argparse.ArgumentParser()
    arg_group = parser.add_mutually_exclusive_group()
    arg_group.add_argument("-y", action="store_true", help="Auto-commit suggested message")
    arg_group.add_argument("--y", action="store_true", help="Auto-commit suggested message")
    arg_group.add_argument("--yes", action="store_true", help="Auto-commit suggested message")
    
    args = parser.parse_args()
    
    if args.y or args.yes:
        try:
            subprocess.run(["git", "commit", "-m", message], check=True)
            print("✅ Commit created successfully!")
            subprocess.run(["git", "push"], check=True)
            print("✅ Pushed to remote repository successfully!")
            return
        except subprocess.CalledProcessError as e:
            print(f"❌ Git commit failed: {e}")
            return
    
    # Show options
    print("\nOptions:")
    print("  (y) Use this message")
    print("  (e) Edit the message")
    print("  (s) Show diff")
    print("  (n) Cancel")
    
    choice = input("\nChoose an option: ").lower().strip()
    
    if choice == 'y':
        try:
            subprocess.run(["git", "commit", "-m", message], check=True)
            print("✅ Commit created successfully!")
            subprocess.run(["git", "push"], check=True)
            print("✅ Pushed to remote repository successfully!")
            return
        except subprocess.CalledProcessError as e:
            print(f"❌ Git commit failed: {e}")
            return
    elif choice == 'e':
        print(f"\nEdit the message (press Enter for default):")
        edited_message = input(f"[{message}]: ").strip()
        if edited_message:
            try:
                subprocess.run(["git", "commit", "-m", edited_message], check=True)
                print("✅ Commit created successfully!")
                subprocess.run(["git", "push"], check=True)
                print("✅ Pushed to remote repository successfully!")
                return
            except subprocess.CalledProcessError as e:
                print(f"❌ Git commit failed: {e}")
                return
        else:
            try:
                subprocess.run(["git", "commit", "-m", message], check=True)
                print("✅ Commit created successfully!")
                subprocess.run(["git", "push"], check=True)
                print("✅ Pushed to remote repository successfully!")
                return
            except subprocess.CalledProcessError as e:
                print(f"❌ Git commit failed: {e}")
                return
    elif choice == 's':
        print(f"\n📄 Staged diff:\n{diff}")
        main()  # Restart the process
    elif choice == 'n':
        print("❌ Commit cancelled")
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()