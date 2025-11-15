# My Blog 2.0 - Backend API

A FastAPI-based simple backend for a personal blog application with support for posts, comments, and image uploads.

## Features

- **Post Management**: Create, read, and manage blog posts
- **Comments System**: Users can comment on posts
- **Image Upload**: Support for featured images on posts
- **View Tracking**: Track unique post views with viewer IDs
- **CORS Support**: Configured for cross-origin requests
- **Async Database**: PostgreSQL with async SQLAlchemy ORM

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (async)
- **ORM**: SQLAlchemy (async)
- **Validation**: Pydantic
- **File Storage**: Local filesystem

## Project Structure

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── posts.py          # Post endpoints
│   │       ├── comments.py       # Comment endpoints
│   │       └── router.py         # API router setup
│   ├── core/
│   │   ├── config.py             # Settings and configuration
│   │   └── dirs.py               # Directory paths
│   ├── db/
│   │   ├── database.py           # Database connection
│   │   └── functions/
│   │       ├── posts.py          # Post database operations
│   │       └── comments.py       # Comment database operations
│   ├── middleware/
│   │   └── request_logger.py     # Request logging middleware
│   ├── models/
│   │   ├── post.py               # Post model
│   │   ├── comment.py            # Comment model
│   │   └── schemas/
│   │       ├── posts.py          # Post schemas
│   │       ├── comments.py       # Comment schemas
│   │       ├── errors.py         # Error schemas
│   │       └── base.py           # Base schemas
│   └── utils/
│       └── logging_config.py     # Logging configuration
├── public/
│   └── images/                   # Uploaded images storage
├── main.py                       # Application entry point
├── run.py                        # Development server runner
├── requirements.txt              # Python dependencies
├── .env.development              # Development environment variables
├── .env.production               # Production environment variables
└── README.md                     # This file
```

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd backend
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the appropriate env file
   cp .env.development .env  # For development
   # Or
   cp .env.production .env   # For production
   ```

   Update the `.env` file with your configuration:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/blog_db
   ENVIRONMENT=development
   SECRET_WORD=your_secret_word_here
   ```

5. **Run the application**
   ```bash
   python run.py
   ```

   The API will be available at `http://localhost:8000`

## API Endpoints

### Posts

- `GET /api/v1/posts/` - Get all posts
- `GET /api/v1/posts/{post_id}` - Get a specific post by ID
- `POST /api/v1/posts/` - Create a new post (requires authentication)

### Comments

- `POST /api/v1/comments/` - Create a new comment on a post

## Environment Variables

- `DATABASE_URL` - PostgreSQL connection string (async)
- `ENVIRONMENT` - Environment mode (development/production)
- `SECRET_WORD` - Secret word required for creating posts
- `ENV` - Environment type (used by config.py)

**Author**: Akbar  
**Created**: 2025