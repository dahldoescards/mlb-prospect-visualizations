# Setup Instructions for GitHub Pages

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `mlb-prospect-visualizations` or `bowman-prospect-charts`
3. Make it public (required for free GitHub Pages)
4. Do NOT initialize with README, .gitignore, or license (we already have these)

## Step 2: Initialize Git and Push Files

Run these commands in the project directory:

```bash
cd /Users/andrewdahl/mlb-prospect-visualizations

# Initialize git repository
git init

# Add all files
git add .

# Commit files
git commit -m "Initial commit: MLB prospect visualizations"

# Add your GitHub repository as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Enable GitHub Pages

1. Go to your repository on GitHub
2. Click on **Settings** (top menu)
3. Scroll down to **Pages** in the left sidebar
4. Under **Source**, select **Deploy from a branch**
5. Select **main** branch and **/ (root)** folder
6. Click **Save**
7. Your site will be available at: `https://YOUR_USERNAME.github.io/REPO_NAME/`

## Step 4: Wait for Deployment

GitHub Pages typically takes 1-2 minutes to deploy. You'll see a green checkmark when it's ready.

## Updating the Visualizations

If you need to regenerate the HTML files with updated data:

```bash
# Make sure mlb_analysis_results.json is in Downloads folder
python3 generate_visualizations.py

# Commit and push changes
git add *.html
git commit -m "Update visualizations with latest data"
git push
```

## Notes

- The `index.html` file serves as the main entry point
- Individual release HTML files are linked via tabs
- All visualizations use Plotly.js loaded from CDN (no local dependencies needed)
- Bootstrap is loaded from CDN for the tab navigation

