# Git / GitHub — Simple Cheat Sheet

## Main commands

- `git status` — See what changed and whether your branch is ahead/behind GitHub.
- `git pull` — Download changes from GitHub and merge them into your current branch.
- `git add .` — Prepare all changed/new files for a commit.
- `git commit -m "message"` — Save your current changes as a Git snapshot.
- `git push` — Upload your commits to GitHub.
- `git fetch` — Download information about GitHub without changing your files.
- `git log --oneline` — See the commit history.
- `git stash` — Temporarily put uncommitted changes aside.
- `git stash pop` — Restore the most recently stashed changes.
- `git restore <file>` — Discard uncommitted changes to a specific file.

## Standard workflow for two computers

### Computer A — before stopping work

```bash
git status
git add .
git commit -m "Save work"
git push
```

### Computer B — when starting work

```bash
git status
git pull
```

Work normally, then when finished:

```bash
git add .
git commit -m "Save work"
git push
```

Then on Computer A:

```bash
git pull
```

The basic cycle:

```text
Computer A
    ↓
commit → push
    ↓
GitHub
    ↓
pull
    ↓
Computer B
```

## The one rule to remember

**Before switching computers: commit and push.**

**Before starting on the other computer: pull.**

## If `git pull` refuses

If you have local changes that you want to keep:

```bash
git stash
git pull
git stash pop
```

Or commit your work first:

```bash
git add .
git commit -m "Save work"
git pull
```

Avoid these for normal synchronization:

```bash
git reset --hard
git clean
git push --force
```
