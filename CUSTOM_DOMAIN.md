# Using a Custom Domain for GitHub Pages

To make your GitHub Pages URL more professional (instead of `username.github.io/repo-name`), you can use a custom domain like `bowmananalysis.com` or `prospectstats.com`.

## Option 1: Use a Subdomain (Easier)

If you own a domain (e.g., `dahldoescards.com`), you can use a subdomain like `bowman.dahldoescards.com`:

### Steps:

1. **Create a CNAME file in your repository:**
   ```bash
   cd /Users/andrewdahl/mlb-prospect-visualizations
   echo "bowman.dahldoescards.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS with your domain provider:**
   - Go to your domain registrar (GoDaddy, Namecheap, etc.)
   - Add a CNAME record:
     - **Type:** CNAME
     - **Name:** bowman (or whatever subdomain you want)
     - **Value:** `dahldoescards.github.io`
     - **TTL:** 3600 (or default)

3. **Enable custom domain in GitHub:**
   - Go to your repo → Settings → Pages
   - Under "Custom domain", enter: `bowman.dahldoescards.com`
   - Check "Enforce HTTPS" (wait a few minutes for SSL certificate)

## Option 2: Use Root Domain (More Complex)

To use `dahldoescards.com` directly (without subdomain):

1. **Create CNAME file:**
   ```bash
   echo "dahldoescards.com" > CNAME
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

2. **Configure DNS:**
   - Add **A records** pointing to GitHub's IPs:
     - `185.199.108.153`
     - `185.199.109.153`
     - `185.199.110.153`
     - `185.199.111.153`
   - OR use a CNAME pointing to `dahldoescards.github.io` (some providers support this)

3. **Enable in GitHub Settings → Pages**

## Option 3: Buy a New Domain

If you don't have a domain, you can buy one:

- **Namecheap:** ~$10-15/year
- **Google Domains:** ~$12/year
- **GoDaddy:** ~$12-15/year

Good domain name ideas:
- `bowmananalysis.com`
- `prospectstats.com`
- `bowmanprospects.com`
- `mlbprospectdata.com`

## Quick Setup (If You Have a Domain)

1. Create CNAME file:
   ```bash
   cd /Users/andrewdahl/mlb-prospect-visualizations
   echo "yourdomain.com" > CNAME
   ```

2. Add to git:
   ```bash
   git add CNAME
   git commit -m "Add custom domain"
   git push
   ```

3. Configure DNS with your domain provider (see steps above)

4. Wait 24-48 hours for DNS to propagate

## Testing

After setup, test with:
```bash
dig yourdomain.com
# or
nslookup yourdomain.com
```

## Notes

- **HTTPS:** GitHub automatically provides SSL certificates for custom domains (free!)
- **Propagation:** DNS changes can take 24-48 hours to fully propagate
- **CNAME file:** Must be in the root of your repository
- **Case sensitive:** Domain names in CNAME should be lowercase

## If You Don't Want a Custom Domain

The current GitHub Pages URL (`dahldoescards.github.io/mlb-prospect-visualizations`) is perfectly fine and professional. Many major projects use GitHub Pages URLs. The custom domain is optional!

