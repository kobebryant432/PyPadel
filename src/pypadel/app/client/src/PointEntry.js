import React, { useState, useEffect } from 'react';
import Tooltip from './Tooltip';
import OptionsDisplay from './OptionsDisplay';
import NaturalLanguageDisplay from './NaturalLanguageDisplay';

const POINT_STRUCTURE = {
"serve": [0, 1],
"player": [1, 2],
"category": [2, 3],
"side": [3, 4],
"shot": [4, 5],
"direction": [5, 6],
};

const FORCED_WINNER_POINT_STRUCTURE = {
...POINT_STRUCTURE,
"player2": [6, 7],
"side2": [7, 8],
"shot2": [8, 9],
};

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
6: {"1": "Player 1", "2": "Player 2", "3": "Player 3", "4": "Player 4"}, // Options for player2
7: {"fh": "Forehand", "bh": "Backhand", "hi": "High", "hd": "High defense"}, // Options for side2
8: {
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
}, // Options for shot_type_2
};

function PointEntry() {
    const [pointData, setPointData] = useState(Array(6).fill(''));
    const [activeIndex, setActiveIndex] = useState(0);
    const [isCorrect, setIsCorrect] = useState(Array(6).fill(null)); // New state
    const [isForcedWinner, setIsForcedWinner] = useState(false); // New state
    const [player2Options, setPlayer2Options] = useState(OPTIONS[6]); // New state
    const inputRef = React.createRef();
  
    useEffect(() => {
      if (['1', '2'].includes(pointData[1])) {
        setPlayer2Options({"3": "Player 3", "4": "Player 4"});
      } else if (['3', '4'].includes(pointData[1])) {
        setPlayer2Options({"1": "Player 1", "2": "Player 2"});
      } else {
        setPlayer2Options(OPTIONS[6]);
      }
    }, [pointData[1]]);

const getTooltip = (index) => {
    const structure = isForcedWinner ? FORCED_WINNER_POINT_STRUCTURE : POINT_STRUCTURE;
    for (const [key, value] of Object.entries(structure)) {
    if (index >= value[0] && index < value[1]) {
        return key.replace(/_/g, ' '); // Replace underscores with spaces for better readability
    }
    }
    return '';
};

const handleKeyDown = (event) => {
    const newPointData = [...pointData];
    const newIsCorrect = [...isCorrect]; // Copy the isCorrect state
  
    if (event.key.length === 1 && !['ArrowRight', 'ArrowLeft'].includes(event.key)) {
        let nextIndex = activeIndex;
    
        if ((activeIndex === 3 || activeIndex === 7) && newPointData[activeIndex].length < 2) {
          newPointData[activeIndex] = newPointData[activeIndex] === '' ? event.key : newPointData[activeIndex] + event.key;
          if (newPointData[activeIndex].length === 2) nextIndex++;
        } else {
          newPointData[activeIndex] = event.key;
          nextIndex++;
        }
    
        // Use the full value of the box for validation
        newIsCorrect[activeIndex] = Object.keys(activeIndex === 6 ? player2Options : OPTIONS[activeIndex]).includes(newPointData[activeIndex]);
    
        setPointData(newPointData);
        setIsCorrect(newIsCorrect);
        setActiveIndex(Math.min(nextIndex, pointData.length - 1));
      } else if (event.key === 'Backspace') {
        if ((activeIndex === 3 || activeIndex === 7) && newPointData[activeIndex].length === 2) {
          newPointData[activeIndex] = newPointData[activeIndex][0];
        } else {
          newPointData[activeIndex] = '';
          setActiveIndex(Math.max(activeIndex - 1, 0));
        }
    
        newIsCorrect[activeIndex] = null; // Reset the isCorrect state for the active box
    
        setPointData(newPointData);
        setIsCorrect(newIsCorrect);
      } else if (event.key === 'ArrowRight') {
        setActiveIndex(Math.min(activeIndex + 1, pointData.length - 1));
      } else if (event.key === 'ArrowLeft') {
        setActiveIndex(Math.max(activeIndex - 1, 0));
      }
  
    // Check if the category is 'f' and set isForcedWinner accordingly
    if (activeIndex === 2 && event.key.length === 1) {
        if (event.key === 'f') {
        setIsForcedWinner(true);
        setPointData([...pointData.slice(0, 2), 'f', ...pointData.slice(3), '', '', '']); // Extend pointData to have 9 elements
        setIsCorrect([...isCorrect.slice(0, 2), true, ...isCorrect.slice(3), null, null, null]); // Extend isCorrect to have 9 elements
        } else {
        setIsForcedWinner(false);
        setPointData([...pointData.slice(0, 2), event.key, ...pointData.slice(3, 6)]); // Update the category with the new character and reduce pointData to have 6 elements
        setIsCorrect([...isCorrect.slice(0, 2), Object.keys(OPTIONS[2]).includes(event.key), ...isCorrect.slice(3, 6)]); // Set the category as checked and reduce isCorrect to have 6 elements
        }
    }
  };

  const handleOptionClick = (key) => {
    const newPointData = [...pointData];
    newPointData[activeIndex] = key;
  
    // Validate the input
    const newIsCorrect = [...isCorrect];
    newIsCorrect[activeIndex] = Object.keys(activeIndex === 6 ? player2Options : OPTIONS[activeIndex]).includes(key);
  
    // Check if the category is 'f' and set isForcedWinner accordingly
    if (activeIndex === 2 && key === 'f') {
      setIsForcedWinner(true);
      newPointData.splice(3, 0, '', '', ''); // Extend pointData to have 9 elements
      newIsCorrect.splice(3, 0, null, null, null); // Extend isCorrect to have 9 elements
    } else if (activeIndex === 2) {
      setIsForcedWinner(false);
      newPointData.splice(3, 3); // Reduce pointData to have 6 elements
      newIsCorrect.splice(3, 3); // Reduce isCorrect to have 6 elements
    }
  
    setActiveIndex(Math.min(activeIndex + 1, newPointData.length - 1)); // Move to the next box
    setPointData(newPointData);
    setIsCorrect(newIsCorrect);
  };

return (
    <div onKeyDown={handleKeyDown} tabIndex="0" ref={inputRef} style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: '20px' }}>
        {pointData.map((char, index) => (
          <Tooltip text={getTooltip(index)} inputWidth={50} isActive={index === activeIndex} color={isCorrect[index] === true ? '#3BD16F' : isCorrect[index] === false ? '#cf363d' : 'black'}>
            <input
              key={index}
              type="text"
              value={char}
              readOnly
              onClick={() => setActiveIndex(index)} // Set activeIndex to the index of the clicked box
              style={{ 
                width: '50px', 
                height: '50px', 
                fontSize: '24px', 
                textAlign: 'center', 
                marginRight: '60px',
                border: index === activeIndex ? '1px solid #FFC000' : 'none',
                backgroundColor: isCorrect[index] === true ? '#3BD16F' : isCorrect[index] === false ? '#cf363d' : undefined // Set the background color based on isCorrect
              }}
            />
          </Tooltip>
        ))}
      </div>
      <OptionsDisplay activeIndex={activeIndex} activeChar={pointData[activeIndex]} onOptionClick={handleOptionClick} options={activeIndex === 6 ? player2Options : OPTIONS[activeIndex]} />
      <NaturalLanguageDisplay pointData={pointData} OPTIONS={OPTIONS} />
    </div>
  );
}

export default PointEntry;