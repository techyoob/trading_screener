
import { useState, useEffect } from 'react';
import './strategy_ranker.css';


// function StrategyRanker() {

//     const [ strategies, setStrategie ] = useState([]);
//     const [ selectedStrategy, setSelectedStrategy] = useState("strategy I")


//     const onSelectStrategy = (strategy) => {
        
//         setSelectedStrategy(strategy)
//     }

//     useEffect(() => {
//         fetch("http://localhost:5000/strategies")
//         .then(response => response.json())
//         .then(data => {
//             setStrategie(data)
//         });
        

//     }, [])

//   return (
//     <div className="strategy-ranking-item-div">
//         <div className="strategy-header-div">
//             {selectedStrategy}
//         </div>
//         <div className="strategy-body-div">
//             <div className="strategy-selection-div">
//                 {strategies.map((strategy, index)=>{
//                     return(
//                         <div 
//                             className="ticker-rank-element-div"
//                             style={{backgroundColor: selectedStrategy ===  strategy ? "yellow" : "green"}}
//                             key={index}
//                             onClick={()=>onSelectStrategy(strategy)}>
//                                 {strategy}
//                         </div>)
//                 })}
//             </div>
//             <div className="strategy-ranking-list-div">
            
//             </div>
//         </div>
//     </div>
//   );
// }

export default StrategyRanker;

