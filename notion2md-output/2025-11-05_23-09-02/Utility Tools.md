# Git 

	### Config

	
```bash
	git config user.name <username>
	git config user.email <email>
git init
```

	### Status

	`git status`

	![Pasted_image_20230530152714.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/8cd5e48f-eea8-48aa-9b9f-82b5b8f37c80/Pasted_image_20230530152714.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Z2WK2SVY%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173910Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCL3xXan9hm5XaR78tlmuWiC68OpqW%2BleOnxo9JGCN8LwIgcFZ2n5%2Ba%2FTxJcz2dIea0BIVRr4j78670rSdLbbUcv54qiAQIj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMPtxyGg6PqCPVdpVircA9SucWcSXbhYF2LTgXKvdXEgH4xCuUBK%2BFprvwdTf9mPUqgB6qqsAd0ERHn5REQJhCI8RAl9Fz998ZlhBxacC7vpaeQ1gd2qSd4%2FUvYHvRPLUf5a%2Bf8iEfWDY55B01DeLXwJGCnbm20A35lsSXpLqTy17TsFglQOd4vxBLdUvNa24edj%2BOC3tiK00k6qAnbnv4K%2FynLp1zt9hVCrRMMCOPRal%2Fpy9bKArnjweO2Uh8TttlZvDrSj%2BA3nUPWeDzWabBGGhgQWnfAmfw2zgccuFDZ%2FKlRxLOHTJlcVO5VksX9YbpY3DbIFYYbS2PZjEJA61b6Et5Fr7f3WZ0cM%2FqbSkjdhc5men6Qc10pWY1ftLFJFl7PqXoD0Lbi8h0UcByLro2bOiiw3h9UpUJCeaFvWFYolZMnR1JgaskiZKRl9CaZCtxddRdbKhKYeeUQoCiRaTXEi8TvrRHO%2BNt9k7jSBbqX29c5uVM53ERgvP8PBqdikOceP81mjWUbuoQw8zVL7xVkjQqw0OTOx%2FsdLUJM3UNl95rNrrdUiNhtBHw0EdE8IdbjEBBVXGVcCFdpPtB6A3HhAKOG3iwlwW1%2FiuMhX7xH6d%2FoniOQGgzV1D3zbNW0HspupsG%2BuPwvApJp7MIetrcgGOqUBa8WgO4yVENouk5uLEh7vIsg8bTwdUnodFWGHNaAaVFF8Hi%2BvtRbf%2F8pgkHhZlkT0UDj9et%2FmzrXFAB8%2BJv%2BBXwsicmZN5sTnYfEUYBTkuuYH7P8tO6a%2BZIpjcHd0DwzvkweBDHSlxvNbQPOmnZ%2BYirPVcGaZalt0zKLUHl45s576NZhaPd%2B7A3Jfj1%2BlVqZ6asxC64%2BezbxFnPKGIzWygNDVTg7z&X-Amz-Signature=d713944844252a09d532004a1c3954fa78cdfee32497ba16a081aca02549bf10&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

	### Shorthand Status

	`git status -s`

	![Pasted_image_20230530155456.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/c6b79f54-45b7-44b9-bc0e-e86af70ecdad/Pasted_image_20230530155456.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466Z2WK2SVY%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173910Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCL3xXan9hm5XaR78tlmuWiC68OpqW%2BleOnxo9JGCN8LwIgcFZ2n5%2Ba%2FTxJcz2dIea0BIVRr4j78670rSdLbbUcv54qiAQIj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDMPtxyGg6PqCPVdpVircA9SucWcSXbhYF2LTgXKvdXEgH4xCuUBK%2BFprvwdTf9mPUqgB6qqsAd0ERHn5REQJhCI8RAl9Fz998ZlhBxacC7vpaeQ1gd2qSd4%2FUvYHvRPLUf5a%2Bf8iEfWDY55B01DeLXwJGCnbm20A35lsSXpLqTy17TsFglQOd4vxBLdUvNa24edj%2BOC3tiK00k6qAnbnv4K%2FynLp1zt9hVCrRMMCOPRal%2Fpy9bKArnjweO2Uh8TttlZvDrSj%2BA3nUPWeDzWabBGGhgQWnfAmfw2zgccuFDZ%2FKlRxLOHTJlcVO5VksX9YbpY3DbIFYYbS2PZjEJA61b6Et5Fr7f3WZ0cM%2FqbSkjdhc5men6Qc10pWY1ftLFJFl7PqXoD0Lbi8h0UcByLro2bOiiw3h9UpUJCeaFvWFYolZMnR1JgaskiZKRl9CaZCtxddRdbKhKYeeUQoCiRaTXEi8TvrRHO%2BNt9k7jSBbqX29c5uVM53ERgvP8PBqdikOceP81mjWUbuoQw8zVL7xVkjQqw0OTOx%2FsdLUJM3UNl95rNrrdUiNhtBHw0EdE8IdbjEBBVXGVcCFdpPtB6A3HhAKOG3iwlwW1%2FiuMhX7xH6d%2FoniOQGgzV1D3zbNW0HspupsG%2BuPwvApJp7MIetrcgGOqUBa8WgO4yVENouk5uLEh7vIsg8bTwdUnodFWGHNaAaVFF8Hi%2BvtRbf%2F8pgkHhZlkT0UDj9et%2FmzrXFAB8%2BJv%2BBXwsicmZN5sTnYfEUYBTkuuYH7P8tO6a%2BZIpjcHd0DwzvkweBDHSlxvNbQPOmnZ%2BYirPVcGaZalt0zKLUHl45s576NZhaPd%2B7A3Jfj1%2BlVqZ6asxC64%2BezbxFnPKGIzWygNDVTg7z&X-Amz-Signature=4afa08193bede89a161f7608a5fdd93c0e014d8c646efc7d89936be3537862ad&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

