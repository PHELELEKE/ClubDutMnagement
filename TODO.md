✅ **TODO.md created**
# ClubManagementSystem GitHub Deployment TODO

## Phase 1: GitHub Repo Setup [STEP 1/5 ✅]

### 1. Prerequisites Check 
- [✅] TODO.md created
- [ ] git --version  
- [ ] gh auth status

### 2. Root Files [4/4 ✅]
- [✅] `.gitignore`
- [✅] `README.md` 
- [✅] `Procfile`
- [✅] `runtime.txt`

### 3. Git Operations
```
git init
git add . 
git commit -m "Initial: DUT Club Management System v1.0"
git branch -M main
gh repo create PHELELEKE/ClubManagementSystem --public --push
```

**Next: Check git/gh → Create remaining files → git init**


### 2. Root Files Creation
- [ ] `.gitignore` (root level)
- [ ] `README.md` (full deploy docs)
- [ ] `Procfile` (Render deploy)
- [ ] `runtime.txt`

### 3. Git Operations
```
git init
git add .
git commit -m "Initial: Complete DUT Club Management System v1.0"
git branch -M main
gh repo create PHELELEKE/ClubManagementSystem --public --push
```

### 4. GitHub Pages Setup
```
git checkout -b gh-pages
mkdir docs
# Copy static demo to docs/
git add docs/
git commit -m "Add GitHub Pages static demo"
git push origin gh-pages
```
Settings → Pages → Source: Deploy from gh-pages branch

### 5. Live Deployment (Render.com)
1. render.com → New Web Service → Connect GitHub repo
2. Runtime: Python
3. Build: `pip install -r requirements.txt`
4. Start: `gunicorn run:app`
5. SQLite creates on first run (ephemeral - resets on restart)

## Phase 2: Development Workflow [SETUP]
```
# Local changes
1. Edit files in VSCode
2. git add .
3. git commit -m "feature: description"
4. git push
↓ Auto-deploys to Render + GitHub Pages
```

## Phase 3: Online Editing
- Edit directly on github.com/PHELELEKE/ClubManagementSystem
- Commits auto-deploy!

**Status: Starting Phase 1**
