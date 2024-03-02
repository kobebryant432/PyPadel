// Tooltip.js
import React from 'react';

function Tooltip({ children, text, inputWidth, color, isActive }) { // Receive isActive prop
  return (
    <div style={{ position: 'relative', display: 'inline-block' }}>
      {children}
      <div style={{
        visibility: 'visible', // Always visible
        backgroundColor: isActive ? '#FFC000' : color || 'black', // Use #FFC000 when active
        color: '#fff',
        textAlign: 'center',
        borderRadius: '6px',
        padding: '5px 10px',
        position: 'absolute',
        zIndex: 1,
        bottom: '150%',
        left: `calc(50% - ${inputWidth / 2}px)`,
        transform: 'translateX(-50%)',
      }}>
        {text}
      </div>
    </div>
  );
}

export default Tooltip;