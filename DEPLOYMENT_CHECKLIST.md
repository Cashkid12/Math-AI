# Deployment Checklist

Follow this checklist to deploy your Equai AI application to Render (backend) and Vercel (frontend).

## Pre-deployment Checklist

- [ ] Ensure all code is committed and pushed to GitHub
- [ ] Verify MongoDB Atlas connection works (test locally first)
- [ ] Check that all environment variables are properly configured
- [ ] Test the application locally in both development and production modes

## Backend Deployment (Render)

- [ ] Create a new Web Service on Render
- [ ] Connect your GitHub repository
- [ ] Set the following configuration:
  - Name: `equai-ai-backend`
  - Region: Select the closest region
  - Branch: `main`
  - Root Directory: `backend`
  - Environment: `Python 3`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app` (for production) or `python app.py`
  - Plan: Free (or select a paid plan)
- [ ] Configure Environment Variables:
  - [ ] `MONGODB_URI` (your MongoDB connection string)
  - [ ] `DATABASE_NAME` (equai_db)
  - [ ] `FLASK_ENV` (production)
  - [ ] `PORT` (10000)
- [ ] Deploy the service
- [ ] Note the deployed URL (e.g., https://equai-ai-backend.onrender.com)

## Frontend Deployment (Vercel)

- [ ] Build the frontend locally to test:
  ```bash
  cd frontend
  npm run build
  ```
- [ ] Commit and push any changes to GitHub
- [ ] Import project to Vercel:
  - [ ] Go to Vercel Dashboard
  - [ ] Click "New Project"
  - [ ] Import your GitHub repository
  - [ ] Set configuration:
    - Framework Preset: `Vite`
    - Root Directory: `frontend`
    - Build Command: `npm run build`
    - Output Directory: `dist`
- [ ] Deploy the project
- [ ] Note the deployed URL (e.g., https://equai-ai-frontend.vercel.app)

## Post-Deployment Configuration

- [ ] Update the frontend to use the production backend URL:
  - [ ] Modify `frontend/src/services/api.js` to point to your Render backend URL
  - [ ] Rebuild and redeploy the frontend
- [ ] Test the complete application:
  - [ ] Solve a math problem
  - [ ] Check that graphs are generated
  - [ ] Verify history and analytics work
- [ ] Set up custom domains if needed (optional)

## Monitoring and Maintenance

- [ ] Set up monitoring on Render for the backend
- [ ] Configure error tracking if needed
- [ ] Set up auto-scaling if expecting high traffic
- [ ] Regularly update dependencies for security

## Troubleshooting Common Issues

- [ ] **CORS errors**: Ensure CORS is properly configured in Flask (already done)
- [ ] **API connection issues**: Verify the frontend is pointing to the correct backend URL
- [ ] **MongoDB connection issues**: Check the MONGODB_URI environment variable
- [ ] **Build failures**: Check build logs on both platforms
- [ ] **Performance issues**: Consider upgrading from free tier to paid plans

## Useful Commands

```bash
# Build frontend and move to backend static folder
cd frontend
npm run build

# Test backend locally with production settings
cd backend
FLASK_ENV=production python app.py

# Commit and push changes
git add .
git commit -m "Prepare for deployment"
git push origin main
```