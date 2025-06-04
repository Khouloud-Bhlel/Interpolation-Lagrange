# 🚀 Complete Vercel Deployment Setup

This guide will help you deploy your Lagrange Animator Django application to Vercel using GitHub Actions.

## 📁 Files Created for Deployment

### Core Configuration Files:
- `vercel.json` - Vercel deployment configuration
- `build_files.sh` - Build script for Vercel
- `.vercelignore` - Files to exclude from deployment
- `.env.production` - Production environment variables template

### GitHub Actions:
- `.github/workflows/vercel-deploy.yml` - Automated deployment workflow

### Helper Scripts:
- `setup-vercel.sh` - Automated setup script
- `VERCEL_DEPLOYMENT_GUIDE.md` - Detailed deployment guide

## 🚀 Quick Setup (Automated)

Run the setup script:
```bash
./setup-vercel.sh
```

## 🔧 Manual Setup Steps

### 1. Prerequisites
```bash
# Install Node.js (for Vercel CLI)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Vercel CLI
npm install -g vercel
```

### 2. Vercel Account Setup
1. Create account at [vercel.com](https://vercel.com)
2. Connect your GitHub account
3. Generate a token at [vercel.com/account/tokens](https://vercel.com/account/tokens)

### 3. Initialize Vercel Project
```bash
cd "/home/khouloud/Documents/all personnel  projects/lagrange_animator"
vercel login
vercel --yes
```

### 4. Configure GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `VERCEL_TOKEN`: Your Vercel token
- `VERCEL_ORG_ID`: From `.vercel/project.json`
- `VERCEL_PROJECT_ID`: From `.vercel/project.json`

### 5. Configure Vercel Environment Variables

In your Vercel project dashboard → Settings → Environment Variables:

```
SECRET_KEY=your-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=.vercel.app,.now.sh
CORS_ALLOWED_ORIGINS=https://your-app-name.vercel.app
VERCEL=1
```

### 6. Deploy
```bash
git add .
git commit -m "Add Vercel deployment configuration"
git push origin main
```

## 🌐 Post-Deployment Steps

### 1. Update CORS Settings
After deployment, update your Vercel environment variables:
```
CORS_ALLOWED_ORIGINS=https://your-actual-domain.vercel.app
```

### 2. Test Your Application
- Main interface: `https://your-app.vercel.app/`
- API endpoints: `https://your-app.vercel.app/api/`
- Admin panel: `https://your-app.vercel.app/admin/`

### 3. Database Considerations
The current setup uses SQLite (suitable for demo). For production:
- Consider Vercel's PostgreSQL addon
- Or use external database services like PlanetScale, Supabase, or Railway

## 🔍 Monitoring & Debugging

### Check Deployment Status
```bash
vercel logs
```

### Local Development with Vercel
```bash
vercel dev
```

### Common Issues & Solutions

1. **Static Files Not Loading**
   - Check `STATICFILES_STORAGE` setting
   - Ensure `whitenoise` is in middleware

2. **CORS Errors**
   - Update `CORS_ALLOWED_ORIGINS` with actual domain
   - Check Vercel environment variables

3. **Build Failures**
   - Check GitHub Actions logs
   - Verify all dependencies in `requirements.txt`

4. **Database Errors**
   - Migrations might need to run manually
   - Consider using external database for production

## 📊 Performance Optimization

### For Better Performance:
1. **Database**: Use external PostgreSQL
2. **Static Files**: Configure CDN
3. **Caching**: Add Redis for caching
4. **Media Files**: Use cloud storage (AWS S3, Cloudinary)

## 🔄 Continuous Deployment

The GitHub Actions workflow automatically:
- ✅ Runs Django checks
- ✅ Builds the application
- ✅ Deploys to Vercel
- ✅ Comments on PRs with preview URLs

## 🛠️ Advanced Configuration

### Custom Domain
1. Add domain in Vercel dashboard
2. Update DNS settings
3. Update environment variables

### Environment-Specific Settings
- **Preview**: Automatic for PR deployments
- **Production**: Manual promotion or main branch
- **Development**: Use `vercel dev`

## 📞 Support

If you encounter issues:
1. Check the [Vercel documentation](https://vercel.com/docs)
2. Review GitHub Actions logs
3. Use `vercel logs` for runtime errors
4. Check the Django deployment guide in `VERCEL_DEPLOYMENT_GUIDE.md`

---

🎉 **Your Lagrange Animator is now ready for the cloud!**
