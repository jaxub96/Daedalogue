# Git / GitHub Cheat Sheet

## The basic model

```text
Your files
   ↓ git add
Staging area
   ↓ git commit
Local Git repository
   ↓ git push
GitHub

GitHub
   ↓ git fetch
Remote history on your computer
   ↓ git pull / git merge
Your local branch
```

- Git = version control on your computer.
- GitHub = remote copy of the repository.
- Commit = saved snapshot.
- Push = upload commits to GitHub.
- Fetch = download information from GitHub without changing your files.
- Pull = fetch + merge.
- Branch = separate line of development.
- `origin` = conventional name for your GitHub repository.
- `origin/main` = your local reference to GitHub's `main`.

## Everyday workflow

Start working:

```bash
git status
git pull
```

Make changes, then save them:

```bash
git add .
git commit -m "Describe what changed"
git push
```

Check what you changed:

```bash
git status
git diff
```

See history:

```bash
git log --oneline --graph --decorate
```

For a single-person, multiple-computer setup, this is usually all you need:

```bash
git pull
# work
git add .
git commit -m "Describe changes"
git push
```

## Checking before doing anything

```bash
git status
```

Shows:
- modified files
- deleted files
- untracked files
- current branch
- whether you're ahead/behind GitHub

```bash
git log --oneline --graph --decorate -10
```

Shows recent commits and branches.

```bash
git remote -v
```

Shows which GitHub repository you're connected to.

## Saving work

Stage everything:

```bash
git add .
```

Stage one file:

```bash
git add "path/to/file"
```

Commit:

```bash
git commit -m "Add new dialogue"
```

Push:

```bash
git push
```

The important distinction:

```text
git add     → prepare changes
git commit  → save changes locally
git push    → upload saved commits to GitHub
```

## Getting changes from GitHub

Safest way to inspect remote changes first:

```bash
git fetch origin
```

This downloads the remote information but doesn't modify your files.

Then:

```bash
git log --oneline main..origin/main
```

Shows commits that are on GitHub but not on your local `main`.

If your local work is already committed and you simply want the latest GitHub version:

```bash
git pull
```

## When Git refuses to pull

If you see:

```text
Your local changes would be overwritten by merge
```

You have uncommitted work.

If you want to keep it:

```bash
git stash
git pull
git stash pop
```

If you want to permanently save it:

```bash
git add .
git commit -m "Save work in progress"
git pull
```

If you don't need the local changes:

```bash
git restore .
```

Be careful: this discards uncommitted modifications.

## Stashing

Temporarily save unfinished work:

```bash
git stash
```

Include new untracked files:

```bash
git stash -u
```

See stashes:

```bash
git stash list
```

Restore the latest stash and remove it:

```bash
git stash pop
```

Restore without removing it:

```bash
git stash apply
```

Delete a stash:

```bash
git stash drop
```

A stash is local. It is not uploaded to GitHub.

## Undoing changes

Undo modifications to a file that haven't been committed:

```bash
git restore "path/to/file"
```

Undo all uncommitted tracked changes:

```bash
git restore .
```

Unstage a file while keeping its modifications:

```bash
git restore --staged "path/to/file"
```

Undo the most recent commit while keeping the changes:

```bash
git reset --soft HEAD~1
```

Undo the most recent commit and discard its changes:

```bash
git reset --hard HEAD~1
```

`--hard` is dangerous because it can permanently discard tracked changes.

## Recovering an old version

Find commits:

```bash
git log --oneline
```

Temporarily look at an old commit:

```bash
git checkout <commit>
```

Return to `main`:

```bash
git checkout main
```

Make your branch exactly match an old commit:

```bash
git reset --hard <commit>
```

For example:

```bash
git reset --hard 81a5ce7
```

## Reverting a commit

If a commit has already been pushed and you want to undo it without rewriting history:

```bash
git revert <commit>
```

This creates a new commit that reverses the old one.

Prefer `git revert` for commits that are already shared.

## Branches

Create a branch:

```bash
git branch feature-name
```

Switch to it:

```bash
git switch feature-name
```

Create and switch in one command:

```bash
git switch -c feature-name
```

See branches:

```bash
git branch
```

Switch back:

```bash
git switch main
```

Merge a branch:

```bash
git switch main
git merge feature-name
```

Delete a local branch:

```bash
git branch -d feature-name
```

## GitHub branches

Push a new branch to GitHub:

```bash
git push -u origin feature-name
```

After that, regular:

```bash
git push
```

is enough.

Update your knowledge of all remote branches:

```bash
git fetch origin
```

## Merge vs. rebase

Merge:

```bash
git merge origin/main
```

Combines two histories and can create a merge commit.

Rebase:

```bash
git rebase origin/main
```

Moves your local commits on top of the latest remote commits.

For a beginner working alone, you generally don't need rebase. Stick with `pull`/`merge` until you have a reason to use it.

## Remote vs local

These are different things:

```text
main
```

Your local branch.

```text
origin/main
```

Your computer's record of GitHub's `main`.

```text
GitHub main
```

The actual branch on GitHub.

`git fetch` updates your local `origin/main`:

```text
GitHub main
     ↓ fetch
origin/main
```

It does not change your local `main`.

`git pull` goes further:

```text
GitHub main
     ↓ fetch
origin/main
     ↓ merge
local main
```

## Important: Git tracks files, not folders

Git doesn't really track empty folders.

It tracks files inside them.

If a file is deleted in a commit, that deletion becomes part of Git history. Therefore, when you merge that commit, Git may delete the corresponding file on your computer.

This is why accidental deletions can propagate:

```text
Computer A:
file exists

Computer B:
file exists

Remote:
file was committed as deleted

git pull / merge
       ↓
Git applies the deletion
```

Git cannot know that the deletion was accidental.

## Untracked files

Check:

```bash
git status
```

If you see:

```text
Untracked files:
    myfile.txt
```

Git isn't tracking that file yet.

Add it:

```bash
git add myfile.txt
```

Then commit it:

```bash
git commit -m "Add myfile"
```

An untracked file generally won't be deleted by a normal `git merge` or `git reset --hard`.

However, this command can delete untracked files:

```bash
git clean -fd
```

Use it very carefully.

## Comparing versions

Compare your current branch with GitHub:

```bash
git diff main origin/main
```

See only changed filenames:

```bash
git diff --name-status main origin/main
```

The letters mean:

```text
A = Added
M = Modified
D = Deleted
```

See commits GitHub has that you don't:

```bash
git log main..origin/main --oneline
```

See commits you have that GitHub doesn't:

```bash
git log origin/main..main --oneline
```

## Conflicts

A conflict means Git cannot automatically decide which version to use.

Check:

```bash
git status
```

Git will identify conflicted files.

After resolving them manually:

```bash
git add .
git commit
```

If you want to abandon the merge:

```bash
git merge --abort
```

## Commands to be careful with

These are powerful and can destroy work:

```bash
git reset --hard
git restore .
git clean -fd
git push --force
git push --force-with-lease
```

Before using any of them, make sure you understand exactly what you are discarding or overwriting.

## Recommended workflow for a two-computer setup

On whichever computer you're starting work:

```bash
git status
git pull
```

Work normally.

When finished:

```bash
git status
git add .
git commit -m "Describe changes"
git push
```

Then, on the other computer:

```bash
git status
git pull
```

The most important rule:

> **Commit and push before switching computers; pull before starting work on the other computer.**

When something unexpected happens, don't immediately run `reset --hard`, `clean`, or `force-push`.

First run:

```bash
git status
git log --oneline --graph --decorate -10
```

Those two commands usually tell you what state you're actually in.
