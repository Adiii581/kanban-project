import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import BoardView from './components/BoardView';
import useAuthStore from './state/authStore';

function App() {
  const token = useAuthStore((state) => state.token);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        {/* Protected Route for the board view */}
        <Route 
          path="/board/:boardId" 
          element={token ? <BoardView /> : <Navigate to="/login" replace />} 
        />

        {/* Redirect root path */}
        <Route 
          path="/" 
          element={token ? <Navigate to="/board/1" replace /> : <Navigate to="/login" replace />}
        />
      </Routes>
    </Router>
  );
}

export default App;