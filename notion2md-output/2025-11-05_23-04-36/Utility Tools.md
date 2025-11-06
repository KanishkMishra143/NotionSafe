# Git 

	### Config

	
```bash
	git config user.name <username>
	git config user.email <email>
git init
```

	### Status

	`git status`

	![Pasted_image_20230530152714.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/8cd5e48f-eea8-48aa-9b9f-82b5b8f37c80/Pasted_image_20230530152714.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466WNHQRPY6%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173454Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCyKBPvso%2FtcPA40rxpzY6eqPRRzpU2gVyC85emAEGRcgIgbXypw%2Fb3E1cxZv5zaDKT6ptwDMdi%2BAPxVlL%2Fk5iJTNQqiAQIj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDCcqIOqoR%2ByYvN2XkircA5psZc%2Fkxiw58EPzXZV0eYtDcbxWnGq5LVeYfkEfeU7%2BdhHZvGV1Pz5R5l3S5Rx6T0iHOnuedh6HvW5oo2pXhoGQWubLZg2lixXxrEcxYJJs3fhOwj1aNjaThQLRibkPESQfzpQG7DZn3V5sxCAPl59lnYQPpJHEaCIZAAAeGGdlV7OcheXj8PHaGVbz5zVJh%2Bf34bg5ZLgmoR4z0IEmgbcrZS9bMAVo%2F2upR%2FsDbIvyV8STMzXCEO3MGgnkFOJfS90Qa%2FJNi38E7ZUVZoNTvtsHaE156Jy8nu%2BaSqxV%2F7n1uNQN9IdfpUeT2e%2FHZ3BYjZHzz1z5gjCwlp%2BZFgXINMfRq5aJvxFv%2BEgutuwyLpPzNvuzKg4AgYuugc2k3QJAa9rQbnyoMoJqSTc2anlNUvalYD%2FgIEao9VeixdczqRj9HEQd5LDIVTTddk1z8cU3oeQvKoC7V%2BZ4ytL9Sy8w7zVf%2BQ7aiPJ7MVyKJMdz3aiTyDxbFTNoEkBiyGDGDP62CAhRMz5RiIv8bVcf3nqopSjzU4cwY8R1WLU291fjitWof%2FHVR9zgxtkeO69tyuEtGtVpJxpwqMew4QGm3mhXJ17mH2ekGDlNj%2Bn0AxIFtb%2BvJ5bOGUmzPi%2BQkKiBMKOsrcgGOqUB2Bkw3agd4Xz9dV5tEDXPU84Q6%2FZVHzUwPSa0DbvBSgCVhsfUJDtoZXIc%2Bk7tMZwFssZSJrMjxJ20vjVqGn7IBkYyMGRVt1f937C%2BCWQlAMto1JI0P%2BZ2NvRzxda6S08bk8z0p7DZ8iSXj1u%2FisGGdC0JWXlyDAHasCsRZxHaj%2B1P6UPx%2BxqS7DTGCOl5JzkwQX6di%2FX%2BqWuevPYI1q3IIZaNMykq&X-Amz-Signature=6ad49a193a5295e411dc884739bb13467ecf604d09413739d99fdf7a9cd446c8&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

	### Shorthand Status

	`git status -s`

	![Pasted_image_20230530155456.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/c6b79f54-45b7-44b9-bc0e-e86af70ecdad/Pasted_image_20230530155456.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB466WNHQRPY6%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173454Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJHMEUCIQCyKBPvso%2FtcPA40rxpzY6eqPRRzpU2gVyC85emAEGRcgIgbXypw%2Fb3E1cxZv5zaDKT6ptwDMdi%2BAPxVlL%2Fk5iJTNQqiAQIj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARAAGgw2Mzc0MjMxODM4MDUiDCcqIOqoR%2ByYvN2XkircA5psZc%2Fkxiw58EPzXZV0eYtDcbxWnGq5LVeYfkEfeU7%2BdhHZvGV1Pz5R5l3S5Rx6T0iHOnuedh6HvW5oo2pXhoGQWubLZg2lixXxrEcxYJJs3fhOwj1aNjaThQLRibkPESQfzpQG7DZn3V5sxCAPl59lnYQPpJHEaCIZAAAeGGdlV7OcheXj8PHaGVbz5zVJh%2Bf34bg5ZLgmoR4z0IEmgbcrZS9bMAVo%2F2upR%2FsDbIvyV8STMzXCEO3MGgnkFOJfS90Qa%2FJNi38E7ZUVZoNTvtsHaE156Jy8nu%2BaSqxV%2F7n1uNQN9IdfpUeT2e%2FHZ3BYjZHzz1z5gjCwlp%2BZFgXINMfRq5aJvxFv%2BEgutuwyLpPzNvuzKg4AgYuugc2k3QJAa9rQbnyoMoJqSTc2anlNUvalYD%2FgIEao9VeixdczqRj9HEQd5LDIVTTddk1z8cU3oeQvKoC7V%2BZ4ytL9Sy8w7zVf%2BQ7aiPJ7MVyKJMdz3aiTyDxbFTNoEkBiyGDGDP62CAhRMz5RiIv8bVcf3nqopSjzU4cwY8R1WLU291fjitWof%2FHVR9zgxtkeO69tyuEtGtVpJxpwqMew4QGm3mhXJ17mH2ekGDlNj%2Bn0AxIFtb%2BvJ5bOGUmzPi%2BQkKiBMKOsrcgGOqUB2Bkw3agd4Xz9dV5tEDXPU84Q6%2FZVHzUwPSa0DbvBSgCVhsfUJDtoZXIc%2Bk7tMZwFssZSJrMjxJ20vjVqGn7IBkYyMGRVt1f937C%2BCWQlAMto1JI0P%2BZ2NvRzxda6S08bk8z0p7DZ8iSXj1u%2FisGGdC0JWXlyDAHasCsRZxHaj%2B1P6UPx%2BxqS7DTGCOl5JzkwQX6di%2FX%2BqWuevPYI1q3IIZaNMykq&X-Amz-Signature=87bdd668be43558e9159ef85ff65a209a3975e0182d1b4b669c764c6935130fe&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

