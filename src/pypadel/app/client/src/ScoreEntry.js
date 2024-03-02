import React from 'react';

function ScoreEntry() {
  return (
    <div>
      <h2>Score Entry</h2>
      <div>
        <h4>Player 1 and Player 2</h4>
        <input type="number" placeholder="Set Score" />
        <input type="number" placeholder="Point Score" />
      </div>
      <div>
        <h4>Player 3 and Player 4</h4>
        <input type="number" placeholder="Set Score" />
        <input type="number" placeholder="Point Score" />
      </div>
    </div>
  );
}

export default ScoreEntry;