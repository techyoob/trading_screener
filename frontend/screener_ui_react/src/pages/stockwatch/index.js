


import React, { useState, useEffect, Component } from 'react';
import './stockwatch.css';
import '../pages.css';


import { 
    FaSearch,
    FaCaretDown,
    FaCaretUp,
    FaAngleLeft,
    FaAngleRight
} from 'react-icons/fa';


import Spinner from "react-svg-spinner";

import MiniLineChart from '../../components/miniatureLineChart';
import CandlestickChart from '../../components/candlestickChart';

import { 
    TypeOneAlert,
    BollingerBandSqueezeAlert
} from '../../components/alerts'









const StockWatchPage = (props) => {
  
    return (
      <div className="main-page-div">
        <div className="main-page-section-I-div">
            <div className="main-page-header-div"> 
                <StockOverview {...props}/>
            </div>
        </div>
        <div className="main-page-section-II-div">
            <div className="stock-chart-details-div">
                <StockChart {...props}/>
            </div>
            <div className="stock-alerts-div">
                <StockAlerts {...props}/>
            </div>
        </div>
      </div>
    );
}




export default StockWatchPage;




const StockOverview = (props) => {


    const [isLoading, setIsLoading] = useState(false)
    const [data, setData] = useState({})


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
        `${process.env.REACT_APP_URL}ticker_info?ticker=${ticker!=undefined? ticker : ""}`,
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
                setData({})
                setIsLoading(false)
              }
        });
    }



    return(
        <div className="stock-overview-div">
            <div className="stock-overview-title-div">
                Overview
            </div>
            {isLoading?
            <div className="loading-spinner"> <Spinner  size="20px" color="white" /></div> 
            : <div className="stock-overview-details-div">
                <div className="stock-overview-element-div">
                    <span className="overview-ticker"> {data['ticker']} </span>
                    <span className="overview-name"> {data['name']} </span>
                </div>
                <div className="stock-overview-element-div">
                    <span className="overview-ticker-price">
                        <span style={{fontSize:"25px", fontWeight:"bold"}}>{`$${data['price']}`} </span>
                        <span >{`$${data['change']} (${data['change percentage']}%)`} </span>
                    </span>
                </div>
                <div className="stock-overview-element-div">                    
                    <span className="overview-item-key">Open</span>
                    <span className="overview-item-value">{`$${data['open']}`}</span>
                </div>
                <div className="stock-overview-element-div">
                    <span className="overview-item-key">Volume</span>
                    <span className="overview-item-value">{`$${shortBigNumber( data['volume'])}`}</span>
                </div>
                <div className="stock-overview-element-div">
                    <span className="overview-item-key">Market Cap</span>
                    <span className="overview-item-value">{`$${shortBigNumber( data['market cap'])}`}</span>
                </div>
                <div className="stock-overview-element-div">
                    <span className="overview-item-key">Day Range</span>
                    <span className="overview-item-value">{`${data['day range']}`}</span>
                </div>
            </div>}
        </div>);
}





const StockChart = (props) => {


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
    <>
        <div className="stock-chart-header-div" >
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
        <div className="stock-chart-body-div" >
            <CandlestickChart data={candlesData}/> 
        </div>
        <div className="stock-chart-overview-div">

        </div>
    </>);
}



const StockAlerts = (props) => {

    const [alerts, setAlerts] = useState([])
    const [isLoading, setIsLoading] = useState(false)

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
        `${process.env.REACT_APP_URL}stock?ticker=${ticker}&query=alerts&filter=all`,
        {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
        })
        .then(res => res.json())
        .then(response => {

            if(isMounted){
                if(response.status===200){
                   
                    setAlerts(response.results)
                    setIsLoading(false)
                } else {
                    throw "error"
                }
            }

        })
        .catch(error => {
            console.log("am here at error ", error)
            if(isMounted){
                setAlerts([])
                setIsLoading(false)
              }
        });
    }




    return (
        <>
            <div className="stock-alerts-title-div">
                Alerts
            </div>
            <div className="stock-alerts-body-div">
            {alerts.map((item, i)=>{
                return (
                    <div className="stock-alert-item-div" key={i}>
                        {alertLoader(item)[item.name]}
                    </div>) 
                
            })}
            </div>
        </>
    );
}



const alertLoader = (props) => ({
    'new high':<TypeOneAlert {...props}/>,
    'new low':<TypeOneAlert {...props}/>,
    'bb squeeze':<BollingerBandSqueezeAlert {...props}/>
})




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
  