# 🚀 EQUAI AI - QUICK START GUIDE

## Welcome to Equai AI!

Your AI-powered math solver with **detailed step-by-step explanations**.

---

## 📋 Prerequisites

Before running Equai AI, ensure you have:
- ✅ Python 3.8+ installed
- ✅ Node.js 16+ installed
- ✅ Internet connection (for MongoDB)

---

## 🎯 Installation & Setup

### Option 1: Automatic Startup (Recommended)

**Simply double-click `start-all.bat`**

This will:
1. Start the Flask backend server on port 5000
2. Start the React frontend on port 5173
3. Open both in separate command windows

### Option 2: Manual Startup

#### Backend Server

1. Open a terminal/command prompt
2. Navigate to backend folder:
   ```bash
   cd backend
   ```
3. Install dependencies (first time only):
   ```bash
   python -m pip install flask flask-cors sympy matplotlib numpy pymongo python-dotenv dnspython
   ```
4. Run the server:
   ```bash
   python app.py
   ```
5. You should see: `Server running on http://localhost:5000`

#### Frontend Server

1. Open a NEW terminal/command prompt
2. Navigate to frontend folder:
   ```bash
   cd frontend
   ```
3. Install dependencies (first time only):
   ```bash
   npm install
   ```
4. Run the development server:
   ```bash
   npm run dev
   ```
5. You should see: `Local: http://localhost:5173`

---

## 🌐 Accessing the Application

1. Open your web browser
2. Navigate to: **http://localhost:5173**
3. You should see the Equai AI interface!

---

## 💡 How to Use Equai AI

### 1. Select Problem Type

Choose from:
- **Algebra**: Solve equations (e.g., `x^2 + 2x - 3 = 0`)
- **Calculus**: Derivatives, integrals, limits
- **Graph**: Visualize functions

### 2. Enter Your Problem

Type your mathematical expression:
- Use `^` for exponents: `x^2` (x squared)
- Use `*` for multiplication: `2*x` (2 times x)
- Use `/` for division: `x/2` (x divided by 2)

### 3. Click "Solve Problem"

The AI will:
- ✅ Parse your input
- ✅ Solve the problem
- ✅ Show each step
- ✅ Explain the reasoning
- ✅ Display graphs (if applicable)

---

## 📚 Example Problems to Try

### Algebra Examples
```
x^2 - 4 = 0
2x + 5 = 11
x^3 - 8 = 0
x^2 + 5x + 6 = 0
```

### Calculus Examples

**Derivatives** (select Calculus → Derivative):
```
x^3 + 2*x^2 - x
sin(x) + cos(x)
exp(x) * x^2
```

**Integrals** (select Calculus → Integral):
```
x^2
sin(x)
1/x
```

**Limits** (select Calculus → Limit):
```
(x^2 - 1)/(x - 1)
sin(x)/x
```

### Graph Examples
```
sin(x)
x^2 - 4*x + 3
exp(-x^2)
cos(x) + sin(2*x)
```

---

## 🎨 Special Features

### ✨ Detailed Step-by-Step Explanations

Unlike other calculators, Equai AI **explains each step**:

**Example: Solving x² + 2x - 3 = 0**

Step 1: `Original equation: x² + 2x - 3 = 0`
💡 *Starting with the given equation*

Step 2: `This is a quadratic equation (degree 2)`
💡 *Applying the quadratic formula to find solutions*

Step 3: `Solutions: x = -3, x = 1`
💡 *There are 2 solutions to this equation*

Step 4: `Verification: For x = -3: 0 ✓`
💡 *Substituting x = -3 confirms it's a valid solution*

### 📊 Graph Analysis

For graphing problems, you get:
- Beautiful visual graph
- Derivative calculation
- Critical points (maxima/minima)
- Y-intercept
- X-intercepts (roots)

### ⌨️ Keyboard Shortcuts

- Press `Ctrl + Enter` to solve quickly!

---

## 🔧 Troubleshooting

### Backend won't start?
- Check if Python is installed: `python --version`
- Ensure port 5000 is not in use
- Check MongoDB connection in `.env` file

### Frontend won't start?
- Check if Node.js is installed: `node --version`
- Run `npm install` in frontend folder
- Ensure port 5173 is not in use

### Cannot solve problems?
- Check if backend is running (http://localhost:5000/health should return "healthy")
- Check browser console for errors (F12)
- Ensure your input uses correct syntax (`^` for powers)

### Graphs not showing?
- Check if Matplotlib is installed
- Verify backend static folder exists
- Check browser network tab for 404 errors

---

## 📊 MongoDB Integration

Your problems are saved to MongoDB Atlas for:
- Problem history
- Usage analytics
- Learning progress tracking

Connection details are in `backend/.env`

---

## 🎓 Tips for Best Results

1. **Use clear notation**:
   - Good: `x^2 + 2*x - 3`
   - Avoid: `x2 + 2x - 3` (missing operators)

2. **For equations, use `=`**:
   - Algebra: `x^2 = 4` or `x^2 - 4 = 0`

3. **For calculus, just the expression**:
   - Just: `x^3 + 2*x`
   - Not: `x^3 + 2*x = 0`

4. **Use parentheses for clarity**:
   - Good: `(x + 1)^2`
   - Good: `sin(2*x)`

---

## 🌟 What Makes Equai AI Special?

### 1. Educational Focus
- Not just answers, but **understanding**
- Every step is explained in plain language
- Learn the "why" behind each calculation

### 2. Beautiful Design
- Modern, clean interface
- Dark theme for comfortable viewing
- Responsive on all devices

### 3. Comprehensive Coverage
- Algebra to advanced calculus
- Symbolic and numeric solutions
- Visual representations

### 4. Production-Quality Code
- Well-structured backend
- Clean React components
- RESTful API design

---

## 📱 Future Features (Coming Soon)

- 🎤 Voice input for problems
- 📷 Photo recognition for handwritten math
- 👤 User accounts and progress tracking
- 📊 Advanced analytics dashboard
- 🌐 Mobile app (React Native)

---

## ❓ Need Help?

### Mathematical Notation
- `^` : Power (x^2 = x²)
- `*` : Multiply (2*x)
- `/` : Divide (x/2)
- `sin(x)`, `cos(x)`, `tan(x)` : Trigonometric functions
- `exp(x)` : e^x
- `log(x)` : Natural logarithm
- `sqrt(x)` : Square root

### Common Issues
- **"Could not parse expression"**: Check your syntax
- **"No real solutions"**: Equation has no real number solutions
- **"Error occurred"**: Check if backend is running

---

## 🎉 Ready to Start!

1. ✅ Both servers running
2. ✅ Browser open to http://localhost:5173
3. ✅ Try the example problems
4. ✅ Explore the step-by-step explanations
5. ✅ Solve your own math problems!

---

**Equai AI - Your Math Genius in an App** ✨

Made with ❤️ for students and math learners worldwide.
