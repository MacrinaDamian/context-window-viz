# CLAUDE.md

## MCP Servers

- **Figma**: Remote (`claude.ai Figma`) + local (`figma`)
- **Atlassian**: Local HTTP (`https://mcp.atlassian.com/v1/mcp`)

On session start: run `claude mcp list` — all servers should show ✓ Connected.

## Rules

### Tool Results
When tool results save to files: parse directly with `jq` — do NOT read the file first.
```bash
jq -r '.[0].text | fromjson | ...' /path/to/result.txt
```

### Debugging
1. Diagnose root cause before changing code — no speculative fixes
2. **Explain the cause and proposed fix. Wait for approval before editing.**
3. If first fix fails, re-analyze from scratch — don't iterate blindly

### Git
Use `gh` CLI for pushes, never SSH. Auth failures → `gh auth login`.

### Documentation
Don't create redundant docs. Consolidate. Ask before creating files if similar content exists.

### Response Quality
If unsure about a capability, say so with a confidence level. Don't flip-flop — investigate once and commit.

## Dashboard Dev (Rich Terminal)

**Acceptance criteria (all must pass before completion):**
1. Single render — no duplication
2. Context window % = current usage, not cumulative
3. Rich 256-color palette only, no ANSI fallbacks
4. Rich Live display for flicker-free updates
**Workflow:** Write code → write programmatic tests for all 4 criteria → run → fix → re-run. No user input until all pass or 5 fix cycles attempted. Show results each iteration.
