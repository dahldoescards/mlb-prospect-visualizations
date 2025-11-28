# Deployment Instructions

## Step 1: Open Terminal

**On Mac:**
- Press `Cmd + Space` to open Spotlight
- Type "Terminal" and press Enter
- Or go to: Applications → Utilities → Terminal

**On Windows:**
- Press `Win + R`, type `cmd` and press Enter
- Or search for "Command Prompt" in the Start menu

**On Linux:**
- Press `Ctrl + Alt + T` (most distributions)
- Or search for "Terminal" in your applications

## Step 2: Navigate to the Project Directory

In the terminal, type:

```bash
cd /Users/andrewdahl/mlb-prospect-visualizations
```

Press Enter. You should see the prompt change to show you're in that directory.

## Step 3: Create GitHub Repository First

**Before running the git commands**, you need to create the repository on GitHub:

1. Go to https://github.com
2. Click the "+" icon in the top right
3. Select "New repository"
4. Name it (e.g., `mlb-prospect-visualizations`)
5. Make it **Public** (required for free GitHub Pages)
6. **DO NOT** check "Initialize with README" (we already have files)
7. Click "Create repository"

## Step 4: Run Git Commands

Copy and paste these commands **one at a time** into your terminal, replacing `YOUR_USERNAME` and `REPO_NAME`:

```bash
# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: MLB prospect visualizations"

# Add your GitHub repository (REPLACE YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Set main branch
git branch -M main

# Push to GitHub
git push -u origin main
```

**Example** (if your username is `johndoe` and repo is `mlb-prospect-visualizations`):
```bash
git remote add origin https://github.com/johndoe/mlb-prospect-visualizations.git
```

## Step 5: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** (top menu)
3. Click **Pages** (left sidebar)
4. Under "Source", select:
   - Branch: **main**
   - Folder: **/ (root)**
5. Click **Save**
6. Wait 1-2 minutes for deployment
7. Your site will be at: `https://YOUR_USERNAME.github.io/REPO_NAME/`

## Troubleshooting

**If you get "command not found":**
- Make sure you're in the correct directory: `pwd` should show `/Users/andrewdahl/mlb-prospect-visualizations`
- Make sure git is installed: `git --version`

**If you get authentication errors:**
- You may need to set up GitHub authentication
- GitHub now requires a Personal Access Token instead of password
- See: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

**If files don't appear:**
- Make sure you ran `git add .` before commit
- Check with `git status` to see what's staged

