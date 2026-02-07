# Meka (Capisnap)

Full-stack caption generator:
- **Backend**: Flask API (auth, caption generation, MongoDB persistence, optional Cloudinary upload)
- **Frontend**: React app (Create React App)

## Repo Structure

- `backend/` Flask API
- `frontend/` React UI

## Prerequisites

- Python **3.10+** (recommended)
- Node.js **18+** and npm
- MongoDB (local or MongoDB Atlas)

## Quick Start (Windows / PowerShell)

### 1) Backend (Flask)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Create `backend/.env`:

```env
# Required
MONGO_URI=mongodb://localhost:27017/capisnap
JWT_SECRET_KEY=change-me
SECRET_KEY=change-me

# Optional (only needed if you want Cloudinary uploads)
CLOUD_NAME=your_cloud_name
CLOUD_API_KEY=your_api_key
CLOUD_API_SECRET=your_api_secret
```

Run the API:

```powershell
python app.py
```

API will start on `http://localhost:5000`.

Health check:
- `GET http://localhost:5000/health`

### 2) Frontend (React)

```powershell
cd ..\frontend
npm install
```

Optional: set the API base URL in `frontend/.env` (defaults to `http://localhost:5000`):

```env
REACT_APP_API_BASE_URL=http://localhost:5000
```

Run the UI:

```powershell
npm start
```

Frontend runs on `http://localhost:3000`.

## Environment Variables

### Backend (`backend/.env`)

- `MONGO_URI` (required): Mongo connection string. If missing/invalid, `/api/auth/*` routes will return a DB error.
- `JWT_SECRET_KEY` (recommended): Used to sign JWT tokens returned by login.
- `SECRET_KEY` (recommended): Flask secret key.
- `CLOUD_NAME`, `CLOUD_API_KEY`, `CLOUD_API_SECRET` (optional): Enables image upload to Cloudinary for `/api/generate-caption`.

### Frontend (`frontend/.env`)

- `REACT_APP_API_BASE_URL` (optional): Base URL for the Flask API. Defaults to `http://localhost:5000`.

## API Endpoints

Base URL: `http://localhost:5000`

### Auth

- `POST /api/auth/register`
  - Body (JSON): `{ "email": "...", "password": "...", "username": "..." }`
- `POST /api/auth/login`
  - Body (JSON): `{ "email": "...", "password": "..." }`
  - Returns: `{ token, user: { id, email, username } }`

### Captions

- `POST /api/generate-caption`
  - Content-Type: `multipart/form-data`
  - Fields:
    - `image` (file, required)
    - `sentiment` (string, optional: `neutral|happy|sad|aesthetic`)
    - `length` (string/number, optional: commonly `short|medium|long`)
    - `user_id` (string, optional)
  - Returns: `{ caption, image_url, caption_id }`
  - Notes:
    - Caption generation is currently **rule-based** (see `backend/model.py`).
    - `image_url` is only present when Cloudinary upload succeeds.
    - MongoDB save is best-effort; if DB is down, caption still returns but `caption_id` may be `null`.

- `POST /api/captions`
  - Body (JSON): `{ user_id, image_url, caption, sentiment, length }`

- `GET /api/captions/<user_id>`
  - Returns all saved captions for that user.

## Build

Frontend production build:

```powershell
cd frontend
npm run build
```

## Troubleshooting

- **MongoDB connection failed**
  - Verify `MONGO_URI` in `backend/.env`.
  - If using Atlas, ensure your IP is allowed and you’re using the correct `mongodb+srv://...` URI.

- **Cloudinary upload not working**
  - Ensure all `CLOUD_*` variables are set in `backend/.env`.

- **CORS / frontend can’t reach backend**
  - Make sure the backend is running on port `5000`.
  - Confirm `REACT_APP_API_BASE_URL` points to the backend URL.
