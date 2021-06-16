


import React, { useState, useEffect, Component } from 'react';
import './bigbang.css';
import { 
    FaSearch,
    FaCaretDown,
    FaCaretUp,
    FaAngleLeft,
    FaAngleRight,
    FaSyncAlt
} from 'react-icons/fa';


import Spinner from "react-svg-spinner";

import MiniLineChart from '../../components/miniatureLineChart'
import CandlestickChart from '../../components/candlestickChart'




const BigBangPage = (props) => {




    const [lastUpdated, setLastUpdated] = useState("")
    const [tableData, setTableData] = useState([]);    
    const [tableHeader, setTablHeader] = useState(["Ticker","current", "forecasting"]);
    const [isLoading, setIsLoading] = useState(false)



    useEffect(() => {

        let isMounted = true;

        requestData(isMounted)
        return function cleanup() {
            isMounted=false;
        }
    }, []);
  
  
  
    const requestData = (isMounted) => {

        

      setIsLoading(true)
      fetch(
        `${process.env.REACT_APP_URL}screener?strat=big_bang&filter=top50`,
        {
          method: "GET",
          headers: { 'Content-Type': 'application/json' }
        }
      )
      .then(res => res.json())
      .then(response => {
        
        if(isMounted){
          if(response.status===200){
              
            setTableData(response.results)
            setLastUpdated(response.last_update)
            setIsLoading(false)
          } else {
              throw "error"
          }
        }
  
  
        
      })
      .catch(error => {
          
          console.log("am here at SocialTrend error ", error)
          if(isMounted){
            setTableData([])
            setTablHeader([])
            setIsLoading(false)
          }
          
        });
    }

    return (
      <div className="big-bang-page-div">
            <div className="section-I-div">
                <div className="main-info-div"> 
                    <HeaderClock {...props}/>
                </div>
            </div>
            <div className="section-II-div">
                <div className="big-bang-list-div">
                    <div className="big-bang-list-title-div">
                        BIG BANG SCREENER
                    </div>
                    {isLoading 
                        ? <div className="spinner-container">
                            <p>Please Wait ...</p>
                            <Spinner size="20px" color="white" />
                        </div>
                        :   <div className="big-bang-list-body-div">
                        <table id='tickers-list'>
                            <thead>
                                <tr>
                                    {tableHeader.map((item, i)=>{
                                        return <th key={i}>{item}</th>
                                    })}
                                </tr>                            
                            </thead>
                            <tbody>
                                {tableData.map((item, j) => {

                                    return (
                                        <tr key={j}>
                                            <td>{item.ticker}</td>
                                            <td>
                                                <CurrentQuoteUI current={item.current}/>
                                            </td>
                                            <td>
                                                <ForecastingUI forecasting={item.forecasting} 
                                                        movement={item.movement}/>
                                            </td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>
                    </div>
                    }
                    <div className="big-bang-list-footer-div">
                        {isLoading ? <Spinner size="20px" color="white"/> : `Last Updated: ${lastUpdated}`}
                        <FaSyncAlt 
                            onClick={requestData}
                            className="refresh-icon-button"/>
                    </div>
                </div>
            </div> 
      </div>
    );
  }




export default BigBangPage;




const CurrentQuoteUI = (props) => {

    const [data, setData] = useState({})
    useEffect(()=>{        
        setData(props.current ? props.current : {})
    }, [props.current])


    return (
        <div className="current-quote-container">
            <div className="current-item-box-I">
                <span style={data['percentage'] > 0 ? {color:"green"} : {color:"red"}}>
                    {`$${data['price']? data['price'] : 0}`}
                </span>
                <span style={data['percentage'] > 0 ? {color:"green"} : {color:"red"}}>
                    {`${data['change']? data['change'] : 0}`}
                </span>
                <span style={data['percentage'] > 0 ? {color:"green"} : {color:"red"}} >
                    {`${data['percentage']? data['percentage'] : 0}%`}
                </span>
            </div>
            <div className="current-item-box-II">
                <div className="current-item">
                    <span>Volume</span>
                    <span>{`$${shortBigNumber(data['volume'])}`}</span>
                </div>
                <div className="current-item">
                    <span>Day High</span>
                    <span>{`$${data['day high']? data['day high'] : 0}`}</span>
                </div>
                <div className="current-item">
                    <span>Day Low</span>
                    <span>{`$${data['percentage']? data['percentage'] : 0}`}</span>
                    
                </div>
            </div>        
        </div>
    )
}






const ForecastingUI = (props) => {

    const [data, setData] = useState([])



    useEffect(()=>{        
        setData(Array.isArray(props.forecasting) ? props.forecasting : [])
    }, [props.forecasting])


    return (
        <div className="forecasting-container">
            {data.map((item, i)=>{

                const key = Object.keys(item)
                const value = item[Object.keys(item)].toFixed(2)
                const movement = props?.movement

                return (
                    <div className="forecasting-item-box"
                        key={i}>
                            <span className="forecasting-item-title">{key}</span>
                            <div className="forecasting-item-value"> <span>{movement}</span> <span>{`$${value}`}</span></div>
                    </div>)
            })}
        </div>
    )
}




const HeaderClock = (props) => {



    const [clockData, setClockData ] = useState({
      day:new Date().toLocaleDateString("en-US", {weekday: 'short', month:"short", day:"2-digit"}),
      time:new Date().toLocaleTimeString("en-US", {hour:"2-digit", minute:"2-digit"})
    })
  
    useEffect(() => {
  
        const onSetClock = () => {
            
          const day  = new Date().toLocaleDateString("en-US", {weekday: 'short', month:"short", day:"2-digit"});
          const time = new Date().toLocaleTimeString("en-US", {hour:"2-digit", minute:"2-digit"});
          setClockData({day, time})
        }
    
      var dateUpdateTimer = setInterval(()=>{
          onSetClock();
        }, 60000 )
      
  
      return function cleanup() {
          clearInterval(dateUpdateTimer)
      }
    }, []);
  
  
  
    return (
      <div className="header-clock-div">
        <span className="date-div"> {clockData.day} </span>
        <span className="time-div"> {clockData.time} </span>
      </div>
    )
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
