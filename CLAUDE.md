# Claude Code Instructions

This file contains project-specific instructions for Claude Code to improve collaboration and reduce friction.

## MCP Server Configuration

Known-working MCP setup commands:
```bash
claude mcp add atlassian -- npx @anthropic/atlassian-mcp
claude mcp add snyk -- npx @anthropic/snyk-mcp
claude mcp list  # Verify all are active
```

**Current Status:**
- ✓ Figma MCP: Connected and working
- ⚠️ Atlassian MCP: Configured but needs authentication on first use
- ⚠️ Snyk MCP: Configured but needs authentication on first use

**Session Start Protocol:**
Before we start, quickly verify all my MCP servers are active and authenticated. List each one with its status. If any are broken, fix them first. Then we'll move on to the actual task.

## Documentation

Avoid creating redundant or excessive documentation files. When generating docs, consolidate into the minimum number of files needed. Ask before creating new files if similar content already exists.

## Debugging

When fixing bugs, diagnose the root cause before applying changes. Do not apply speculative fixes that could worsen the problem. If the first attempt fails, step back and re-analyze rather than iterating blindly.

**Before making any changes, explain what you think is causing this issue and what your fix will do. Wait for my approval before editing any files.**

## Dashboard Development & Testing

When building or refining Rich-based terminal dashboards, use this test-driven workflow:

**Acceptance Criteria (must pass before completion):**
1. Dashboard renders exactly once (no duplication)—verify by running the script and counting render calls
2. Context window percentage must reflect CURRENT usage, not cumulative (mock a test case: 54000 tokens used of 100000 = 54.0%)
3. Colors must use Rich's full 256-color palette, no ANSI fallbacks—verify by checking Rich style objects
4. Must use Rich Live display for real-time updates without screen flicker
5. All category labels must be visible (not faded) against a dark terminal background—use minimum brightness threshold

**Workflow:**
1. Write the dashboard code
2. Write a test script that validates all 5 criteria programmatically
3. Run tests
4. Fix failures
5. Re-run until all pass
6. Show test results at each iteration
7. Do not ask for input until all tests pass or you've tried 5 fix cycles

## Response Quality

When unsure about a tool or repo's capabilities, say so clearly. Do not flip-flop between 'yes it supports X' and 'no it doesn't' — investigate once, state confidence level, and stick with the assessment unless new evidence appears.
