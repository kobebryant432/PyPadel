// OptionsDisplay.js
import React from 'react';

const OPTIONS = {
  0: {"e": "First Serve", "t": "Second Serve"},
  1: {"1": "Player 1", "2": "Player 2", "3": "Player 3", "4": "Player 4"},
  2: {"f": "Forced Winner", "u": "Unforced Error", "w": "Winner",},
  3: {"fh": "Forehand", "bh": "Backhand", "hi": "High", "hd": "High defense"},
  4: {
    "v": "Volley",
    "o": "Other",
    "n": "Normal",
    "g": "Glass",
    "r": "return",
    "l": "lob",
    "s": "smash",
    "V": "vibora",
    "k": "kick",
    "b": "bandeja",
    "j": "bajada",
    "f": "fake",
    "z": "double fault",
  },
  5: {
    "c": "cross",
    "p": "parallel",
    "n": "net",
    "l": "long",
    "m": "middle",
    "d": "dropshot",
    "k": "dunk",
    "g": "globo",
    "f": "fence",
  },
};
function OptionsDisplay({ activeIndex, activeChar, onOptionClick }) {
    const options = OPTIONS[activeIndex];
    const numColumns = Math.min(4, Object.keys(options).length); // Determine the number of columns
  
    return (
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        backgroundColor: '#f2f2f2', 
        padding: '20px', 
        borderRadius: '10px',
        maxHeight: '50vh',
        overflowY: 'auto'
      }}>
        <h2 style={{ marginBottom: '20px' }}>Options</h2>
        <div style={{
          display: 'grid',
          gridTemplateColumns: `repeat(${numColumns}, 1fr)`, // Use the number of columns
          gap: '20px' // Increase the gap between options
        }}>
          {Object.entries(options).map(([key, value]) => (
            <div 
              key={key} 
              style={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center', 
                padding: '10px', 
                backgroundColor: key === activeChar ? '#bbb' : '#fff', 
                borderRadius: '5px', 
                cursor: 'pointer', 
                transition: 'background-color 0.3s'
              }}
              onClick={() => onOptionClick(key)}
              onMouseEnter={(e) => e.target.style.backgroundColor = '#ddd'}
              onMouseLeave={(e) => e.target.style.backgroundColor = key === activeChar ? '#bbb' : '#fff'}
              onMouseDown={(e) => e.target.style.backgroundColor = '#bbb'}
              onMouseUp={(e) => e.target.style.backgroundColor = '#ddd'}
            >
              <span style={{ fontWeight: 'bold' }}>{key}</span> {/* Make the key bold */}
              <span style={{ fontStyle: 'italic' }}>({value})</span> {/* Make the value italic and add brackets */}
            </div>
          ))}
        </div>
      </div>
    );
  }
  
  export default OptionsDisplay;