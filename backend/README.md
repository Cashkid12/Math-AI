# Equai AI - Backend

Flask backend for the Equai AI math solver application.

## Features

- **Advanced Math Solving**: Algebra, Calculus, and Function Analysis
- **Step-by-Step Explanations**: Detailed explanations for every calculation
- **Graph Generation**: Beautiful graphs using Matplotlib
- **MongoDB Integration**: Store problem history and analytics
- **RESTful API**: Clean API endpoints for frontend communication

## Setup

1. **Install Python dependencies**:
```bash
cd backend
pip install -r requirements.txt
```

2. **Configure environment**:
The `.env` file is already configured with MongoDB connection.

3. **Run the server**:
```bash
python app.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### POST /api/solve
Solve math problems with detailed steps.

**Request**:
```json
{
  "type": "algebra",
  "input": "x^2 + 2x - 3 = 0"
}
```

**Response**:
```json
{
  "solution": "[-3, 1]",
  "steps": ["..."],
  "explanations": ["..."],
  "detailed_steps": [{"step": "...", "explanation": "..."}]
}
```

### GET /api/graph?expr=sin(x)&xmin=-10&xmax=10
Generate and return graph image.

### GET /api/history?limit=20
Get recent solved problems.

### GET /api/analytics
Get usage statistics.

## Technologies

- Flask
- SymPy (symbolic mathematics)
- Matplotlib (graphing)
- NumPy
- MongoDB (via PyMongo)
