# Deployment Guide for Equai AI

This guide explains how to deploy the Equai AI application to both Vercel (frontend) and Render (backend).

## Prerequisites

1. Accounts:
   - [Vercel account](https://vercel.com/signup)
   - [Render account](https://render.com/)
   - MongoDB Atlas account (you already have this configured)

2. Tools:
   - Git
   - Node.js (v16+)
   - Python (3.8+)

## Deploying to Render (Backend)

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Create a new Web Service on Render**
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New+" and select "Web Service"
   - Connect your GitHub repository
   - Set the following options:
     - Name: `equai-ai-backend`
     - Region: Select the closest region
     - Branch: `main`
     - Root Directory: `backend`
     - Environment: `Python 3`
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `python app.py`
     - Plan: Free (or select a paid plan for better performance)

3. **Configure Environment Variables**
   In the "Advanced" section, add these environment variables:
   ```
   MONGODB_URI=your_mongodb_connection_string
   DATABASE_NAME=equai_db
   FLASK_ENV=production
   PORT=10000
   ```

4. **Deploy**
   Click "Create Web Service" and wait for the deployment to finish.

## Deploying to Vercel (Frontend)

1. **Build the frontend**
   ```bash
   cd frontend
   npm run build
   ```

2. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Add deployment configurations"
   git push origin main
   ```

3. **Import project to Vercel**
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "New Project"
   - Import your GitHub repository
   - Set the following options:
     - Framework Preset: `Vite`
     - Root Directory: `frontend`
     - Build Command: `npm run build`
     - Output Directory: `dist`

4. **Configure Environment Variables**
   No environment variables are needed for the frontend.

5. **Deploy**
   Click "Deploy" and wait for the deployment to finish.

## Setting Up the Production Environment

After deploying both services:

1. **Update your backend URL in the frontend**
   Once your Render backend is deployed, you'll get a URL like `https://your-app-name.onrender.com`.
   
   Update your frontend to use this URL by modifying `frontend/src/services/api.js`:
   ```javascript
   const API_BASE_URL = import.meta.env.DEV 
     ? 'http://localhost:5000/api' 
     : 'https://your-render-app-url.onrender.com/api';
   ```

2. **Re-deploy the frontend**
   Commit and push the changes, then redeploy on Vercel.

## Updating Your Application

To update your deployed applications:

1. **Backend (Render)**
   - Push changes to your GitHub repository
   - Render will automatically redeploy

2. **Frontend (Vercel)**
   - Push changes to your GitHub repository
   - Vercel will automatically redeploy

## Troubleshooting

1. **CORS Issues**
   If you encounter CORS issues, ensure your Flask backend has CORS enabled (it's already configured).

2. **API Connection Issues**
   Make sure your frontend is pointing to the correct backend URL in production.

3. **MongoDB Connection Issues**
   Verify your `MONGODB_URI` environment variable is correctly set on Render.

4. **Build Failures**
   Check the build logs on both platforms for specific error messages.