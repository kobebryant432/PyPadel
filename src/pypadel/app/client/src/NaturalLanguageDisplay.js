// NaturalLanguageDisplay.js
import React from 'react';

function NaturalLanguageDisplay({ pointData, OPTIONS }) {
  const descriptions = [];

  // Add each part of the description only if the corresponding data is defined
  if (pointData[0] !== '') descriptions.push(<span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[0][pointData[0]]}</span>, ': ');
  if (pointData[1] !== '') descriptions.push(<span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[1][pointData[1]]}</span>);
  if (pointData[2] !== '') descriptions.push('made a', <span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[2][pointData[2]]}</span>);
  if (pointData[3] !== '') descriptions.push('on a', <span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[3][pointData[3]]}</span>);
  if (pointData[4] !== '') descriptions.push(<span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[4][pointData[4]]}</span>);
  if (pointData[5] !== '') descriptions.push('in the', <span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[5][pointData[5]]}</span>, '. ');

  // If the category is 'f', add the additional descriptions
  if (pointData[2] === 'f') {
    if (pointData[6] !== '') descriptions.push('Attempted response by', <span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[6][pointData[6]]}</span>);
    if (pointData[7] !== '') descriptions.push('with a', <span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[7][pointData[7]]}</span>);
    if (pointData[8] !== '') descriptions.push(<span style={{ fontWeight: 'bold', color: '#FFC000' }}>{OPTIONS[8][pointData[8]]}</span>);
  }

  return (
    <div style={{ fontSize: '24px', marginBottom: '20px' }}>
      {descriptions.reduce((prev, curr, i) => {
        return [...prev, i > 0 && ' ', curr];
      }, [])}
    </div>
  );
}

export default NaturalLanguageDisplay;