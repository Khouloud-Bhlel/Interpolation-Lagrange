# Setup Guide for Vercel Deployment with GitHub Actions

## Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
3. **Vercel CLI**: Install globally with `npm install -g vercel`

## Step 1: Link Your Project to Vercel

1. Navigate to your project directory:
   ```bash
   cd "/home/khouloud/Documents/all personnel  projects/lagrange_animator"
   ```

2. Login to Vercel:
   ```bash
   vercel login
   ```

3. Initialize your project with Vercel:
   ```bash
   vercel
   ```
   - Choose "Link to existing project" if you have one, or create new
   - Follow the prompts to set up your project

## Step 2: Get Vercel Tokens and IDs

1. Get your Vercel token:
   - Go to [Vercel Dashboard](https://vercel.com/account/tokens)
   - Create a new token
   - Copy the token

2. Get your Organization ID and Project ID:
   ```bash
   vercel ls
   ```
   Or check the `.vercel/project.json` file after running `vercel`

## Step 3: Set GitHub Secrets

In your GitHub repository, go to Settings > Secrets and variables > Actions, then add:

1. **VERCEL_TOKEN**: Your Vercel token from Step 2
2. **VERCEL_ORG_ID**: Your organization ID  
3. **VERCEL_PROJECT_ID**: Your project ID

### How to Add GitHub Secrets:
1. Go to your GitHub repository
2. Click on "Settings" tab
3. In the left sidebar, click "Secrets and variables" > "Actions"
4. Click "New repository secret" for each secret
5. Add the name and value for each secret

## Step 4: Configure Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Navigate to Settings > Environment Variables
3. Add the following variables:

**Required Environment Variables:**
- `SECRET_KEY`: Generate a new Django secret key (use https://djecrety.ir/)
- `DEBUG`: Set to `False` for production
- `ALLOWED_HOSTS`: Your domain names (e.g., `your-app.vercel.app`)

**Optional Environment Variables:**
- `ODOO_URL`: If using Odoo integration
- `ODOO_DB`: Odoo database name
- `ODOO_USERNAME`: Odoo username
- `ODOO_PASSWORD`: Odoo password
2. Navigate to Settings > Environment Variables
3. Add the following variables for Production:

```
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.vercel.app,.now.sh
CORS_ALLOWED_ORIGINS=https://your-app.vercel.app
VERCEL=1
```

## Step 5: Push to GitHub

Your GitHub Actions workflow will automatically deploy when you push to main/master:

```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

## Step 6: Monitor Deployment

1. Check the Actions tab in your GitHub repository
2. Monitor the deployment process
3. Once successful, your app will be live on Vercel

## Troubleshooting

### Common Issues:

1. **Static Files**: Make sure `STATIC_ROOT` is properly configured
2. **Dependencies**: Ensure all dependencies are in `requirements.txt`
3. **Database**: SQLite works for demo; consider PostgreSQL for production
4. **CORS**: Update CORS settings with your actual Vercel domain

### Vercel Logs:
```bash
vercel logs your-deployment-url
```

### Local Testing:
```bash
vercel dev
```

## Production Considerations

1. **Database**: Consider using Vercel's PostgreSQL addon or external database
2. **Static Files**: Use Vercel's CDN for better performance
3. **Environment Variables**: Keep sensitive data in Vercel's environment variables
4. **Domain**: Add custom domain in Vercel dashboard if needed

## File Structure for Vercel

The key files for Vercel deployment are:
- `vercel.json` - Vercel configuration
- `build_files.sh` - Build script
- `.vercelignore` - Files to ignore during deployment
- `.github/workflows/vercel-deploy.yml` - GitHub Actions workflow
