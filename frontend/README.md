# Travel Planner — Frontend

A React + TypeScript frontend for the Travel Planner AI app. Built with Vite and React Router.

---

## Prerequisites

- **Node.js** v18 or higher — [Download](https://nodejs.org/)
- **npm** v9 or higher (comes with Node.js)
- Backend server running on `http://127.0.0.1:8000` (see `backend/src/README.md`)

---

## Project Structure

```
frontend/travel-planner/
├── src/
│   ├── home/          # Home page — travel itinerary planner
│   │   ├── Home.tsx
│   │   └── Home.css
│   ├── ask-me/        # Ask Me page — RAG-powered Q&A
│   │   ├── AskMe.tsx
│   │   └── AskMe.css
│   ├── App.tsx        # Route definitions
│   ├── main.tsx       # App entry point
│   ├── index.css      # Global styles & CSS variables
│   └── App.css
├── package.json
├── vite.config.ts
└── tsconfig.json
```

---

## Steps to Run

### 1. Navigate to the frontend folder

```bash
cd frontend/travel-planner
```

### 2. Install dependencies

```bash
npm install
```

### 3. Start the development server

```bash
npm run dev
```

The app will be available at `http://localhost:5173` by default.

---

## Available Scripts

| Script | Description |
|---|---|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Type-check and build for production |
| `npm run preview` | Preview the production build locally |
| `npm run lint` | Run ESLint |

---

## Pages & API Endpoints

### Home (`/`)
- Enter a travel query to generate a 4-day itinerary
- Calls `POST http://127.0.0.1:8000/plan-trip`
- Navigates to the Ask Me page

### Ask Me (`/ask-me`)
- Ask questions about the loaded document (RAG pipeline)
- Calls `POST http://127.0.0.1:8000/api/v1/ask-question`

---

## Dependencies

| Package | Version | Purpose |
|---|---|---|
| react | ^19.2.4 | UI library |
| react-dom | ^19.2.4 | DOM rendering |
| react-router-dom | ^7.18.1 | Client-side routing |
| vite | ^8.0.1 | Build tool & dev server |
| typescript | ~5.9.3 | Type checking |
