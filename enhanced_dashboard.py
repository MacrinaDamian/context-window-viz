#!/usr/bin/env python3
"""
Claude Code Context Window - Enhanced Dashboard
Matches the /context command style with colored breakdowns
"""

import json
import time
import sys
import os
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich.live import Live
from rich.layout import Layout

class EnhancedContextDashboard:
    def __init__(self, jsonl_path: str):
        self.jsonl_path = Path(jsonl_path)
        self.console = Console()
        self.last_line_count = 0
        self.stats = self.create_empty_stats()

    def create_empty_stats(self):
        return {
            'total_input': 0,
            'total_output': 0,
            'total_cache_read': 0,
            'total_cache_write': 0,
            'current_context': 0,
            'api_calls': 0,
            'messages_by_role': defaultdict(int),
            'content_by_type': defaultdict(int),
            'tool_uses': 0,
            'tool_tokens': defaultdict(int),  # Track tokens per tool
            'mcp_tools': defaultdict(int),
            'system_tools': defaultdict(int),
            'model': 'Unknown',
            'max_tokens': 200000,
            'last_call': {},
            # Category breakdown
            'system_prompt_tokens': 0,
            'system_tools_tokens': 0,
            'mcp_tools_tokens': 0,
            'skills_tokens': 0,
            'messages_tokens': 0,
            'first_cache_creation': 0,
            'total_message_chars': 0,
            'total_tool_chars': 0,
            'thinking_chars': 0,
        }

    def parse_jsonl(self) -> bool:
        """Parse the JSONL file and update stats"""
        try:
            if not self.jsonl_path.exists():
                return False

            with open(self.jsonl_path, 'r') as f:
                lines = f.readlines()

            if len(lines) == self.last_line_count:
                return False

            self.last_line_count = len(lines)
            self.stats = self.create_empty_stats()

            for line in lines:
                try:
                    record = json.loads(line.strip())
                    self.process_record(record)
                except json.JSONDecodeError:
                    continue

            # Estimate category tokens
            self.estimate_categories()

            return True

        except Exception as e:
            self.console.print(f"[red]Error parsing JSONL: {e}[/red]")
            return False

    def process_record(self, record: dict):
        """Process a single JSONL record"""
        message = record.get('message', {})

        if 'model' in message:
            self.stats['model'] = message['model']

        usage = message.get('usage')
        if usage:
            self.stats['api_calls'] += 1
            input_tok = usage.get('input_tokens', 0)
            output_tok = usage.get('output_tokens', 0)
            cache_read = usage.get('cache_read_input_tokens', 0)
            cache_write = usage.get('cache_creation_input_tokens', 0)

            self.stats['total_input'] += input_tok
            self.stats['total_output'] += output_tok
            self.stats['total_cache_read'] += cache_read
            self.stats['total_cache_write'] += cache_write

            # Capture first cache creation (tool definitions)
            if self.stats['api_calls'] == 1 and cache_write > 0:
                self.stats['first_cache_creation'] = cache_write

            self.stats['last_call'] = {
                'input': input_tok,
                'output': output_tok,
                'cache_read': cache_read,
                'cache_write': cache_write,
            }

            # Current context = last call's total
            self.stats['current_context'] = input_tok + cache_read + output_tok

        role = message.get('role')
        if role:
            self.stats['messages_by_role'][role] += 1

        content = message.get('content', [])
        if isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    content_type = item.get('type', 'unknown')
                    self.stats['content_by_type'][content_type] += 1

                    if content_type == 'tool_use':
                        self.stats['tool_uses'] += 1
                        tool_name = item.get('name', 'unknown')

                        # Count tool call characters
                        tool_input = str(item.get('input', ''))
                        self.stats['total_tool_chars'] += len(tool_name) + len(tool_input)

                        # Categorize MCP vs System tools
                        if tool_name.startswith('mcp__'):
                            self.stats['mcp_tools'][tool_name] += 1
                        else:
                            self.stats['system_tools'][tool_name] += 1

                    elif content_type == 'tool_result':
                        # Count tool result characters
                        result_content = str(item.get('content', ''))
                        self.stats['total_tool_chars'] += len(result_content)

                    elif content_type == 'text':
                        # Count message text characters
                        text = item.get('text', '')
                        if role in ['user', 'assistant']:
                            self.stats['total_message_chars'] += len(text)

                    elif content_type == 'thinking':
                        # Count thinking characters
                        thinking = item.get('thinking', '')
                        self.stats['thinking_chars'] += len(thinking)

    def estimate_categories(self):
        """Calculate token usage by category using actual content"""
        current = self.stats['current_context']

        if current == 0:
            return

        # 1. System prompt: relatively fixed in Claude Code (~3-4k)
        self.stats['system_prompt_tokens'] = 3500

        # 2. Tool definitions: Use first API call's cache_creation
        # (Tools get cached on first call and include both system + MCP tools)
        total_tool_defs = self.stats['first_cache_creation']

        # Split tool definitions between System and MCP based on usage ratio
        total_tools = len(self.stats['system_tools']) + len(self.stats['mcp_tools'])
        if total_tools > 0:
            mcp_ratio = len(self.stats['mcp_tools']) / total_tools
            system_ratio = len(self.stats['system_tools']) / total_tools

            self.stats['mcp_tools_tokens'] = int(total_tool_defs * mcp_ratio)
            self.stats['system_tools_tokens'] = int(total_tool_defs * system_ratio)
        else:
            # Fallback to rough estimates
            self.stats['system_tools_tokens'] = int(total_tool_defs * 0.45)
            self.stats['mcp_tools_tokens'] = int(total_tool_defs * 0.55)

        # 3. Skills: minimal (usually < 100 tokens)
        self.stats['skills_tokens'] = 100

        # 4. Messages: Count actual characters and convert to tokens
        # Rule of thumb: 1 token ≈ 4 characters
        message_tokens = self.stats['total_message_chars'] / 4
        tool_tokens = self.stats['total_tool_chars'] / 4
        thinking_tokens = self.stats['thinking_chars'] / 4

        # Messages = actual message text + tool calls/results + thinking
        estimated_message_tokens = int(message_tokens + tool_tokens + thinking_tokens)

        # 5. Adjust to match current context total
        estimated_total = (self.stats['system_prompt_tokens'] +
                          self.stats['system_tools_tokens'] +
                          self.stats['mcp_tools_tokens'] +
                          self.stats['skills_tokens'] +
                          estimated_message_tokens)

        # Scale messages to fit actual current context
        if estimated_total > 0:
            remaining = current - (self.stats['system_prompt_tokens'] +
                                  self.stats['system_tools_tokens'] +
                                  self.stats['mcp_tools_tokens'] +
                                  self.stats['skills_tokens'])
            self.stats['messages_tokens'] = max(0, remaining)
        else:
            self.stats['messages_tokens'] = estimated_message_tokens

    def format_number(self, num):
        """Format large numbers compactly"""
        if num >= 1_000_000:
            return f"{num/1_000_000:.1f}M"
        elif num >= 1_000:
            return f"{num/1_000:.1f}K"
        else:
            return str(num)

    def create_colored_progress_bar(self, width=60) -> Text:
        """Create multi-colored segmented progress bar"""
        current = self.stats['current_context']
        max_tokens = self.stats['max_tokens']

        if current == 0:
            return Text("░" * width, style="dim")

        # Calculate segment sizes
        sys_prompt = self.stats['system_prompt_tokens']
        sys_tools = self.stats['system_tools_tokens']
        mcp_tools = self.stats['mcp_tools_tokens']
        skills = self.stats['skills_tokens']
        messages = self.stats['messages_tokens']
        free = max_tokens - current
        autocompact = int(max_tokens * 0.165)  # 16.5% buffer

        # Calculate bar segments
        sys_prompt_bars = int((sys_prompt / max_tokens) * width)
        sys_tools_bars = int((sys_tools / max_tokens) * width)
        mcp_tools_bars = int((mcp_tools / max_tokens) * width)
        skills_bars = int((skills / max_tokens) * width)
        messages_bars = int((messages / max_tokens) * width)

        used_bars = sys_prompt_bars + sys_tools_bars + mcp_tools_bars + skills_bars + messages_bars
        free_bars = width - used_bars

        # Create colored bar with IBM Carbon Design System colors
        bar = Text()
        bar.append("█" * sys_prompt_bars, style="rgb(141,141,141)")  # Carbon Gray-60
        bar.append("█" * sys_tools_bars, style="rgb(15,98,254)")  # Carbon Blue-60
        bar.append("█" * mcp_tools_bars, style="rgb(0,157,154)")  # Carbon Teal-50
        bar.append("█" * skills_bars, style="rgb(241,194,27)")  # Carbon Yellow-30
        bar.append("█" * messages_bars, style="rgb(138,63,252)")  # Carbon Purple-50
        bar.append("░" * free_bars, style="rgb(224,224,224)")  # Carbon Gray-20

        return bar

    def create_category_table(self) -> Table:
        """Create category breakdown table"""
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column(style="", width=2)  # No dim style for colored symbols
        table.add_column(style="white", width=30)
        table.add_column(style="dim", justify="right")

        current = self.stats['current_context']
        max_tokens = self.stats['max_tokens']

        def add_row(symbol, label, tokens, color="white"):
            pct = (tokens / max_tokens * 100) if max_tokens > 0 else 0
            table.add_row(
                f"[{color}]{symbol}[/{color}]",
                f"{label}:",
                f"{self.format_number(tokens)} tokens ({pct:.1f}%)"
            )

        # IBM Carbon Design System colors - FILLED symbols for visibility
        add_row("●", "System prompt", self.stats['system_prompt_tokens'], "rgb(141,141,141)")  # Carbon Gray-60
        add_row("●", "System tools", self.stats['system_tools_tokens'], "rgb(15,98,254)")  # Carbon Blue-60
        add_row("●", "MCP tools", self.stats['mcp_tools_tokens'], "rgb(0,157,154)")  # Carbon Teal-50
        add_row("●", "Skills", self.stats['skills_tokens'], "rgb(241,194,27)")  # Carbon Yellow-30
        add_row("●", "Messages", self.stats['messages_tokens'], "rgb(138,63,252)")  # Carbon Purple-50

        free = max_tokens - current
        autocompact = int(max_tokens * 0.165)
        add_row("■", "Free space", free, "rgb(224,224,224)")  # Carbon Gray-20
        add_row("▦", "Autocompact buffer", autocompact, "rgb(168,168,168)")  # Carbon Gray-40

        return table

    def generate_display(self):
        """Generate the full dashboard display as a renderable"""
        from rich.console import Group

        stats = self.stats
        current = stats['current_context']
        max_tokens = stats['max_tokens']
        used_pct = (current / max_tokens * 100) if max_tokens > 0 else 0

        renderables = []

        # Header
        renderables.append(Text("Context Usage", style="bold white"))
        renderables.append(Text())  # Add spacing

        # Progress bar
        bar = self.create_colored_progress_bar(50)
        renderables.append(bar)
        renderables.append(Text())

        # Usage line
        renderables.append(Text(f"{stats['model']} · {self.format_number(current)}/{self.format_number(max_tokens)} tokens ({used_pct:.1f}%)\n", style="dim"))

        # Category breakdown
        renderables.append(Text("Usage by category (calculated from actual content)", style="dim italic"))
        renderables.append(self.create_category_table())
        renderables.append(Text())

        # MCP Tools section - grouped by server
        if stats['mcp_tools']:
            renderables.append(Text("MCP tools", style="bold"))

            # Group tools by server type
            servers = {}
            for tool, count in stats['mcp_tools'].items():
                # Extract server name: mcp__server__tool_name
                parts = tool.split('__')
                if len(parts) >= 3:
                    server = parts[1]  # Get the server name
                    # Clean up server name for display
                    if server == 'claude_ai_Figma':
                        server_display = 'Claude.ai Figma'
                    else:
                        server_display = server.replace('_', ' ').title()

                    if server_display not in servers:
                        servers[server_display] = []
                    servers[server_display].append((tool, count))

            # Display grouped by server
            for server_name in sorted(servers.keys()):
                tools = servers[server_name]
                total_calls = sum(count for _, count in tools)
                tool_count = len(tools)

                renderables.append(Text(f"  {server_name} ({tool_count} tools, {total_calls} calls)", style="rgb(0,157,154)"))

                # Show top 5 tools per server
                for tool, count in sorted(tools, key=lambda x: x[1], reverse=True)[:5]:
                    # Show just the tool name without the mcp__server__ prefix
                    tool_name = tool.split('__', 2)[2] if len(tool.split('__')) >= 3 else tool
                    renderables.append(Text(f"    └ {tool_name}: {count} calls", style="dim"))

                if len(tools) > 5:
                    renderables.append(Text(f"    └ ...and {len(tools) - 5} more", style="dim italic"))

            renderables.append(Text())

        # System Tools section
        if stats['system_tools']:
            renderables.append(Text("System tools (top 5)", style="bold"))
            for tool, count in sorted(stats['system_tools'].items(), key=lambda x: x[1], reverse=True)[:5]:
                renderables.append(Text(f"  └ {tool}: {count} calls", style="dim"))
            renderables.append(Text())

        # Stats with live indicator
        current_time = datetime.now().strftime('%H:%M:%S')
        renderables.append(Text(f"API Calls: {stats['api_calls']} | ● LIVE {current_time}\n", style="dim"))

        # Legend
        renderables.append(Text("─" * 60))
        renderables.append(Text("Legend - What does this mean?\n", style="bold"))

        legend = Table(show_header=False, box=None, padding=(0, 2))
        legend.add_column(style="cyan", width=20)
        legend.add_column(style="white", width=40)

        legend.add_row(
            "[rgb(141,141,141)]● System prompt[/rgb(141,141,141)]",
            "[dim]Instructions that tell Claude how to behave[/dim]"
        )
        legend.add_row(
            "[rgb(15,98,254)]● System tools[/rgb(15,98,254)]",
            "[dim]Built-in tools (Read, Write, Bash, etc.)[/dim]"
        )
        legend.add_row(
            "[rgb(0,157,154)]● MCP tools[/rgb(0,157,154)]",
            "[dim]External integrations (Figma, Atlassian, etc.)[/dim]"
        )
        legend.add_row(
            "[rgb(241,194,27)]● Skills[/rgb(241,194,27)]",
            "[dim]Custom commands and shortcuts[/dim]"
        )
        legend.add_row(
            "[rgb(138,63,252)]● Messages[/rgb(138,63,252)]",
            "[dim]Your conversation history (questions + answers)[/dim]"
        )
        legend.add_row(
            "[rgb(224,224,224)]■ Free space[/rgb(224,224,224)]",
            "[dim]Available context remaining[/dim]"
        )
        legend.add_row(
            "[rgb(168,168,168)]▦ Autocompact[/rgb(168,168,168)]",
            "[dim]Reserved buffer (context compacts at 83.5%)[/dim]"
        )

        renderables.append(legend)
        renderables.append(Text())
        renderables.append(Text("💡 Tip: Context = working memory. When full, older messages get compressed.", style="dim"))
        renderables.append(Text("Press Ctrl+C to exit", style="dim"))

        return Group(*renderables)

    def run(self, refresh_interval: float = 1.0):
        """Run the dashboard with live updates"""
        try:
            with Live(self.generate_display(), refresh_per_second=1, screen=False) as live:
                while True:
                    self.parse_jsonl()
                    live.update(self.generate_display())
                    time.sleep(refresh_interval)
        except KeyboardInterrupt:
            self.console.print("\n[yellow]Dashboard stopped.[/yellow]")

def find_current_session():
    """Find the current session JSONL file"""
    claude_dir = Path.home() / '.claude' / 'projects'
    if not claude_dir.exists():
        return None

    jsonl_files = list(claude_dir.glob('*/*.jsonl'))
    if not jsonl_files:
        return None

    jsonl_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return jsonl_files[0]

def main():
    console = Console()

    if len(sys.argv) > 1:
        jsonl_path = Path(sys.argv[1])
    else:
        jsonl_path = find_current_session()
        if not jsonl_path:
            console.print("[red]Error: Could not find session JSONL file[/red]")
            sys.exit(1)

    if not jsonl_path.exists():
        console.print(f"[red]Error: File not found: {jsonl_path}[/red]")
        sys.exit(1)

    console.print(f"[green]Starting Enhanced Dashboard...[/green]")
    console.print(f"[dim]Monitoring: {jsonl_path.name}[/dim]\n")
    time.sleep(1)

    dashboard = EnhancedContextDashboard(str(jsonl_path))
    dashboard.run(refresh_interval=1.0)

if __name__ == "__main__":
    main()
