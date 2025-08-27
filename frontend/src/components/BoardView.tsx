import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import apiClient from '../services/api';

// --- Define TypeScript interfaces for our data shapes ---
interface Card {
  id: number;
  title: string;
  description: string | null;
}

interface List {
  id: number;
  title: string;
  cards: Card[];
}

interface Board {
  id: number;
  title: string;
  lists: List[];
}

const BoardView = () => {
  const [board, setBoard] = useState<Board | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const { boardId } = useParams<{ boardId: string }>();

  useEffect(() => {
    const fetchBoardData = async () => {
      if (!boardId) return;

      try {
        setLoading(true);
        setError('');
        const response = await apiClient.get<Board>(`/api/boards/${boardId}`);
        setBoard(response.data);
      } catch (err) {
        setError('Failed to fetch board data. You may not have access or the board may not exist.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchBoardData();
  }, [boardId]);

  if (loading) return <div>Loading board...</div>;
  if (error) return <div style={{ color: 'red', padding: '20px' }}>{error}</div>;
  if (!board) return <div>Board not found.</div>;

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>{board.title}</h1>
      <main style={{ display: 'flex', gap: '16px', overflowX: 'auto', paddingBottom: '10px' }}>
        {board.lists.map((list) => (
          <div key={list.id} style={{ flex: '0 0 272px', background: '#ebecf0', padding: '8px', borderRadius: '4px' }}>
            <h2 style={{ fontSize: '1rem', margin: '0 0 10px 0' }}>{list.title}</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
              {list.cards.map((card) => (
                <div key={card.id} style={{ background: 'white', padding: '12px', borderRadius: '4px', boxShadow: '0 1px 1px rgba(0,0,0,0.1)' }}>
                  {card.title}
                </div>
              ))}
            </div>
          </div>
        ))}
      </main>
    </div>
  );
};

export default BoardView;