# 📦 EQUAI AI - INSTALLATION GUIDE

Complete step-by-step installation instructions for Equai AI.

---

## 🎯 PREREQUISITES

Before installing Equai AI, ensure you have the following installed on your system:

### Required Software

1. **Python 3.8 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, check "Add Python to PATH"
   - Verify installation: Open command prompt and run `python --version`

2. **Node.js 16 or higher**
   - Download from: https://nodejs.org/
   - Install LTS (Long Term Support) version
   - Verify installation: Run `node --version` and `npm --version`

3. **Internet Connection**
   - Required for MongoDB Atlas connection
   - Required for downloading dependencies

### Optional (Recommended)

- **Git** for version control
- **VS Code** or any code editor
- Modern web browser (Chrome, Firefox, Edge)

---

## 📥 INSTALLATION STEPS

### Step 1: Navigate to Project Directory

Open Command Prompt or PowerShell and navigate to the Equai AI folder:

```bash
cd C:\Users\SHIRUH\OneDrive\Desktop\EquaAI
```

---

### Step 2: Install Backend Dependencies

#### Option A: Using pip (Recommended)

```bash
cd backend
python -m pip install flask flask-cors sympy matplotlib numpy pymongo python-dotenv dnspython
```

#### Option B: Using requirements.txt

```bash
cd backend
python -m pip install -r requirements.txt
```

**Expected Output:**
```
Collecting flask...
Collecting sympy...
...
Successfully installed flask-3.0.0 sympy-1.12 matplotlib-3.8.2 ...
```

#### Verify Backend Installation

```bash
python -c "import flask, sympy, matplotlib; print('All packages installed successfully!')"
```

---

### Step 3: Install Frontend Dependencies

Open a **new** command prompt/terminal window:

```bash
cd C:\Users\SHIRUH\OneDrive\Desktop\EquaAI\frontend
npm install
```

**Expected Output:**
```
npm install
added 200 packages...
```

**Note:** This may take 2-5 minutes depending on your internet speed.

#### Verify Frontend Installation

```bash
npm list react vite tailwindcss
```

Should show installed versions of React, Vite, and Tailwind.

---

### Step 4: Configure Environment Variables

The `.env` file in the backend folder is already configured with MongoDB connection:

**File:** `backend/.env`
```
MONGODB_URI=mongodb+srv://nthigacharles2_db_user:cjzdyA5EXA0SC8Kj@cluster0.v6xblzm.mongodb.net/?appName=Cluster0
DATABASE_NAME=equai_db
FLASK_ENV=development
PORT=5000
```

**No changes needed** - MongoDB Atlas is already configured!

---

## 🚀 RUNNING THE APPLICATION

### Option 1: Automatic Startup (Easiest)

**Double-click:** `start-all.bat`

This will:
1. ✅ Start the backend server on port 5000
2. ✅ Start the frontend on port 5173
3. ✅ Open both in separate command windows

### Option 2: Manual Startup

#### Terminal 1 - Backend Server

```bash
cd C:\Users\SHIRUH\OneDrive\Desktop\EquaAI\backend
python app.py
```

**Expected Output:**
```
Starting Equai AI Backend Server...
Successfully connected to MongoDB
 * Running on http://0.0.0.0:5000
```

**Leave this terminal running!**

#### Terminal 2 - Frontend Server

Open a **new** terminal window:

```bash
cd C:\Users\SHIRUH\OneDrive\Desktop\EquaAI\frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

**Leave this terminal running too!**

---

## 🌐 ACCESSING THE APPLICATION

1. **Open your web browser**
2. **Navigate to:** http://localhost:5173
3. **You should see:** The Equai AI interface with the header, input area, and tips section

### Verify Backend is Running

Open: http://localhost:5000/health

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "Equai AI Backend",
  "version": "1.0.0"
}
```

---

## ✅ FIRST TEST

### Test 1: Solve an Algebra Problem

1. In the web interface, select **Algebra**
2. Enter: `x^2 - 4 = 0`
3. Click **Solve Problem**
4. You should see:
   - Solution: x = -2, x = 2
   - Step-by-step explanation
   - Verification of solutions

### Test 2: Generate a Graph

1. Select **Graph**
2. Enter: `sin(x)`
3. Click **Solve Problem**
4. You should see:
   - Function analysis
   - Beautiful graph visualization
   - Critical points and intercepts

### Test 3: Calculus Derivative

1. Select **Calculus**
2. Select **Derivative** operation
3. Enter: `x^3 + 2*x^2`
4. Click **Solve Problem**
5. You should see:
   - Derivative result
   - Power rule explanation
   - Step-by-step derivation

---

## 🔧 TROUBLESHOOTING

### Problem: "python is not recognized"

**Solution:**
1. Add Python to PATH during installation
2. Or reinstall Python with "Add to PATH" checked
3. Restart command prompt after installation

### Problem: "npm is not recognized"

**Solution:**
1. Reinstall Node.js
2. Restart command prompt
3. Verify with `node --version`

### Problem: Backend won't start - "ModuleNotFoundError"

**Solution:**
```bash
cd backend
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### Problem: Frontend won't start - "ENOENT" or package errors

**Solution:**
```bash
cd frontend
rm -rf node_modules
rm package-lock.json
npm install
```

### Problem: Port already in use

**Backend (5000):**
```bash
# Find process using port
netstat -ano | findstr :5000
# Kill the process
taskkill /PID <process_id> /F
```

**Frontend (5173):**
```bash
# Find process
netstat -ano | findstr :5173
# Kill the process
taskkill /PID <process_id> /F
```

### Problem: MongoDB connection error

**Check:**
1. Internet connection is active
2. MongoDB URI in `.env` is correct
3. No firewall blocking MongoDB Atlas

**Test Connection:**
```bash
cd backend
python -c "from database import db; print('MongoDB connected!')"
```

### Problem: Graphs not displaying

**Solutions:**
1. Verify Matplotlib is installed:
   ```bash
   python -c "import matplotlib; print('OK')"
   ```
2. Check if `static/graphs` folder exists in backend
3. Create it manually if needed:
   ```bash
   cd backend
   mkdir static
   mkdir static\graphs
   ```

### Problem: CORS errors in browser

**Solution:**
- Ensure flask-cors is installed
- Check backend is running on port 5000
- Frontend API URL in `src/services/api.js` should be `http://localhost:5000/api`

---

## 📊 SYSTEM REQUIREMENTS

### Minimum Requirements
- **OS:** Windows 10, macOS 10.14+, or Linux
- **RAM:** 4 GB
- **Disk Space:** 500 MB
- **Python:** 3.8+
- **Node.js:** 16+

### Recommended Requirements
- **OS:** Windows 11, macOS 12+, or Ubuntu 22.04+
- **RAM:** 8 GB
- **Disk Space:** 1 GB
- **Python:** 3.10+
- **Node.js:** 18+ LTS
- **Internet:** Broadband connection

---

## 🔄 UPDATING THE APPLICATION

### Update Backend Dependencies
```bash
cd backend
python -m pip install --upgrade -r requirements.txt
```

### Update Frontend Dependencies
```bash
cd frontend
npm update
```

---

## 🛑 STOPPING THE APPLICATION

### Stop Backend
In the backend terminal, press `Ctrl + C`

### Stop Frontend
In the frontend terminal, press `Ctrl + C`

### Using start-all.bat
Simply close both command windows that opened.

---

## 📝 POST-INSTALLATION CHECKLIST

- [ ] Python installed and accessible
- [ ] Node.js and npm installed
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend server starts successfully
- [ ] Frontend server starts successfully
- [ ] Can access http://localhost:5173
- [ ] Backend health check returns "healthy"
- [ ] Can solve an algebra problem
- [ ] Can generate a graph
- [ ] Can perform calculus operations
- [ ] MongoDB connection working

---

## 🎓 NEXT STEPS

After successful installation:

1. **Read the Quick Start Guide:** `QUICKSTART.md`
2. **Try example problems** from the documentation
3. **Explore the UI features**
4. **Check the Project Summary:** `PROJECT_SUMMARY.md`
5. **Start solving your own math problems!**

---

## 📞 GET HELP

### Check Logs

**Backend Logs:**
- Displayed in backend terminal
- Look for error messages or stack traces

**Frontend Logs:**
- Open browser Developer Tools (F12)
- Check Console tab for errors
- Check Network tab for failed requests

### Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `ModuleNotFoundError` | Missing Python package | Run `pip install <package>` |
| `ENOENT` | Missing Node modules | Run `npm install` |
| `Port already in use` | Port occupied | Kill process or change port |
| `MongoDB connection failed` | Network/config issue | Check internet and .env file |
| `404 Not Found` | Backend not running | Start backend server |

---

## ✨ SUCCESS INDICATORS

You've successfully installed Equai AI when you can:

✅ Start both backend and frontend servers
✅ Access the web interface at localhost:5173
✅ Solve an algebra problem and see steps
✅ Generate a graph visualization
✅ Perform calculus operations
✅ See detailed explanations for each step

---

## 🎉 CONGRATULATIONS!

You've successfully installed **Equai AI**!

Now you can:
- Solve any algebra problem
- Compute derivatives and integrals
- Visualize functions with graphs
- Learn math with step-by-step explanations

**Enjoy your math journey with Equai AI!** ✨

---

**Need more help?** Check out:
- `README.md` - Project overview
- `QUICKSTART.md` - Usage guide
- `PROJECT_SUMMARY.md` - Technical details
