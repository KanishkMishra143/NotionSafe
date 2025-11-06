# Git 

	### Config

	
```bash
	git config user.name <username>
	git config user.email <email>
git init
```

	### Status

	`git status`

	![Pasted_image_20230530152714.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/8cd5e48f-eea8-48aa-9b9f-82b5b8f37c80/Pasted_image_20230530152714.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665HR4J62E%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173206Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCpsFd4lc91yU4jeTSRqJ8mSHG7UgFJPH0xWJG5JcJy0QIhAN9aYyEEErcond6qW7hADZaugfP5k6OPMMHX53vcj6%2BoKogECI%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgztubspN6wMTyg9syoq3AMah1qHiBjdbBb4SAa0%2FPOSsrGsMWFWjSBF0KBXO5KvQgE8UMCsAEX%2BGIvchc0PjAwI46V15uQDQKksuOUI7ylOvj1pl2BvmW0gvB7QBo5QlaXy7%2FFvQIk1QCmCjHWxfOqhto1aSxFjnw4L8PXNYbvkkdm0MLLXd9g%2BAtnGnKAdYNsaDLcTKRENcf%2F86ilzUX9YpSld2aovFOkWq2vU%2F1PcgWMevdBNL2VD%2FA5qkYLhIuEiSvAzNe8C0RTLSw9KuSlaVIvm%2B%2FJ3me3%2FGK9NJCZ8%2FWeBv3OKY%2FaGKyM77hmblwjabBkTCk3oZ78sYr8xa5jEwiEBMlsttzK%2F0KVcr%2BFN5V8duCcvEeogud%2BJBLDDIs676hMFqh%2FrV9HgIEz0%2BJ6yGi1RFZR0x1isWDrV2vtbN%2BGZS%2Fzc7Ge2Uy79d4rFMgMhPIWf35nJ%2BK981%2FkXs1a5f8AOyYCXMHFL0VQ%2FMgbfK3liayPBoJ3Lxf6NDYcX7WfCWXt%2BecqaDQI1V53KQt9Lkuk7rSSsKrQYwXn1M37%2FDwsxIIu0XyUXwhaqLtjMlhkL0P2PCb60AiCZK%2BR%2Fi7aomWSPQfzfM6qKaxaWxVjI4aqHGHm7NrSRiWo2K9gzSipaAhBrXt2BNeWb%2BzCTra3IBjqkAXdb8ux9DgHOtjj3Hf60PT%2BSuARtv%2FMeJWfhZmbQ8PditRJAa7zP77uMePyTWYDmMQ1Ss2kZ9LogJZnXWCaN41jlr1S0FISVCFAYrgNrWs%2B0AgJvci696PZY6DptxscGOMZDSuMNwRJo%2Bd9gjXn2WCyUVYIDgNpS63omfpLFbjdy2u6aiATyqIVB9B5Gvz%2FWZMN8yLnOx10OIdwZm3pSxuRq9JaU&X-Amz-Signature=bb0185fb70cc60f78d9e887ec0e19b12affc7e9355aa4d2000452c55ad643503&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

	### Shorthand Status

	`git status -s`

	![Pasted_image_20230530155456.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8b5a29e4-b818-4730-8ee4-77eca8830c79/c6b79f54-45b7-44b9-bc0e-e86af70ecdad/Pasted_image_20230530155456.png?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZI2LB4665HR4J62E%2F20251105%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20251105T173206Z&X-Amz-Expires=3600&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMiJIMEYCIQCpsFd4lc91yU4jeTSRqJ8mSHG7UgFJPH0xWJG5JcJy0QIhAN9aYyEEErcond6qW7hADZaugfP5k6OPMMHX53vcj6%2BoKogECI%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQABoMNjM3NDIzMTgzODA1IgztubspN6wMTyg9syoq3AMah1qHiBjdbBb4SAa0%2FPOSsrGsMWFWjSBF0KBXO5KvQgE8UMCsAEX%2BGIvchc0PjAwI46V15uQDQKksuOUI7ylOvj1pl2BvmW0gvB7QBo5QlaXy7%2FFvQIk1QCmCjHWxfOqhto1aSxFjnw4L8PXNYbvkkdm0MLLXd9g%2BAtnGnKAdYNsaDLcTKRENcf%2F86ilzUX9YpSld2aovFOkWq2vU%2F1PcgWMevdBNL2VD%2FA5qkYLhIuEiSvAzNe8C0RTLSw9KuSlaVIvm%2B%2FJ3me3%2FGK9NJCZ8%2FWeBv3OKY%2FaGKyM77hmblwjabBkTCk3oZ78sYr8xa5jEwiEBMlsttzK%2F0KVcr%2BFN5V8duCcvEeogud%2BJBLDDIs676hMFqh%2FrV9HgIEz0%2BJ6yGi1RFZR0x1isWDrV2vtbN%2BGZS%2Fzc7Ge2Uy79d4rFMgMhPIWf35nJ%2BK981%2FkXs1a5f8AOyYCXMHFL0VQ%2FMgbfK3liayPBoJ3Lxf6NDYcX7WfCWXt%2BecqaDQI1V53KQt9Lkuk7rSSsKrQYwXn1M37%2FDwsxIIu0XyUXwhaqLtjMlhkL0P2PCb60AiCZK%2BR%2Fi7aomWSPQfzfM6qKaxaWxVjI4aqHGHm7NrSRiWo2K9gzSipaAhBrXt2BNeWb%2BzCTra3IBjqkAXdb8ux9DgHOtjj3Hf60PT%2BSuARtv%2FMeJWfhZmbQ8PditRJAa7zP77uMePyTWYDmMQ1Ss2kZ9LogJZnXWCaN41jlr1S0FISVCFAYrgNrWs%2B0AgJvci696PZY6DptxscGOMZDSuMNwRJo%2Bd9gjXn2WCyUVYIDgNpS63omfpLFbjdy2u6aiATyqIVB9B5Gvz%2FWZMN8yLnOx10OIdwZm3pSxuRq9JaU&X-Amz-Signature=8832a399ceb8d9927936d54a440f0093a1eb6778e2c77fa35f54fb47268b800e&X-Amz-SignedHeaders=host&x-amz-checksum-mode=ENABLED&x-id=GetObject)

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

