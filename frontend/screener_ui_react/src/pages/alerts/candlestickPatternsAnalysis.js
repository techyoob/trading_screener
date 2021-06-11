


import React, { useState, useEffect, useRef } from 'react';
import './candlestickPatternsAnalysis.css';


import { 
    FaSearch,
    FaCaretDown,
    FaCaretUp,
    FaAngleLeft,
    FaAngleRight
} from 'react-icons/fa';






const CandlestickPatternsAnalysis = (props) => {

    const candlestickItemRef = useRef(null)

    return (
      <div 
        className="candlestick-item-div"
        ref={candlestickItemRef}>
            <div className="patterns-bulls-div">
                <span>{`Bulls`}</span>
                <span>{`${props.item.strategies[props.strategy].bulls}`}</span>
            </div>
            <div className="patterns-bears-div">
                <span>{`Bears`}</span>
                <span>{`${props.item.strategies[props.strategy].bears}`}</span>
            </div>

      </div>
      
    );
  }
    
export default CandlestickPatternsAnalysis;