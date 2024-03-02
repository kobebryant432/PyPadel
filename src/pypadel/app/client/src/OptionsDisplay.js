// OptionsDisplay.js
import React from 'react';

function OptionsDisplay({ activeIndex, activeChar, onOptionClick, options }) {
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