# LUMA - Luminous AI Search

LUMA is an AI-enhanced search platform that combines traditional web search with AI analysis to provide comprehensive answers to your queries.

## Features

- Multi-model AI analysis from providers like Google (Gemini) and Meta (Llama)
- Web search integration with content extraction
- Beautiful, responsive UI with typewriter effect for AI responses
- Gradient design elements and modern interface

## Tech Stack

- **Frontend**: React, Tailwind CSS
- **Backend**: FastAPI, Python
- **AI Integration**: Google Gemini API, Groq API (for Llama models)

## Getting Started

### Prerequisites

- Node.js and npm
- Python 3.9+
- API keys for Google Gemini and Groq

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/luma.git
   cd luma
   ```

2. Set up the backend
   ```
   cd backend
   pip install -r requirements.txt
   cp .env.example .env  # Create and edit with your API keys
   ```

3. Set up the frontend
   ```
   cd frontend
   npm install
   ```

4. Start the development servers
   ```
   # Terminal 1 - Backend
   cd backend
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

   # Terminal 2 - Frontend
   cd frontend
   npm run dev
   ```

5. Open your browser and navigate to `http://localhost:5173`

## License

MIT 