import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [items, setItems] = useState([]);
  const [name, setName] = useState('');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState('Checking...');
  
  const API = process.env.REACT_APP_API_URL || 'http://localhost:5001';

  useEffect(() => {
    checkHealth();
    fetchItems();
  }, []);

  const checkHealth = async () => {
    try {
      const res = await fetch(`${API}/api/health`);
      const data = await res.json();
      setStatus(data.db === 'connected' ? '✅ Connected' : '⚠️ Disconnected');
    } catch (error) {
      setStatus('❌ Server Offline');
    }
  };

  const fetchItems = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API}/api/items`);
      const data = await res.json();
      setItems(data);
    } catch (error) {
      console.error('Error fetching items:', error);
    }
    setLoading(false);
  };

  const addItem = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;

    try {
      const res = await fetch(`${API}/api/items`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
      });

      if (res.ok) {
        setName('');
        fetchItems();
      }
    } catch (error) {
      console.error('Error adding item:', error);
    }
  };

  const deleteItem = async (id) => {
    try {
      await fetch(`${API}/api/items/${id}`, {
        method: 'DELETE'
      });
      fetchItems();
    } catch (error) {
      console.error('Error deleting item:', error);
    }
  };

  return (
    <div className="App">
      <div className="container">
        <h1>🐳 Docker Compose Demo</h1>
        <div className="status">{status}</div>

        <form onSubmit={addItem} className="add-form">
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Add new item..."
            className="input"
          />
          <button type="submit" className="btn-add">Add Item</button>
        </form>

        <div className="items-section">
          <h2>Items ({items.length})</h2>
          {loading ? (
            <p className="loading">Loading...</p>
          ) : items.length === 0 ? (
            <p className="empty">No items yet. Add one above!</p>
          ) : (
            <ul className="items-list">
              {items.map((item) => (
                <li key={item._id} className="item">
                  <span className="item-name">{item.name}</span>
                  <button
                    onClick={() => deleteItem(item._id)}
                    className="btn-delete"
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;