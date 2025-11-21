# Equai AI - Your Math Genius in an App

A full-stack AI-powered math-solving application that helps students solve algebra, calculus, and graphing problems with **detailed step-by-step explanations** and visual representations.

## 🎯 Features

### Mathematics Support
- ✅ **Algebra**: Solve equations, simplify expressions, find roots
- ✅ **Calculus**: Derivatives, integrals, limits with detailed steps
- ✅ **Graphing**: Beautiful function graphs with analysis
- ✅ **Step-by-Step Explanations**: Every step includes mathematical reasoning

### Technical Features
- 🚀 Real-time problem solving
- 📊 Graph visualization with Matplotlib
- 💾 MongoDB integration for problem history
- 🎨 Modern, responsive UI with Tailwind CSS
- 🌙 Beautiful dark theme
- 📱 Mobile-friendly design

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Math Engine**: SymPy (symbolic mathematics)
- **Graphing**: Matplotlib + NumPy
- **Database**: MongoDB
- **API**: RESTful with CORS support

### Frontend
- **Framework**: React 18 + Vite
- **Styling**: Tailwind CSS
- **HTTP Client**: Axios
- **Design**: Custom Equai AI design system

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB Atlas account (already configured)

### Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the Flask server
python app.py
```

Backend runs on `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

Frontend runs on `http://localhost:5173`

## 📖 Usage

1. **Open the app** in your browser at `http://localhost:5173`
2. **Select problem type**: Algebra, Calculus, or Graph
3. **Enter your expression**:
   - Algebra: `x^2 + 2x - 3 = 0`
   - Calculus: `x^3 + 2*x^2 - x`
   - Graph: `sin(x) + cos(x)`
4. **Click "Solve Problem"**
5. **View results**:
   - Solution with answer
   - Step-by-step explanation
   - Mathematical reasoning for each step
   - Graph visualization (if applicable)

## 🎓 Example Problems

### Algebra
```
x^2 - 4 = 0
2x + 5 = 11
x^3 - 8 = 0
```

### Calculus
```
Derivative: x^3 + 2*x^2 - x
Integral: sin(x) + cos(x)
Limit: (x^2 - 1)/(x - 1)
```

### Graphs
```
sin(x)
x^2 - 4*x + 3
exp(-x^2)
```

## 📁 Project Structure

```
EquaAI/
├── backend/
│   ├── app.py                 # Flask application
│   ├── config.py              # Configuration
│   ├── database.py            # MongoDB connection
│   ├── math_solver.py         # Math solving engine
│   ├── graph_generator.py     # Graph generation
│   ├── requirements.txt       # Python dependencies
│   └── .env                   # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API services
│   │   ├── App.jsx            # Main app component
│   │   └── index.css          # Global styles
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## 🎨 Design System

- **Primary Color**: `#1A73E8` (Blue)
- **Accent Color**: `#00C896` (Green)
- **Dark Background**: `#0E1117`
- **Card Background**: `#1A1F2E`
- **Fonts**: Poppins, Montserrat

## 🔌 API Endpoints

### POST `/api/solve`
Solve mathematical problems

### GET `/api/graph?expr=<expression>`
Generate function graph

### GET `/api/history`
Get solution history

### GET `/api/analytics`
Get usage statistics

## 🌟 Key Features Explained

### Detailed Step-by-Step Solutions
Every problem shows:
- Each mathematical step
- Explanation of what's happening
- Why that step is taken
- Visual highlighting of the process

### Enhanced Explanations
The AI not only shows calculations but **explains the reasoning**:
- "This is a quadratic equation (degree 2)"
- "Applying the power rule for polynomial terms"
- "Substituting x = 2 confirms it's a valid solution"

### Graph Analysis
For graphs, you get:
- Function visualization
- Derivative calculation
- Critical points
- Y-intercept
- X-intercepts (roots)

## 📝 MongoDB Configuration

The app is pre-configured with MongoDB Atlas:
- Connection string in `.env`
- Database: `equai_db`
- Collection: `problems`

## 🚀 Deployment

### Deploying to Render (Backend) and Vercel (Frontend)

Detailed deployment instructions are available in [DEPLOYMENT.md](DEPLOYMENT.md).

### Backend
Deploy to Render:
1. Push your code to GitHub
2. Create a new Web Service on Render
3. Connect your repository
4. Set environment variables
5. Deploy!

### Frontend
Deploy to Vercel:
1. Push your code to GitHub
2. Import your project to Vercel
3. Configure build settings
4. Deploy!

## 📱 Future Enhancements

- 🎤 Voice input for problems
- 📷 OCR for handwritten math
- 👤 User accounts and progress tracking
- 📊 Advanced analytics dashboard
- 🌐 Multi-language support
- 📱 React Native mobile app

## 🤝 Contributing

This is a demonstration project built for educational purposes.

## 📄 License

MIT License

## 👨‍💻 Author

Built with ❤️ for students and math learners worldwide.

---

**Equai AI** - Making math accessible, one step at a time! ✨