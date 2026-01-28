#!/usr/bin/env python3
"""
Show markdown diff files with colors in terminal.
Uses rich for colored output.
"""

import sys
from rich.console import Console
from rich.markdown import Markdown

console = Console()

def show_colored_diff(file_path):
    """Show diff file with colors."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()

        # Split into lines for coloring
        lines = content.split('\n')
        in_diff_block = False

        for line in lines:
            # Detect diff block
            if line.strip() == '```diff':
                in_diff_block = True
                console.print(line, style="dim")
                continue
            elif line.strip() == '```' and in_diff_block:
                in_diff_block = False
                console.print(line, style="dim")
                continue

            # Color diff lines
            if in_diff_block:
                if line.startswith('+'):
                    console.print(line, style="green")
                elif line.startswith('-'):
                    console.print(line, style="red")
                elif line.startswith('@@'):
                    console.print(line, style="cyan bold")
                else:
                    console.print(line)
            else:
                # Outside diff block, render as normal markdown
                if line.startswith('#'):
                    console.print(line, style="bold blue")
                elif line.startswith('**'):
                    console.print(line, style="bold yellow")
                elif line.startswith('- '):
                    console.print(line, style="yellow")
                else:
                    console.print(line)

    except FileNotFoundError:
        console.print(f"[red]Error: File not found: {file_path}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        console.print("[yellow]Usage: python3 show-diff.py <diff-file.md>[/yellow]")
        sys.exit(1)

    show_colored_diff(sys.argv[1])
