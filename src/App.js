// App.js
import React, { useState } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [answer, setAnswer] = useState('');
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  const handleTextChange = (e) => {
    setText(e.target.value);
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleButtonClick = () => {
    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('questions', text);

    fetch('http://192.168.56.1:5000/ask_about_spreadsheet', {
      method: 'POST',
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        setAnswer(data.response);
        setHistory([...history, { question: text, answer: data.response }]);
        setLoading(false);
      })
      .catch((error) => {
        console.error('Error:', error);
        setLoading(false);
      });
  };

  return (
    <div className="App">
      {loading && <div className="loading-bar">Loading...</div>}
      <div className="header">
        <img src="logo.png" alt="Logo" className="logo" />
      </div>
      <div className="content">
        <div className="left-content">
          <div className="input-section">
            <input
              type="file"
              onChange={handleFileChange}
              className="file-uploader"
              accept=".xlsx"
            />
            <textarea
              placeholder="Type your Question here..."
              value={text}
              onChange={handleTextChange}
              className="text-editor"
            />
            <button onClick={handleButtonClick} className="styled-button">
              Submit
            </button>
          </div>
          <div className="answer-section">
            <h2>Answer</h2>
            <div className="answer-text">
              {answer}
            </div>
          </div>
        </div>
        <div className="right-content">
          <div className="history-container">
            <h2>History</h2>
            <div className="history-list">
              {history.map((item, index) => (
                <div key={index} className="history-item">
                  <div className="question">{item.question}</div>
                  <div className="answer">{item.answer}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    
    </div>
  );
}

export default App;
