# Claude Code Context Window Visualization

> Real-time visualization of your Claude Code context window usage

[![GitHub](https://img.shields.io/badge/GitHub-context--window--viz-blue?logo=github)](https://github.com/MacrinaDamian/context-window-viz)

## 🚀 Quick Start

```bash
python3 enhanced_dashboard.py
```

**Or use the launcher:**
```bash
./dashboard
```

## ✨ Features

- ✅ **Real-Time Updates** - Smooth, flicker-free display using Rich Live
- ✅ **Color-Coded Display** - Professional color scheme matching Claude Code's `/context` command
- ✅ **Category Breakdown** - Visual breakdown of context usage by type (System Prompt, Tools, MCP, Skills, Messages)
- ✅ **Multi-Colored Progress Bar** - Segmented bar showing usage by category
- ✅ **Tool Analytics** - Detailed breakdown of MCP and System tool usage
- ✅ **Auto-Detection** - Automatically finds your current Claude Code session
- ✅ **No Duplication** - Clean single render with proper screen updates

## 📊 What You'll See

```
┌─────────────────────────────────────────────────────────┐
│ Context Usage                                           │
└─────────────────────────────────────────────────────────┘
████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
claude-sonnet-4-5-20250929 · 78k/200k tokens (39%)

Usage by category (calculated from actual content)
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
  └ Glob: 1 calls
  └ Edit: 1 calls

API Calls: 33 | ● LIVE 15:23:24
```

## 🛠️ Installation

```bash
pip3 install -r requirements.txt
```

**Requirements:**
- Python 3.7+
- `rich` library (for terminal UI)

## 📖 Usage

### Run in a Separate Terminal

1. Open a new terminal window
2. Run: `python3 enhanced_dashboard.py`
3. Keep it open while using Claude Code
4. Watch your context usage update in real-time!

### Manual Session Selection

```bash
# Specify a particular session file
python3 enhanced_dashboard.py ~/.claude/projects/my-project/session-id.jsonl
```

### Exit

Press **Ctrl+C** to stop the dashboard cleanly.

## 📁 Project Structure

```
.
├── enhanced_dashboard.py    # Main dashboard
├── context_report.py        # Static report generator
├── dashboard                # Quick launcher script
├── requirements.txt         # Python dependencies
├── .claude/
│   ├── settings.json        # Pre-commit hooks
│   └── skills/
│       └── gitpush/         # Custom git workflow skill
├── CLAUDE.md                # Claude Code instructions
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## ⚙️ Claude Code Configuration

This project includes ready-to-use Claude Code configurations:

### Custom Skills
- **`/gitpush`** - Automated git workflow using GitHub CLI (no SSH)

### Pre-Commit Hooks
- Automatic check for system files (.DS_Store, Thumbs.db)
- Blocks commits with unwanted files

### Project Instructions
See `CLAUDE.md` for:
- MCP server configuration
- Debugging guidelines
- Documentation standards
- Response quality requirements
- Dashboard development workflow

## 🎨 Color Legend

- **Gray (●)** - System prompt
- **Blue (●)** - System tools (Read, Write, Bash, etc.)
- **Teal (●)** - MCP tools (Figma, Atlassian, etc.)
- **Yellow (●)** - Skills
- **Purple (●)** - Messages (conversation history)
- **Light Gray (■)** - Free space
- **Medium Gray (▦)** - Autocompact buffer

## 🔍 Data Source

Dashboards read from Claude Code session files:
```
~/.claude/projects/<project-path>/<session-id>.jsonl
```

The latest modified session is automatically detected.

## 🐛 Troubleshooting

**Dashboard not finding session?**
```bash
# Check if session files exist
ls ~/.claude/projects/*/*.jsonl

# Manually specify the file
python3 enhanced_dashboard.py /path/to/session.jsonl
```

**Dashboard showing duplicate content?**
- This has been fixed in the latest version using Rich's Live display
- Make sure you're using the updated `enhanced_dashboard.py`

**Colors look pale or faded?**
- Fixed in latest version - colors now use full RGB palette
- Category symbols are no longer dimmed

**Import errors?**
```bash
pip3 install -r requirements.txt
```

## 🤝 Contributing

Contributions welcome! This project was built iteratively with Claude Code.

## 📄 License

MIT

## 🔗 Links

- **GitHub Repository:** https://github.com/MacrinaDamian/context-window-viz
- **Claude Code:** https://claude.com/claude-code

---

Built with Claude Code 🤖
