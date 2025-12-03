# How to Deploy to Vercel - Step by Step

## Step 1: Prepare Your Files

### Move API folder inside ml-dashboard:

**Windows PowerShell:**
```powershell
Move-Item -Path "api" -Destination "ml-dashboard\api"
```

**Windows CMD:**
```cmd
move api ml-dashboard\api
```

### Copy the dataset file to api folder:

**Windows PowerShell:**
```powershell
Copy-Item -Path "hybrid_dataset.pkl" -Destination "ml-dashboard\api\hybrid_dataset.pkl"
```

**Windows CMD:**
```cmd
copy hybrid_dataset.pkl ml-dashboard\api\hybrid_dataset.pkl
```

## Step 2: Install Vercel CLI

Open terminal/command prompt and run:
```bash
npm install -g vercel
```

## Step 3: Navigate to ml-dashboard folder

```bash
cd ml-dashboard
```

## Step 4: Login to Vercel

```bash
vercel login
```

This will open your browser to login. Follow the prompts.

## Step 5: Deploy to Vercel

### For first deployment (preview):
```bash
vercel
```

### For production deployment:
```bash
vercel --prod
```

Follow the prompts:
- **Set up and deploy?** → Type `Y` and press Enter
- **Which scope?** → Select your account
- **Link to existing project?** → Type `N` and press Enter (first time)
- **What's your project's name?** → Press Enter for default or type a name
- **In which directory is your code located?** → Press Enter (it's `./`)
- **Want to override the settings?** → Type `N` and press Enter

## Step 6: Set Environment Variable

1. Go to https://vercel.com/dashboard
2. Click on your project
3. Go to **Settings** → **Environment Variables**
4. Click **Add New**
5. Add:
   - **Key:** `VITE_API_URL`
   - **Value:** `/api`
   - **Environments:** Check all (Production, Preview, Development)
6. Click **Save**

## Step 7: Redeploy (if needed)

After adding environment variable, you may need to redeploy:
```bash
vercel --prod
```

Or trigger a redeploy from Vercel dashboard.

## Step 8: Test Your Deployment

Visit the URL provided by Vercel (something like `your-project.vercel.app`) and test the prediction form!

---

## Alternative: Deploy via GitHub (Easier)

### Option A: Using GitHub + Vercel Dashboard

1. **Push your code to GitHub:**
   - Create a new repository on GitHub
   - Make sure `api/` folder is inside `ml-dashboard/`
   - Make sure `hybrid_dataset.pkl` is in `ml-dashboard/api/`
   - Push your code

2. **Deploy on Vercel:**
   - Go to https://vercel.com/new
   - Click **Import Git Repository**
   - Select your GitHub repository
   - **Root Directory:** Set to `ml-dashboard`
   - Click **Deploy**

3. **Add Environment Variable:**
   - Go to Project Settings → Environment Variables
   - Add `VITE_API_URL` = `/api`
   - Redeploy

---

## Troubleshooting

### Issue: "Function not found" or "404"
- Make sure `api/` folder is inside `ml-dashboard/`
- Check that `api/predict.py` exists
- Verify `vercel.json` is in `ml-dashboard/`

### Issue: "Dataset file not found"
- Ensure `hybrid_dataset.pkl` is in `ml-dashboard/api/`
- Check file size (Vercel has 50MB limit per function)

### Issue: Build fails
- Check that all dependencies are in `package.json`
- Verify Python dependencies in `api/requirements.txt`
- Check Vercel build logs for errors

### Issue: API returns error
- Check Vercel function logs in dashboard
- Verify environment variable is set correctly
- Make sure dataset file is uploaded

---

## File Structure After Setup

```
ml-dashboard/
├── api/
│   ├── predict.py
│   ├── requirements.txt
│   └── hybrid_dataset.pkl  ← Must be here!
├── src/
├── vercel.json
├── package.json
└── ... (other files)
```

---

## Quick Commands Summary

```bash
# 1. Move files (PowerShell)
Move-Item -Path "api" -Destination "ml-dashboard\api"
Copy-Item -Path "hybrid_dataset.pkl" -Destination "ml-dashboard\api\hybrid_dataset.pkl"

# 2. Install Vercel CLI
npm install -g vercel

# 3. Navigate and deploy
cd ml-dashboard
vercel login
vercel --prod
```

