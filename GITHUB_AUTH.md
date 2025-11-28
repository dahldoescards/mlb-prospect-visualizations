# GitHub Authentication Setup

GitHub no longer accepts passwords for Git operations. You need to use a **Personal Access Token (PAT)** instead.

## Step 1: Create a Personal Access Token

1. Go to GitHub.com and sign in
2. Click your profile picture (top right) → **Settings**
3. Scroll down in the left sidebar and click **Developer settings**
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a name like "MLB Visualizations" or "Local Git"
7. Select an expiration (or "No expiration" if you prefer)
8. **Check these scopes:**
   - ✅ `repo` (full control of private repositories)
   - ✅ `workflow` (if you plan to use GitHub Actions)
9. Click **Generate token** at the bottom
10. **IMPORTANT:** Copy the token immediately - you won't be able to see it again!
   - It will look like: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

## Step 2: Use the Token as Your Password

When you run `git push -u origin main` and it asks for:
- **Username:** `dahldoescards` (your GitHub username)
- **Password:** Paste your Personal Access Token (NOT your GitHub password)

## Step 3: Alternative - Use SSH Instead

If you prefer, you can set up SSH keys to avoid entering credentials each time:

1. Generate SSH key: `ssh-keygen -t ed25519 -C "your_email@example.com"`
2. Add to GitHub: Settings → SSH and GPG keys → New SSH key
3. Change remote URL: `git remote set-url origin git@github.com:dahldoescards/mlb-prospect-visualizations.git`

## Quick Fix for Right Now

Just run the push command again and when prompted:
- Username: `dahldoescards`
- Password: Paste your Personal Access Token (the `ghp_...` token you created)

