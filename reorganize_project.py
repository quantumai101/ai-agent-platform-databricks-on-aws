#!/usr/bin/env python3
"""
AI Agent Platform - Project Reorganizer (Windows Safe)
Run from your project root:
    python reorganize_project.py
"""

import os
import shutil
from pathlib import Path

ROOT = Path(__file__).parent.resolve()

# ── Color output (works on Windows with modern PowerShell) ──────────────────
def pr(emoji, msg, color=""):
    RESET = "\033[0m"
    print(f"{color}{emoji}  {msg}{RESET}")

OK   = lambda e, m: pr(e, m, "\033[92m")
WARN = lambda e, m: pr(e, m, "\033[93m")
INFO = lambda e, m: pr(e, m, "\033[96m")

# ── Exact file → destination mapping based on YOUR project ──────────────────
MOVES = [
    # AGENTS
    ("nova.py",             "agents/nova_infrastructure_agent.py"),
    ("axiom.py",            "agents/axiom_data_pipeline_agent.py"),
    ("sentinel.py",         "monitoring/sentinel.py"),
    ("prometheus.py",       "monitoring/prometheus.py"),

    # ORCHESTRATION
    ("orchestrator.py",     "orchestration/orchestrator.py"),

    # TESTS
    ("test_nova.py",        "tests/test_nova.py"),

    # DEPLOYMENT
    ("deploy.sh",           "deployment/deploy.sh"),
    ("launch_ui.py",        "deployment/launch_ui.py"),
    ("START_UI.bat",        "deployment/START_UI.bat"),
    ("nexus.py",            "deployment/nexus.py"),

    # FRONTEND
    ("index.html",          "frontend/index.html"),

    # CONFIG
    (".env.example",        "config/.env.example"),
    ("requirements.txt",    "config/requirements.txt"),

    # DOCS
    ("GITHUB_GUIDE.md",     "docs/GITHUB_GUIDE.md"),
    ("PACKAGE_COMPLETE.md", "docs/PACKAGE_COMPLETE.md"),
    ("PROJECT_STRUCTURE.md","docs/PROJECT_STRUCTURE.md"),
    ("README.md",           "docs/README.md"),
]

# Files/folders to never touch
IGNORE = {"reorganize_project.py", ".git", ".github", ".gitignore"}


def backup():
    """Copy entire project to a sibling BACKUP folder."""
    backup_dir = ROOT.parent / (ROOT.name + "-BACKUP")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    shutil.copytree(ROOT, backup_dir)
    OK("💾", f"Backup created: {backup_dir}")


def move_files():
    moved, skipped, missing = [], [], []

    for src_name, dst_rel in MOVES:
        src = ROOT / src_name
        dst = ROOT / dst_rel

        if not src.exists():
            missing.append(src_name)
            continue

        if src == dst:
            skipped.append(src_name)
            continue

        if dst.exists():
            WARN("⚠️ ", f"Already exists, skipping: {dst_rel}")
            skipped.append(src_name)
            continue

        # Create destination folder if needed
        dst.parent.mkdir(parents=True, exist_ok=True)

        shutil.move(str(src), str(dst))
        OK("✅", f"{src_name}  ->  {dst_rel}")
        moved.append(src_name)

    return moved, skipped, missing


def remove_empty_dirs():
    """Remove any directories that are now empty."""
    for dirpath in sorted(ROOT.rglob("*"), reverse=True):
        if (dirpath.is_dir()
                and dirpath.name not in IGNORE
                and dirpath != ROOT):
            try:
                if not any(dirpath.iterdir()):
                    dirpath.rmdir()
                    WARN("🗑️ ", f"Removed empty dir: {dirpath.relative_to(ROOT)}")
            except Exception:
                pass


def print_tree():
    """Print the new folder structure."""
    print()
    INFO("📁", f"New structure under: {ROOT.name}/")
    seen = set()
    for _, dst_rel in MOVES:
        parts = Path(dst_rel).parts
        folder = parts[0]
        if folder not in seen:
            print(f"      \033[96m  {folder}/\033[0m")
            seen.add(folder)
        print(f"         \033[92m  └─ {parts[-1]}\033[0m")
    print()


def main():
    print()
    print("\033[1m\033[96m" + "="*50 + "\033[0m")
    print("\033[1m\033[96m  AI AGENT PLATFORM - Project Reorganizer\033[0m")
    print("\033[1m\033[96m" + "="*50 + "\033[0m")
    print(f"\n  Root: {ROOT}\n")

    # Step 1: Backup
    INFO("💾", "Creating backup first...")
    backup()
    print()

    # Step 2: Move files
    INFO("🚀", "Moving files...")
    print()
    moved, skipped, missing = move_files()

    # Step 3: Clean empty dirs
    print()
    remove_empty_dirs()

    # Step 4: Summary
    print()
    print("\033[1m" + "="*50 + "\033[0m")
    print("\033[1m  SUMMARY\033[0m")
    print("="*50)
    OK("✅", f"Moved:   {len(moved)} files")
    WARN("⚠️ ", f"Skipped: {len(skipped)} files")
    INFO("❓", f"Missing: {len(missing)} files (not found - may already be moved)")

    if missing:
        print()
        WARN("📋", "Not found (check manually):")
        for f in missing:
            print(f"       · {f}")

    # Step 5: Print tree
    print_tree()
    print("\033[1m\033[92m  Done! Refresh your VS Code explorer (Ctrl+Shift+E).\033[0m\n")


if __name__ == "__main__":
    main()