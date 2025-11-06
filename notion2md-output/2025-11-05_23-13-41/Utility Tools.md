# Git 

	### Config

	
```bash
	git config user.name <username>
	git config user.email <email>
git init
```

	### Status

	`git status`

	![Pasted_image_20230530152714.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/8cd5e48f-eea8-48aa-9b9f-82b5b8f37c80/Pasted_image_20230530152714.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662IXZBFGJ%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T174506Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIGIbI7BQwyjjZzeEaT84ebYoJx%2FE6tAbkgj36W0d%2BcYdAiBAnPLNtJBny7q4gSPB9aLA%2FRnt3%2FSKCl8DU%2FhOy%2FKB%2BSqIBAiP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMaanDimTg1GgeTDfqKtwDhSVFjDIQScK1lyHPEqNyL97lLusaNRI2kilbMtiuMHttEouzZpCAl3VP9CYPqK6UZRRKZLDKxwCrZzz2eAneSeF51U9mxxK2mlzVl02gTW6QIPNOfJwd%2FY96hVI0xLl%2B0wGGGAuPSvxBIBKvZh91%2ByzgLu83C6JvfhItsfgCWk%2F9JQgOZUB0uSYHF852AMQ7m%2F%2FihnWkuMtEO5Kjq9Js3Hp%2BvGUGEHm81S8V0wPOG7yp%2BX6QAja7jBS9lqMmnjuO7eAvxPRnTvkx8BWl4u3D%2BZkwvmxyEtKPEYZdNpCTK4CAa1g9GopMOJuFczI1htVUsfg4py6CzU370twBV%2F3qhUZmq3mw6w9DJmYOkW%2F4M2Uq2%2Bsp%2BSfYd3Mkw7fuxSiV3MuF5y6j%2F2H9cG64V31Z8AlavyXl3q%2BzZMjVu%2BrKCrc%2FZMrwPRGeN8nW2D2uzxmZkXgPJBK%2FpHIO052xf5jB9xXCWjhysgp34%2BY1YSE6UpM2Z1FYEaSA2PzBEj9NmosqxGJ127G4WaS3THJub8aA0nDOCwFJXgauccdjPSvjk8tOXUDtdI4llLGQtAnCG4pfpAzhygSl7tDsxggueXQSz2xnsKkkWKGkXFz%2BI%2Bn%2BoS3vvRpQs7RufjLYrKcw6KutyAY6pgFoDocoGVaL6iOmEio7y6nLggMORO6BKT0SLju%2FwW9n3vCpk%2BDFBT1%2BrT9bLt%2BRZzRfUpawclMb5%2BDpDY2F97YedBshorD55%2BbpnqTVpmnUq9SJNqid%2FA%2FgApRDooftNPlQ6jNFyBrUmNdoHU4MTjWCrWlhRu32pfzisHV76BTnJDfXmkHsHj2mIV9lRTlCLdpqJh8wShT4k%2BQHoijN8RjPWEEe%2FfOd&X-Amz-Signature=d72b869c4b39526af9478bc9a29d38647fcde915b5f9ca024f71fbc8c76852f8&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

	### Shorthand Status

	`git status -s`

	![Pasted_image_20230530155456.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/c6b79f54-45b7-44b9-bc0e-e86af70ecdad/Pasted_image_20230530155456.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4662IXZBFGJ%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T174506Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJGMEQCIGIbI7BQwyjjZzeEaT84ebYoJx%2FE6tAbkgj36W0d%2BcYdAiBAnPLNtJBny7q4gSPB9aLA%2FRnt3%2FSKCl8DU%2FhOy%2FKB%2BSqIBAiP%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAAaDDYzNzQyMzE4MzgwNSIMaanDimTg1GgeTDfqKtwDhSVFjDIQScK1lyHPEqNyL97lLusaNRI2kilbMtiuMHttEouzZpCAl3VP9CYPqK6UZRRKZLDKxwCrZzz2eAneSeF51U9mxxK2mlzVl02gTW6QIPNOfJwd%2FY96hVI0xLl%2B0wGGGAuPSvxBIBKvZh91%2ByzgLu83C6JvfhItsfgCWk%2F9JQgOZUB0uSYHF852AMQ7m%2F%2FihnWkuMtEO5Kjq9Js3Hp%2BvGUGEHm81S8V0wPOG7yp%2BX6QAja7jBS9lqMmnjuO7eAvxPRnTvkx8BWl4u3D%2BZkwvmxyEtKPEYZdNpCTK4CAa1g9GopMOJuFczI1htVUsfg4py6CzU370twBV%2F3qhUZmq3mw6w9DJmYOkW%2F4M2Uq2%2Bsp%2BSfYd3Mkw7fuxSiV3MuF5y6j%2F2H9cG64V31Z8AlavyXl3q%2BzZMjVu%2BrKCrc%2FZMrwPRGeN8nW2D2uzxmZkXgPJBK%2FpHIO052xf5jB9xXCWjhysgp34%2BY1YSE6UpM2Z1FYEaSA2PzBEj9NmosqxGJ127G4WaS3THJub8aA0nDOCwFJXgauccdjPSvjk8tOXUDtdI4llLGQtAnCG4pfpAzhygSl7tDsxggueXQSz2xnsKkkWKGkXFz%2BI%2Bn%2BoS3vvRpQs7RufjLYrKcw6KutyAY6pgFoDocoGVaL6iOmEio7y6nLggMORO6BKT0SLju%2FwW9n3vCpk%2BDFBT1%2BrT9bLt%2BRZzRfUpawclMb5%2BDpDY2F97YedBshorD55%2BbpnqTVpmnUq9SJNqid%2FA%2FgApRDooftNPlQ6jNFyBrUmNdoHU4MTjWCrWlhRu32pfzisHV76BTnJDfXmkHsHj2mIV9lRTlCLdpqJh8wShT4k%2BQHoijN8RjPWEEe%2FfOd&X-Amz-Signature=7c5ef03a92b6e18ae9f69a5a09d4af2ad5a4ae4b78db7a84f4ce4c242917a47d&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

