# 🚀 RAILWAY DEPLOYMENT GUIDE

Railway is an excellent alternative to Vercel for Django applications with better Python support and no file upload limits.

## Quick Start

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   # or
   curl -fsSL https://railway.app/install.sh | sh
   ```

2. **Login and Deploy:**
   ```bash
   railway login
   railway new
   railway up
   ```

## Configuration

Railway will automatically:
- Detect Django project
- Install requirements.txt
- Set up PostgreSQL database (optional)
- Configure environment variables
- Deploy with zero downtime

## Environment Variables

Set these in Railway dashboard:
- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `ALLOWED_HOSTS=your-app.railway.app`
- `CORS_ALLOWED_ORIGINS=https://your-app.railway.app`

## Benefits over Vercel

✅ No file upload limits
✅ Better Django support
✅ Persistent storage
✅ Built-in database options
✅ WebSocket support
✅ Background tasks
✅ SSH access

## Deploy Now

```bash
cd /home/khouloud/Documents/all\ personnel\ \ projects/lagrange_animator
railway login
railway new
railway up
```

Your app will be available at: `https://your-app.railway.app`
