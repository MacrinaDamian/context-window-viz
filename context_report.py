#!/usr/bin/env python3
"""
Claude Code Context Report Generator
Reads JSON from stdin (same format as statusline) and generates detailed report
"""

import json
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich import box

def create_report(data: dict):
    console = Console()

    # Extract data
    workspace = data.get('workspace', {})
    model = data.get('model', {})
    context = data.get('context_window', {})

    # Create overview table
    overview = Table(show_header=False, box=box.ROUNDED, padding=(0, 2))
    overview.add_column(style="cyan bold", width=25)
    overview.add_column(style="white")

    overview.add_row("Working Directory:", workspace.get('current_dir', 'N/A'))
    overview.add_row("Model:", model.get('display_name', 'N/A'))
    overview.add_row("Model ID:", model.get('id', 'N/A'))

    if context:
        overview.add_row("", "")  # Spacing
        overview.add_row("[bold]CONTEXT WINDOW[/bold]", "")
        overview.add_row("Max Tokens:", f"{context.get('max_tokens', 0):,}")
        overview.add_row("Used:", f"{context.get('used_percentage', 0):.2f}%")
        overview.add_row("Remaining:", f"{context.get('remaining_percentage', 100):.2f}%")
        overview.add_row("", "")  # Spacing
        overview.add_row("[bold]SESSION TOTALS[/bold]", "")
        overview.add_row("Total Input Tokens:", f"{context.get('total_input_tokens', 0):,}")
        overview.add_row("Total Output Tokens:", f"{context.get('total_output_tokens', 0):,}")
        overview.add_row("Total Tokens:", f"{context.get('total_input_tokens', 0) + context.get('total_output_tokens', 0):,}")

        # Last API call
        current = context.get('current_usage', {})
        if current:
            overview.add_row("", "")  # Spacing
            overview.add_row("[bold]LAST API CALL[/bold]", "")
            overview.add_row("Input Tokens:", f"{current.get('input_tokens', 0):,}")
            overview.add_row("Output Tokens:", f"{current.get('output_tokens', 0):,}")

        # Cache stats
        cache_read = context.get('cache_read_input_tokens', 0)
        cache_write = context.get('cache_creation_input_tokens', 0)
        if cache_read > 0 or cache_write > 0:
            overview.add_row("", "")  # Spacing
            overview.add_row("[bold]CACHE STATISTICS[/bold]", "")
            overview.add_row("Cache Read Tokens:", f"{cache_read:,}")
            overview.add_row("Cache Write Tokens:", f"{cache_write:,}")
            total_input = context.get('total_input_tokens', 0)
            if total_input > 0:
                efficiency = (cache_read / (total_input + cache_read) * 100) if cache_read > 0 else 0
                overview.add_row("Cache Efficiency:", f"{efficiency:.1f}%")

    # Create progress bar
    if context:
        used_pct = context.get('used_percentage', 0)
        bar_width = 60
        filled = int(bar_width * used_pct / 100)
        empty = bar_width - filled

        if used_pct < 50:
            color = "green"
        elif used_pct < 80:
            color = "yellow"
        else:
            color = "red"

        bar = Text()
        bar.append("█" * filled, style=color)
        bar.append("░" * empty, style="dim")
        bar.append(f"  {used_pct:.1f}% used", style="bold")

        console.print(Panel(bar, title="[bold]Context Window Usage[/bold]", border_style=color))
        console.print()

    # Print overview
    console.print(Panel(overview, title="[bold cyan]Context Window Report[/bold cyan]", border_style="cyan"))

    # Print raw data availability info
    console.print()
    console.print("[dim]Available data fields:[/dim]")
    console.print(f"[dim]  - workspace: {list(workspace.keys())}[/dim]")
    console.print(f"[dim]  - model: {list(model.keys())}[/dim]")
    console.print(f"[dim]  - context_window: {list(context.keys())}[/dim]")

def main():
    try:
        # Read JSON from stdin
        data = json.load(sys.stdin)
        create_report(data)
    except json.JSONDecodeError as e:
        console = Console()
        console.print(f"[red]Error: Invalid JSON input[/red]")
        console.print(f"[red]{e}[/red]")
        sys.exit(1)
    except Exception as e:
        console = Console()
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
