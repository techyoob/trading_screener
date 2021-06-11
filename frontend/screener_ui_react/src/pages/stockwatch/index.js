


import React, { useState, useEffect, Component } from 'react';
import './screener.css';
import { 
    FaSearch,
    FaCaretDown,
    FaCaretUp,
    FaAngleLeft,
    FaAngleRight
} from 'react-icons/fa';


import Spinner from "react-svg-spinner";

import MiniLineChart from '../../components/miniatureLineChart'
import CandlestickChart from '../../components/candlestickChart'





const StockWatchPage = (props) => {
  
    return (
      <div className="screener-page-div">
          <div className="screener-header-div">
            <Header {...props}/>
          </div>
          <div className="screener-main-detail-div">
              <div className="ticker-chart-details-div">
                   <Chart {...props} />
              </div>
              <div className="ticker-info-div">
                <Info  {...props} />
              </div>
          </div>
          <div className="screener-strategies-div">
            <Strategies  {...props} /> 
          </div>
      </div>
    );
  }




export default StockWatchPage;


const Header = (props) => {

    
    const [isLoading, setIsLoading] = useState(false)
    const [data, setData] = useState([])


    const onClickNext = (direction) => {

        if(direction==='left'){
            console.log(" bringing left slide ");
        } else if (direction==='right') {
            console.log(" bringing right slide ");
        }

    }

    useEffect(() => {
        
        let isMounted = true;
        
        requestData(isMounted)
        return function cleanup() {
            isMounted = false;
        }
    }, [props.stock.ticker]);

    const requestData = (isMounted) => {
        setIsLoading(true)
        fetch(
        `${process.env.REACT_APP_URL}screener_header`,
        {
            method: "GET",
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(response => {

            if(isMounted){
                if(response.status===200){

                    setData(response.results)
                    setIsLoading(false)
                } else {
                    throw "error"
                }
            }
        
 
        })
        .catch(error => {
            if(isMounted){
                setData([])
                setIsLoading(false)
              }
        });
    }



    return(
        <div className="pre-during-after-market-div">
            <div className="slide-button-div"
                onClick={()=>onClickNext('left')}>
                    <FaAngleLeft/>
            </div>
            <div className="list-div">
                <div className="list-title-div">
                    Most Actives
                </div>
                <div className="list-items-div">
                    {data.map((item, index)=>{

                        return (
                            <div 
                                className="trend-item-div"
                                key={index}>
                                <div className="ticker-current-stats-div">
                                    <div className="stats-1-div"> {item.ticker} </div>
                                    <div className="stats-2-div"> {item.price} </div>
                                    <div className="stats-3-div">{item.changes}{<FaCaretUp style={{color:"#4ce9a0"}}/>}</div>
                                </div>
                                <div className="current-chart-div">
                                    <MiniLineChart data={item.chartData}/>
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
            <div className="slide-button-div"
                onClick={()=>onClickNext('right')}>
                <FaAngleRight />
            </div>
        </div>);
}









const Chart = (props) => {


   const candleSize = ["1D", "5D"]
   const [selectedCandleSize, setSelectedCandleSize] = useState("1D");
   const [candlesData, setCandlesData] = useState([])
   const [isLoading, setIsLoading] = useState(false)

   const onSelectCandleSize = (size) => {
        setSelectedCandleSize(size)
   }

   
   useEffect(() => {
                
        let isMounted = true;
        
        requestData(isMounted,  props.stock.ticker)
        return function cleanup() {
            isMounted = false;
        }
    }, [selectedCandleSize]);


    useEffect(() => {
            
        let isMounted = true;
        
        requestData(isMounted, props.stock.ticker)
        return function cleanup() {
            isMounted = false;
        }
    }, [props.stock.ticker]);

    const requestData = (isMounted, ticker) => {

        setIsLoading(true)
        fetch(
        `${process.env.REACT_APP_URL}ticker_history?ticker=${ticker}&p=${selectedCandleSize}`,
        {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(response => {

            if(isMounted){
                if(response.status===200){

                    setCandlesData(response.results)
                    setIsLoading(false)
                } else {
                    throw "error"
                }
            }

        })
        .catch(error => {
            console.log("am here at error ", error)
            if(isMounted){
                setCandlesData([])
                setIsLoading(false)
              }
        });
    }





    return(
    <div className="chart-div" >
        <div className="chart-header-div" >
            {candleSize.map((item, index)=>{

                return (
                    <button 
                        className={`${selectedCandleSize===item? "selected-" : ""}candle-size-div`}
                        key={index}
                        disabled={selectedCandleSize===item? true : false }
                        onClick={()=> onSelectCandleSize(item)}>
                        {item}
                    </button>)

            })}
        </div>
        <div className="chart-body-div" >
           <CandlestickChart data={candlesData}/>
        </div>)
    </div>);
}


const Info = (props) => {


    const infoTemplate = [
        {
            ticker:"-",
            name:"-"
        },
        {
            "previous close":"-",
            "open":"-"
        },
        {
            volume:"-",
            "market cap":"-"
        },
        {
            "intraday range":"-"
        }
    ]
    const [tickerInfoList, setTickerInfoList] = useState(infoTemplate)
    const [isLoading, setIsLoading] = useState(false)



    useEffect(() => {
        
        
        let isMounted = true;
        
        requestData(props.stock.ticker, isMounted)
        return function cleanup() {
            isMounted=false;
        }
    }, [props.stock.ticker]);
  
  
  
    const requestData = (ticker, isMounted) => {

        setIsLoading(true)

        fetch( `${process.env.REACT_APP_URL}ticker_info?ticker=${ticker!=undefined? ticker : ""}`,
            {
            method: "GET",
            headers: { 'Content-Type': 'application/json' }
            }
        )
        .then(res => res.json())
        .then(response => {
            if (isMounted){
                
                if(response.status===200){
                
                    const info =  [
                        {
                            ticker:response.results['ticker'],
                            name:response.results['name']
                        },
                        {
                            "price":"$"+response.results['price'],
                            "changes":"$"+response.results['changes']
                        },
                        {
                            volume:"$"+shortBigNumber(response.results['volume']),
                            "market cap":"$"+shortBigNumber(response.results['market cap'])
                        },
                        {
                            "intraday range":response.results['intraday range']
                        }
                    ]
    
                    setTickerInfoList(info)
                    setIsLoading(false)
                } else {
                    throw "error"
                }

            }

          

        })
        .catch(error => {
            console.log("am here at error ", error)
            if (isMounted){
                
                setIsLoading(false)
                setTickerInfoList(infoTemplate)

            }
        });
    }
  


    return(
    <div className="ticker-info-details-div">
        {tickerInfoList.map((items, index)=>{

            const itemLabels = Object.keys(items)

            if(index == 0){

                return (
                    <div 
                        className="ticker-info-section-I"
                        key={index}>
                            {isLoading===true
                                    ? <Spinner size="30px" color="white"/>
                                    : <React.Fragment>
                                        <span className="company-symbol">{items.ticker}</span>
                                        <span className="company-name">{items.name}</span>
                                    </React.Fragment>

                            }
                    </div>
                );
            } else {

                return (
                    <div 
                        className="ticker-info-section-II"
                        key={index}>
                    {itemLabels.map((label, i)=>{
                        
                        return (
                            <div 
                                className="item-section-I"
                                key={i}>
                                <span className="item-label">{label}</span>
                                {isLoading===true
                                    ? <Spinner size="20px" color="white"/>
                                    : <span className="item-value">{items[label]}</span>
                                }
                                
                            </div>
                        );
                    })}
                    </div>
                );
            }


        })}
    </div>);
}







const Strategies = (props) => {

    const strategies = ["patternes rating"]


    return(
    <div className="strategies-div">
        <div className="strategies-header-div">
            <span className="strategies-header-title">{`Screening Picks `}</span>
            <span>{`for `}</span>
            <span className="strategies-header-symbol">{props.stock.ticker}</span>
        </div>
        {strategies.map((item, index)=>{
            return (
                <React.Fragment
                    key={index}>
                        <PatternsRating item={item} {...props}/>
                </React.Fragment>)
        })}
    </div>);
}







const PatternsRating = (props) => {


    const [isLoading, setIsLoading] = useState(false)
    const [data, setData] = useState({bears:0,bulls:0})

    useEffect(() => {
        
        let isMounted = true
        requestData(isMounted, props.stock.ticker)
        return function cleanup() {
            isMounted = false;
        }
    }, [props.stock.ticker]);
  
  

    const requestData = (isMounted, ticker) => {

        setIsLoading(true)

        fetch(
        `${process.env.REACT_APP_URL}screener?strat=patterns_analysis&filter=one&ticker=${ticker}`,
        {
            method: "GET",
            headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(response => {


            if (isMounted){
                if(response.status===200){
                    

                    setData({
                        bulls:response.results.bulls,
                        bears:response.results.bears
                    })
                    setIsLoading(false)
                } else {
                    throw "error"
                }
            
            }

            // setbullsData(response.top_bulls)
            // setbearsData(response.top_bears)
            
        })
        .catch(error => {
            console.log("am here at error ", error)
            if(isMounted){
                setData([])
                setIsLoading(false)
            }
            
            
        });
    }


    
    return(
        <div className="patterns-rating-div">
            <span className="patterns-rating-title">{`Patterns`}</span>
            <span className="patterns-rating-title">{`Analysis`}</span>
            <div className="patterns-rating-bulls">
                <span>{`Bulls`}</span>
                {isLoading===true? <Spinner size="15px" color="white"/> : <span>{`${data.bulls.toFixed(2)}%`}</span>}
            </div>
            <div className="patterns-rating-bears">
                <span>{`Bears`}</span>
                {isLoading===true? <Spinner size="15px" color="white"/> : <span>{`${data.bears.toFixed(2)}%`}</span>}
            </div>
        </div>);
}









const  shortBigNumber = (bigNumber) => {
    
    const numberLength = Math.floor(bigNumber).toString().length
    
    return numberLength > 12 
    ? (Math.round( bigNumber/Math.pow(10,10) ) / 100).toFixed(2)+"T" 
    : numberLength > 9 
          ? (Math.round( bigNumber/Math.pow(10,7) ) / 100).toFixed(2)+"B" 
          : numberLength > 6 
              ? (Math.round( bigNumber/Math.pow(10,4) ) / 100).toFixed(2)+"M"
              : numberLength > 3
                  ? (Math.round( bigNumber/Math.pow(10,1) ) / 100).toFixed(2)+"K"
                  : bigNumber
  
  }
  