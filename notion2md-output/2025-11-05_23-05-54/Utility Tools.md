# Git 

	### Config

	
```bash
	git config user.name <username>
	git config user.email <email>
git init
```

	### Status

	`git status`

	![Pasted_image_20230530152714.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/8cd5e48f-eea8-48aa-9b9f-82b5b8f37c80/Pasted_image_20230530152714.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466XNMA7REJ%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173559Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIA4HX2X4kzhFTikzHh28vLz4l4HtMBbs6YEJTtcTdfydAiAEAYfSXlRLrLr3Hxr4y7PM5BtXuoFHqurEdN8ZJjYcBCqIBAiP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIM17Ft6W4OqvZvlb4YKtwDniM7Q0IKxJUbBawKLctKw2n1lXsQ5WR3ZHcGwXH0exvtMc6daLxWysaqn9bZ7v5ofrw6m4%2FY7%2B2yxo%2FxqUZaNzIsmDN6KZANCEc8ogp3%2BZ3R6vi%2BkZfyhDi0xe8%2FCoANcxmroqiTpLmJIesHqObOE1gx0rDaldk4Ccpb8rBIDqpmbjNvMdwWozO2CHG3KU1IjhDLdrdkdF6T0UxYTiobfcPaeqdHFpOHwFGEjz1eIOuDxXZgCQ2yY%2FAtyVenMgHgqEGGxUCRS%2B3HzaBke4HS1SAyFlEZDhutTs05CU2Z0vWPe95pVvID5LGfmszc1fIduwQN7mNGDUEz5gOH4gz6zerYyHBM5Mn2iOf%2BXco4u3AiCCBiJfoFQh3YjjRHdIKKH8u7Vaqi%2BzLgPQ%2BJGmreNLntCN5fJu9xsQT6fdS3POpMdKH7wXYOr7SwCSTYzHuAeBLDuS0V6exfTlitIX%2FYMQeFDrFg9adslIKz8rIgcxMxt08w5Nk9kF%2B7W6Ikh0ZvXv14qx6RERrT%2BpaZLaVrR1cJTLch5PNPnWKpbPsOXHxNjBhBGOOf%2F9lzLY7M1y6YIkcXb%2BE0ze%2FiL8J6NRNtUarYQhpzuNwGlb9PCwN7XPP4yNOtxVmwJgFLWAswta2tyAY6pgH0FETgY4db7JyBFgEA0AnU8c23VD8%2FxXNFKWd17qHSlDAYwBFLuROQehHNe2m4HYvgSuqwpGS%2FtXSwLSZl0pCK1fW%2Bu2PHxajlmyJUtpC4%2BoDUyulkOpK1glj99V5TTHsmXJ1vxdarztP5cEeT%2BMiLBi5hJGKjQZMkteKcB6%2FsgZ5amd3OK5pkzt3vxUTs%2BXuCh0%2FudIoIQgjzxDWjfwDyS5dARqbO&X-Amz-Signature=158e4d564aae566cb12babca98af32171d9c9042029d0fbc6bfb8a3b46585592&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

	### Shorthand Status

	`git status -s`

	![Pasted_image_20230530155456.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/c6b79f54-45b7-44b9-bc0e-e86af70ecdad/Pasted_image_20230530155456.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466XNMA7REJ%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173559Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIA4HX2X4kzhFTikzHh28vLz4l4HtMBbs6YEJTtcTdfydAiAEAYfSXlRLrLr3Hxr4y7PM5BtXuoFHqurEdN8ZJjYcBCqIBAiP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIM17Ft6W4OqvZvlb4YKtwDniM7Q0IKxJUbBawKLctKw2n1lXsQ5WR3ZHcGwXH0exvtMc6daLxWysaqn9bZ7v5ofrw6m4%2FY7%2B2yxo%2FxqUZaNzIsmDN6KZANCEc8ogp3%2BZ3R6vi%2BkZfyhDi0xe8%2FCoANcxmroqiTpLmJIesHqObOE1gx0rDaldk4Ccpb8rBIDqpmbjNvMdwWozO2CHG3KU1IjhDLdrdkdF6T0UxYTiobfcPaeqdHFpOHwFGEjz1eIOuDxXZgCQ2yY%2FAtyVenMgHgqEGGxUCRS%2B3HzaBke4HS1SAyFlEZDhutTs05CU2Z0vWPe95pVvID5LGfmszc1fIduwQN7mNGDUEz5gOH4gz6zerYyHBM5Mn2iOf%2BXco4u3AiCCBiJfoFQh3YjjRHdIKKH8u7Vaqi%2BzLgPQ%2BJGmreNLntCN5fJu9xsQT6fdS3POpMdKH7wXYOr7SwCSTYzHuAeBLDuS0V6exfTlitIX%2FYMQeFDrFg9adslIKz8rIgcxMxt08w5Nk9kF%2B7W6Ikh0ZvXv14qx6RERrT%2BpaZLaVrR1cJTLch5PNPnWKpbPsOXHxNjBhBGOOf%2F9lzLY7M1y6YIkcXb%2BE0ze%2FiL8J6NRNtUarYQhpzuNwGlb9PCwN7XPP4yNOtxVmwJgFLWAswta2tyAY6pgH0FETgY4db7JyBFgEA0AnU8c23VD8%2FxXNFKWd17qHSlDAYwBFLuROQehHNe2m4HYvgSuqwpGS%2FtXSwLSZl0pCK1fW%2Bu2PHxajlmyJUtpC4%2BoDUyulkOpK1glj99V5TTHsmXJ1vxdarztP5cEeT%2BMiLBi5hJGKjQZMkteKcB6%2FsgZ5amd3OK5pkzt3vxUTs%2BXuCh0%2FudIoIQgjzxDWjfwDyS5dARqbO&X-Amz-Signature=766683f16f1a381a70318028226bbb57b4cc3823955c416cf43bcd3c78dfddcb&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

	### Create

	To Create an empty file - `touch <file>.extn`  like .html or .py or .cpp

	### Staging

	`git add <FILE> `or` ``**git add -A**`

	### Commit

	- `git commit <FILE> `

	- `git commit -a -m "<SKIP STAGING AREA>"`      (***Not recommended***)

	- `git commit -m "MESSAGE"`

	### gitignore

	- `touch .gitignore*.log`      (*Ignores all the files with this ext.*)

		- `log/`     ('/'* this tells git that it's a directory, & to ignore it)*

	### git diff

	- Shows difference between working directory and stage - `git diff`

	- To see diff between stage and the last commit - `git diff --staged`

	### Restoring

	- `git restore <FILE> `

	- `git restore -f`

	### Logs

	- `git log -p -<no. of last commits to see>`

	### Removing

	- `git restore --staged <FILE>`      (*Remove from Stage, Make it untracked*)

	- `git rm <FILE>`     (*Remove from HDD as well as git*)

	### Branch

	- `git branch <branch name>`     (*creates a branch*)

	- `git checkout <branch name>`     (*switches to the branch)*

	- `git checkout -b <branch name>`     (*creates a new branch and also switches to it)*

	### Merge

	- switch to the branch
`git merge <some other branch>`     (*present branch and selected branch gets merged*)

	<br/>

	### Clone

	- `git clone https://github.com/libgit2/libgit2` this clone in a new directory within called `libgit2`  

	- `git clone ``[https://github.com/libgit2/libgit2](https://github.com/libgit2/libgit2)`` mylibgit`  this clones at location, in a dir named `mylibgit` in arg, and inside a `libgit2` directory

# GitHub

	### Add Repository

	- `git remote add orgin <SSH URL>`     (***origin ****is alias of the repository*)

	- fetch and push URL can be obtained by - `git remote -v`

	### Getting GitHub Repo Setup

	- `ssh-keygen -t rsa -b 4096 -C "kanishk.kumar412@gmail.com"`

	- `eval $(ssh-agent -s)`

	- `ssh-add ~/.ssh/id_rsa`

	- `cat ~/.ssh/id_rsa.pub`     (*prints the key*)

	- create a new SSH key in GitHub, with the above obtained key.

	- Set new SSH URL - `git remote set-url origin <SSH URL>`

	### Push

	- Switch to the branch to push `git push -u <repo name> <branch name>`

	- `git push -u {branch name}`      (this stores the command after -u for quick use by command `git push)`

# Maintaining Multiple Repos on a single machine

	### 1. Copy over the already generated SSH keys ;

	- `id_rsa` = private key

	- `*.pub` = public key (which is added into github or AUR)

	- `kanishk_github` = private key for (KanishkMishra143)

	- `kanishk_github.pub` = public key for (KanishkMishra143)

	### 2. Setting proper permissions

	
```javascript
cd ~/.ssh

# Set folder permissions
chmod 700 ~/.ssh

# Private keys (restrict to user only)
chmod 600 id_rsa
chmod 600 gitlab_key
chmod 600 collab_kanishk
chmod 600 kanishk_github

# Public keys (readable by everyone)
chmod 644 id_rsa.pub
chmod 644 gitlab_key.pub
chmod 644 collab_kanishk.pub
chmod 644 kanishk_github.pub

# Config and known hosts
chmod 644 config
chmod 644 known_hosts
chmod 644 known_hosts.old

# Fix ownership in case it got copied as root or another user
sudo chown -R $USER:$USER ~/.ssh
```

	### 3. Global Config

	- `git init` (If required)

	- `git config —global ``[user.email](http://user.email/)`` <email.@gmail.com>`

	- `git config —global user.username <username>`

	### 4. Local Config (New Local repo)

	- `git init`

	- `git config ``[user.email](http://user.email/)`` <email.@gmail.com>`

	- `git config user.username <username>`

	### 5. New Repository

	- Make a repository on Github without LICENSE or README

	- `git remote add origin <ssh-url> `(first time origin setup to remote repo)

	- `git remote set-url origin <ssh-url>` (for correcting origin url after it is set the first time)

	- `git push -u origin main`  (`-u` saves origin and main, so that `git push` can be used for easy use)

[//]: # (link_to_page is not supported)

<br/>

