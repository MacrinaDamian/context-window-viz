# Git Push Skill
1. Check if `gh` CLI is authenticated: `gh auth status`
2. If not authenticated, run `gh auth login` (web flow)
3. Stage changes: `git add -A`
4. Show diff summary and ask user for commit message
5. Commit and push. If push fails, do NOT try SSH — use `gh` CLI to fix.
6. Never explore SSH key setup unless explicitly asked.
