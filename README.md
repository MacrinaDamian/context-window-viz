# Context Window Viz

Real-time visualization of Claude Code context window usage.

## Quick Start

```bash
python3 enhanced_dashboard.py
```

Or use the launcher:
```bash
./dashboard
```

## Features

- **Real-time updates** - Flicker-free display with Rich Live
- **Category breakdown** - System prompt, tools, MCP, skills, messages
- **Multi-colored progress bar** - Visual usage by category
- **Tool analytics** - Detailed MCP and system tool tracking
- **Auto-detection** - Finds your current Claude Code session automatically

## Installation

```bash
pip3 install -r requirements.txt
```

**Requirements:** Python 3.7+ and `rich` library

## Usage

### Live Dashboard
Open a separate terminal and run:
```bash
python3 enhanced_dashboard.py
```

Keep it open while using Claude Code to see real-time updates.

### Manual Session
```bash
python3 enhanced_dashboard.py ~/.claude/projects/my-project/session-id.jsonl
```

### Static Report
```bash
python3 context_report.py
```

Exit with **Ctrl+C**.

## Display

```
┌─────────────────────────────────────────────────────────┐
│ Context Usage                                           │
└─────────────────────────────────────────────────────────┘
████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
claude-sonnet-4-5-20250929 · 78k/200k tokens (39%)

Usage by category
  ● System prompt:        3.3k tokens (1.7%)
  ● System tools:          17k tokens (8.5%)
  ● MCP tools:           13.5k tokens (6.8%)
  ● Skills:                 61 tokens (0.0%)
  ● Messages:            38.9k tokens (19.4%)
  ■ Free space:            94k (47.1%)
  ▦ Autocompact buffer:    33k tokens (16.5%)

System tools (top 5)
  └ Bash: 6 calls
  └ Read: 2 calls

API Calls: 33 | ● LIVE 15:23:24
```

## Color Legend

- **Gray** - System prompt
- **Blue** - System tools (Read, Write, Bash, etc.)
- **Teal** - MCP tools (Figma, Atlassian, etc.)
- **Yellow** - Skills
- **Purple** - Messages
- **Light Gray** - Free space
- **Medium Gray** - Autocompact buffer

## Data Source

Reads from Claude Code session files:
```
~/.claude/projects/<project-path>/<session-id>.jsonl
```

## Troubleshooting

**Dashboard not finding session?**
```bash
ls ~/.claude/projects/*/*.jsonl
python3 enhanced_dashboard.py /path/to/session.jsonl
```

**Import errors?**
```bash
pip3 install -r requirements.txt
```

## Configuration

See `CLAUDE.md` for project-specific instructions including MCP server setup.

## License

MIT

---

[GitHub](https://github.com/MacrinaDamian/context-window-viz) • [Claude Code](https://claude.com/claude-code)
