# Candidate Database Frontend

React frontend application for browsing and searching candidate profiles.

## Features

- **Candidate List View**: Browse all candidates with search and filter options
- **Candidate Detail View**: View full profile information for individual candidates
- **Semantic Search**: Search for candidates by profession using semantic similarity
- **Exact Match Toggle**: Option to use exact profession matching instead of semantic search
- **Date Range Filtering**: Filter candidates by creation date range
- **Combined Filters**: Use semantic search and date filters together
- **Similarity Visualization**: Visual indicator showing how similar search results are

## Getting Started

### Prerequisites

- Node.js and npm installed
- Backend API running on `http://localhost:8000`

### Installation

1. Navigate to the client directory:
   ```bash
   cd client
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Development Server

```bash
npm start
```

The app will open at [http://localhost:3000](http://localhost:3000) in your browser.

The page will reload automatically when you make changes.

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` folder.

## Project Structure

```
client/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable React components
│   │   ├── UserCard.js           # Candidate card component
│   │   ├── SearchBar.js          # Profession search input
│   │   ├── DateRangeFilter.js    # Date filter inputs
│   │   └── SimilarityIndicator.js # Similarity visualization
│   ├── pages/          # Page components
│   │   ├── UserListView.js       # Main candidate list page
│   │   └── UserDetailView.js     # Individual candidate detail page
│   ├── services/       # API integration
│   │   └── api.js      # Axios-based API client
│   ├── App.js          # Main app component with routing
│   └── index.js        # Entry point
├── package.json
└── README.md
```

## Usage

### Searching Candidates

1. **Semantic Search** (default):
   - Enter a profession in the search bar (e.g., "programmer")
   - Results will include semantically similar professions (Software Engineer, Software Developer, etc.)
   - Similarity scores are displayed as progress bars

2. **Exact Match**:
   - Check the "Exact match" checkbox
   - Enter the exact profession name
   - Results will only include exact matches (case-insensitive)

### Filtering by Date

- Set a start date to show candidates created on/after that date
- Set an end date to show candidates created on/before that date
- Date filters work with both semantic and exact match searches

### Viewing Candidate Details

- Click on any candidate card to view their full profile
- Use the back button to return to the list view

## Configuration

The API base URL can be configured via environment variable:

```bash
REACT_APP_API_URL=http://localhost:8000 npm start
```

By default, it uses `http://localhost:8000`.

## Technology Stack

- **React**: UI library (ES6, no TypeScript)
- **React Router Dom**: Client-side routing
- **Axios**: HTTP client for API calls
- **Tailwind CSS**: Utility-first CSS framework
- **React Context + useState**: Lightweight state management

## Styling

The application uses a light, modern aesthetic with:
- Primary colors: Light blue tones
- Background: White and light gray
- Typography: Light, airy font weights
- Components: Rounded corners, soft shadows, subtle borders

## Available Scripts

- `npm start`: Start development server
- `npm test`: Run tests in watch mode
- `npm run build`: Build for production
- `npm run eject`: Eject from Create React App (one-way operation)

## Learn More

- [React Documentation](https://reactjs.org/)
- [React Router Documentation](https://reactrouter.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [Create React App Documentation](https://facebook.github.io/create-react-app/docs/getting-started)
