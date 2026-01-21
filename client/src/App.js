import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import UserListView from './pages/UserListView';
import UserDetailView from './pages/UserDetailView';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UserListView />} />
        <Route path="/users/:id" element={<UserDetailView />} />
      </Routes>
    </Router>
  );
}

export default App;
