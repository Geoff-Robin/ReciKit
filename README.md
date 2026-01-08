# ReciKit

ReciKit is an intelligent recipe management and meal planning application designed to help users organize their inventory, discover new recipes, and plan their weekly meals with the help of AI agents.

## Project Structure

The project encompasses three main microservices/components:

1.  **Frontend (`/frontend`)**: A modern web interface built with React and Vite.
2.  **Backend (`/backend`)**: The core API service built with FastAPI, handling authentication, user data, and the conversational Chatbot Agent.
3.  **Recommendation Service (`/recommendation_service`)**: A specialized service focused on AI-driven recipe recommendations and meal plan generation using RAG (Retrieval-Augmented Generation) and MCP (Model Context Protocol).

## Tech Stack

-   **Frontend**: React, Vite, Tailwind CSS, Radix UI.
-   **Backend**: Python, FastAPI, MongoDB (Motor), LangChain, Groq.
-   **Recommendation Service**: Python, FastAPI, FastMCP (Model Context Protocol), Qdrant (Vector Database), Sentence Transformers.

## Prerequisites

-   **Node.js** (v18+)
-   **Python** (v3.10+)
-   **MongoDB** (Local or Atlas)
-   **Qdrant** (Local Docker instance or Cloud)

## Getting Started

### 1. Frontend Setup

Navigate to the `frontend` directory:

```bash
cd frontend
npm install
```

Create a `.env` file (if applicable) or configure environment variables as needed.

Start the development server:

```bash
npm run dev
```

The app will generally be available at `http://localhost:5173`.

### 2. Backend Setup

Navigate to the `backend` directory:

```bash
cd backend
# Install dependencies using uv
uv sync
```

Create a `.env` file in `backend/` with the following variables (example):

```env
MONGO_DB_URI=mongodb://localhost:27017
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_jwt_secret
ENV=development
PORT=3000
```

Start the backend server:

```bash
uv run main.py
```

The backend runs on port 3000 by default.

### 3. Recommendation Service Setup

Navigate to the `recommendation_service` directory:

```bash
cd recommendation_service
# Install dependencies using uv
uv sync
```

Create a `.env` file in `recommendation_service/` with:

```env
MONGO_DB_URI=mongodb://localhost:27017
QDRANT_URI=http://localhost:6333
QDRANT_API_KEY=your_qdrant_key (if applicable)
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile
PORT=8000
```

Start the service:

```bash
uv run main.py
```

The recommendation service runs on port 8000.

## Features

-   **Inventory Management**: Track ingredients you have at home.
-   **Smart Meal Planning**: Generate weekly meal plans based on your inventory, minimizing waste and shopping lists.
-   **Interactive Chat**: Talk to the "Chef" agent for cooking advice and recipe modifications.
-   **Preference Learning**: The system learns from your likes, dislikes, and allergies.
