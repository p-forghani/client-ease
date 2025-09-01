# ClientEase Deployment Guide - Render (Free)

## 🚀 Quick Deployment Steps

### 1. Prepare Your Repository
- [x] All deployment files are ready (`render.yaml`, `Procfile`, `requirements.txt`, `runtime.txt`)
- [x] Code is committed to Git repository
- [x] Repository is pushed to GitHub

### 2. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub account
3. Connect your GitHub repository

### 3. Deploy Database
1. In Render dashboard, click "New +"
2. Select "PostgreSQL"
3. Choose "Free" plan
4. Name it: `client-ease-db`
5. Click "Create Database"
6. **Save the connection string** - you'll need it later

### 4. Deploy Web Service
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `client-ease`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && flask db upgrade`
   - **Start Command**: `gunicorn client_ease:app`
   - **Plan**: Free

### 5. Set Environment Variables
In your Render web service settings, add these environment variables:

```
FLASK_ENV=production
SECRET_KEY=<generate-a-secure-random-key>
SECURITY_PASSWORD_SALT=<generate-a-secure-random-salt>
EMAIL_VERIFICATION_SALT=<generate-a-secure-random-salt>
DATABASE_URL=<your-postgresql-connection-string>
BREVO_API_KEY=<your-brevo-api-key>
```

### 6. Generate Secure Keys
Use this Python script to generate secure keys:
```python
import secrets
print("SECRET_KEY=" + secrets.token_hex(32))
print("SECURITY_PASSWORD_SALT=" + secrets.token_hex(32))
print("EMAIL_VERIFICATION_SALT=" + secrets.token_hex(32))
```

### 7. Get Brevo API Key
1. Go to [brevo.com](https://brevo.com) (formerly Sendinblue)
2. Create free account
3. Go to Settings > API Keys
4. Create new API key
5. Copy the key to your Render environment variables

### 8. Deploy
1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Your app will be available at: `https://client-ease.onrender.com`

## 🔧 Post-Deployment Setup

### 1. Create Admin User
After deployment, you'll need to create an admin user. You can do this by:
1. Registering a new account through the web interface
2. Or running a script to create an admin user

### 2. Test All Features
- [ ] User registration and email verification
- [ ] Client management (CRUD)
- [ ] Project management (CRUD)
- [ ] Invoice creation and PDF download
- [ ] Dashboard functionality

## 📊 Render Free Tier Limits

### Web Service
- **Sleep**: App sleeps after 15 minutes of inactivity
- **Wake-up time**: ~30 seconds to wake up
- **Bandwidth**: 100GB/month
- **Build time**: 90 minutes/month

### Database
- **Storage**: 1GB
- **Connections**: 97 concurrent connections
- **Backup**: 7-day retention

## 🚨 Important Notes

### Free Tier Considerations
1. **Sleep Mode**: Your app will sleep after 15 minutes of inactivity
2. **Cold Starts**: First request after sleep takes ~30 seconds
3. **Database Limits**: 1GB storage limit
4. **Build Time**: Limited to 90 minutes/month

### Production Recommendations
For production use, consider upgrading to:
- **Starter Plan** ($7/month): No sleep, more resources
- **Standard Plan** ($25/month): Better performance, more storage

## 🔍 Troubleshooting

### Common Issues

1. **Build Fails**
   - Check `requirements.txt` for all dependencies
   - Ensure Python version is compatible

2. **Database Connection Error**
   - Verify `DATABASE_URL` is correct
   - Check database is running

3. **Email Not Working**
   - Verify `BREVO_API_KEY` is set correctly
   - Check Brevo account is active

4. **App Crashes on Startup**
   - Check logs in Render dashboard
   - Verify all environment variables are set

### Logs and Monitoring
- View logs in Render dashboard
- Monitor performance and errors
- Set up alerts for critical issues

## 🎯 Next Steps After Deployment

1. **Domain Setup**: Add custom domain (optional)
2. **SSL Certificate**: Automatically provided by Render
3. **Monitoring**: Set up error tracking (Sentry)
4. **Backup**: Regular database backups
5. **Scaling**: Upgrade plan as needed

## 📞 Support

- **Render Documentation**: [render.com/docs](https://render.com/docs)
- **ClientEase Issues**: Create GitHub issue
- **Community**: Flask community forums

---

**Your ClientEase MVP is now live! 🎉**
