import React, { useState, useEffect } from 'react';
import Tooltip from './Tooltip';
import OptionsDisplay from './OptionsDisplay';

const POINT_STRUCTURE = {
  "serve_type": [0, 1],
  "player": [1, 2],
  "category": [2, 3],
  "side": [3, 4],
  "shot_type": [4, 5],
  "direction": [5, 6],
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
  };

  function PointEntry() {
    const [pointData, setPointData] = useState(Array(6).fill(''));
    const [activeIndex, setActiveIndex] = useState(0);
    const [isCorrect, setIsCorrect] = useState(Array(6).fill(null)); // New state
    const inputRef = React.createRef();
  
    useEffect(() => {
      inputRef.current.focus();
    }, []);

    const getTooltip = (index) => {
        for (const [key, value] of Object.entries(POINT_STRUCTURE)) {
            if (index >= value[0] && index < value[1]) {
                return key.replace(/_/g, ' '); // Replace underscores with spaces for better readability
            }
        }
        return '';
    };
    
  
    const handleKeyDown = (event) => {
      const newPointData = [...pointData];
      const newIsCorrect = [...isCorrect]; // Copy the isCorrect state
      if (event.key.length === 1) {
        let nextIndex = activeIndex;
    
        if (activeIndex === 3 && newPointData[3].length < 2) {
            newPointData[3] = newPointData[3] === '' ? event.key : newPointData[3] + event.key;
            if (newPointData[3].length === 2) nextIndex++;
        } else {
            newPointData[activeIndex] = event.key;
            nextIndex++;
        }
    
        // Use the full value of the box for validation
        newIsCorrect[activeIndex] = Object.keys(OPTIONS[activeIndex]).includes(newPointData[activeIndex]);
    
        setPointData(newPointData);
        setIsCorrect(newIsCorrect);
        setActiveIndex(Math.min(nextIndex, pointData.length - 1));
      } else if (event.key === 'Backspace') {
        if (activeIndex === 3 && newPointData[3].length === 2) {
          newPointData[3] = newPointData[3][0];
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
    };
  
    const handleOptionClick = (key) => {
      const newPointData = [...pointData];
      newPointData[activeIndex] = key;
      setActiveIndex(Math.min(activeIndex + 1, pointData.length - 1)); // Move to the next box
      setPointData(newPointData);
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
          <OptionsDisplay activeIndex={activeIndex} activeChar={pointData[activeIndex]} onOptionClick={handleOptionClick} />
        </div>
      );
    }
    
    export default PointEntry;