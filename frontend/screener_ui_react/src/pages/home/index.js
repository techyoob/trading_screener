

import React, { useState, useEffect } from 'react';
import './home.css';
import { FaSearch, FaCaretDown, FaCaretUp, FaSyncAlt } from 'react-icons/fa';





import Spinner from "react-svg-spinner";




const HomePage = (props) => {
  
  
    const homePageItems = ["patterns analysis", "social trends", "most gainers"]

  
    
    return (
      <div className="home-page-div">
        <div className="section-I-div">
          <div className="main-info-div"> 
            <HeaderClock {...props}/>
          </div>
        </div>
        <div className="section-II-div">
          {homePageItems.map((item, index )=>{

              return (
                <div 
                  className="strategy-screened-list-div"
                  key={index}>
                    <div className="strategy-header-div">
                      {item}
                    </div>
                    <div className="strategy-body-div">
                      {homePageItemLoader({name:item, ...props})}
                    </div>
                </div>
              );
            })
          }
        </div>
      </div>
    );
  }
  
export default HomePage;



const homePageItemLoader = (props) => {



  switch(props.name){
    case "patterns analysis":
      return (<PatternsAnalysis {...props}/>)
    case "most gainers":
      return (<MostGainers {...props}/>)
    case "most losers":
      return (<MostLosers {...props}/>)
    case "social trends":
      return (<SocialTrends {...props}/>)
    default:
      return ( 
      <React.Fragment>

      </React.Fragment>)
  }

}



const SocialTrends = (props) => {



  const [lastUpdated, setLastUpdated] = useState("")
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false)


        
  useEffect(() => {
        
        
      let isMounted = true;
      
      requestData(isMounted)

      return function cleanup() {
          isMounted=false;
      }

  }, [props.stock.ticker]);



  const requestData = (isMounted) => {

    setIsLoading(true)
    fetch(
      `${process.env.REACT_APP_URL}screener?strat=social_trends&filter=top30`,
      {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
      }
    )
    .then(res => res.json())
    .then(response => {
      
      if(isMounted){
        if(response.status===200){
          setData(response.results)
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
          setData([])
          setIsLoading(false)
        }
        
      });
  }

  return (
    <React.Fragment>
      <div className="ticker-items-header-div">
        <div className="symbol-item-title-div">
          Company
        </div>
        <div className="score-item-title-div">
          Score
        </div>
        <div className="direction-item-title-div">
          Direction
        </div>
        <div className="activity-day-week-item-title-div">
          {`Average\nDay/Week`}
        </div>
      </div>
      <div className="ticker-items-list-div">
      {Array.isArray(data) 
        ? data.length === 0 ? isLoading ? `Please Wait...` : "" : data.map((item, j)=>{

            return (
              <div
                className="ticker-generic-item-div"
                onClick={()=>props.onSearchStockSymbol(item.ticker)}
                key={j}>
                  <div className="symbol-item-div">
                    {item['ticker']}
                  </div>
                  <div className="score-item-div">
                    {item['score'] > 60 ? "Very Positive" : item['score'] > 0 ? " Positive" : item['score'] > -60 ? "Negative" : "very Negative"}
                  </div>
                  <div className="direction-item-div">
                    {item['direction']}
                  </div>
                  <div className="activity-day-week-item-div">
                    {item['activity day-week']}
                  </div>
              </div>)

        })
        : null
      }
      </div>
      <div className="ticker-items-footer-div">
        {isLoading ? <Spinner size="20px" color="white" /> : `Last Updated: ${lastUpdated}`}
        <FaSyncAlt 
          onClick={requestData}
          className="refresh-icon-button"/>
      </div>
    </React.Fragment>
  );
}


const PatternsAnalysis = (props) => {

  const [lastUpdated, setLastUpdated] = useState("")
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false)


  useEffect(() => {
      // var dateUpdateTimer = setInterval(()=>setDate(new Date()), 1000 )
      // var patternsRatetimer = setInterval(requestData, 50000 )
      let isMounted = true;
      
      requestData(isMounted)
      return function cleanup() {
          isMounted=false;
          // clearInterval(dateUpdateTimer)
          // clearInterval(patternsRatetimer)
      }
  }, []);


  const requestData = (isMounted) => {

    setIsLoading(true)
    fetch(
    `${process.env.REACT_APP_URL}screener?strat=patterns_analysis&filter=top50`,
    {
      method: "GET",
      headers: { 'Content-Type': 'application/json' }
    }
  )
    .then(res => res.json())
    .then(response => {
      
             
      if(isMounted){
        if(response.status===200){
          setData(response.results)
          setLastUpdated(response.last_update)
          setIsLoading(false)
        } else {
            throw "error"
        }
      }

      
    })
    .catch(error => {
        console.log("am here at PatternsAnalysis error ", error)
        if(isMounted){
          setData([])
          setIsLoading(false)
        }
      });
  }

return (
  <React.Fragment>
  <div className="ticker-items-header-div">
    <div className="most-bullish-title-div">
      Most Bullish
    </div>
    <div className="most-bearish-title-div">
      Most Bearish
    </div>
  </div>
  <div className="ticker-items-list-div">
  {Array.isArray(data) 
    ? data.length === 0 ? isLoading ? `Please Wait...` : "" : data.map((item, j)=>{

        return (
          <div
            className="pair-item-div"
            key={j}>
              {item.map((company, i)=>{
                
                  return (
                    <div className="patterns-item-div"
                        onClick={()=>props.onSearchStockSymbol(company.ticker)}
                        key={i}>
                        <span className="company-symbol-item-span">{company.ticker}</span>          
                        <span className="company-name-item-span">{company.name}</span>    
                        <div className="patterns-score-item-div">
                          {company.hasOwnProperty('bulls') && <span> {`${company.bulls.toFixed(2)}%`} <FaCaretDown style={{color:"#14a52c", height:"100%"}}/> </span>}
                          {company.hasOwnProperty('bears') && <span> {`${company.bears.toFixed(2)}%`} <FaCaretUp style={{color:"red", height:"100%"}}/> </span>}
                        </div>
                    </div>
                  );

                })
              }
          </div>)
    })
    : null
  }
  </div>
  <div className="ticker-items-footer-div">
    {isLoading ? <Spinner size="20px" color="white"/> : `Last Updated: ${lastUpdated}`}
    <FaSyncAlt 
      onClick={requestData}
      className="refresh-icon-button"/>
  </div>
</React.Fragment>
 
  );
}


const MostGainers = (props) => {

  const [lastUpdated, setLastUpdated] = useState("")
  const [data, setData] = useState([]);
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
    fetch( `${process.env.REACT_APP_URL}screener?strat=most_gainers&filter=top30`,
    {
      method: "GET",
      headers: { 'Content-Type': 'application/json' }
    }
  )
    .then(res => res.json())
    .then(response => {
      
      
      if(isMounted){
        if(response.status===200){
          setData(response.results)
          setLastUpdated(response.last_update)
          setIsLoading(false)
        } else {
            throw "error"
        }
      }

      
    })
    .catch(error => {
        console.log("am here at MostGainers error ", error)
        if(isMounted){
          setData([])
          setIsLoading(false)
        }
      });
  }

  return (
    <React.Fragment>
      <div className="ticker-items-header-div">
        <div className="symbol-item-title-div">
          Company
        </div>
        <div className="score-item-title-div">
          Price
        </div>
        <div className="direction-item-title-div">
          Change
        </div>
        <div className="activity-day-week-item-title-div">
          
        </div>
      </div>
      <div className="ticker-items-list-div">
      {Array.isArray(data) 
        ? data.length === 0 ? isLoading ? `Please Wait...` : "" : data.map((item, j)=>{

            return (
              <div className="ticker-generic-item-div"
                onClick={()=>props.onSearchStockSymbol(item.ticker)}
                key={j}>
                  <div className="symbol-item-div">
                    {item['ticker']}
                  </div>
                  <div className="score-item-div">
                    {`%${item['price']}`}
                  </div>
                  <div className="direction-item-div">
                    {item['changes']}
                  </div>
                  <div className="activity-day-week-item-div">
                    {item['activity day-week']}
                  </div>
              </div>)

        })
        : null
      }
      </div>
      <div className="ticker-items-footer-div">
        {isLoading ? <Spinner size="20px" color="white"/> : `Last Updated: ${lastUpdated}`}
        <FaSyncAlt 
          onClick={requestData}
          className="refresh-icon-button"/>
      </div>
    </React.Fragment>
  );
}


const MostLosers = (props) => {



  const [lastUpdated, setLastUpdated] = useState("")
  const [data, setData] = useState([]);
  const [isLoading, setIsLoading] = useState(false)


  useEffect(() => {
      // var dateUpdateTimer = setInterval(()=>setDate(new Date()), 1000 )
      // var patternsRatetimer = setInterval(requestData, 50000 )
      
      let isMounted = true;
      
      requestData(isMounted)
      return function cleanup() {
          isMounted=false;
          // clearInterval(dateUpdateTimer)
          // clearInterval(patternsRatetimer)
      }
  }, []);


  const requestData = (isMounted) => {

    setIsLoading(true)
    fetch(
    `${process.env.REACT_APP_URL}screener?strat=most_losers&filter=top30`,
    {
      method: "GET",
      headers: { 'Content-Type': 'application/json' }
    }
  )
    .then(res => res.json())
    .then(response => {


      if(isMounted){
        if(response.status===200){
          setData(response.results)
          setLastUpdated(response.last_update)
          setIsLoading(false)
        } else {
            throw "error"
        }
      }
            
    })
    .catch(error => {
        console.log("am here at MostLoser error ", error)
        if(isMounted){
          setData([])
          setIsLoading(false)
        }
      });
  }

  return (
    <React.Fragment>
      <div className="ticker-items-list-div">
      {Array.isArray(data) 
        ? data.map((item, j)=>{

            return (
              <div
                className="ticker-generic-item-div"
                onClick={()=>props.onSearchStockSymbol(item.ticker)}
                key={j}>
                  <div className="company-info-div" >
                    <span className="company-symbol-span" >
                      {item.ticker}
                    </span>
                    <span className="company-name-span" >
                      {item.name}
                    </span>
                  </div>
              </div>)
        })
        : null
      }
      </div>
      <div className="ticker-items-footer-div">
        {isLoading ? <Spinner size="20px" color="white"/> : `Last Updated: ${lastUpdated}`}
        <FaSyncAlt 
          onClick={requestData}
          className="refresh-icon-button"/>
      </div>
    </React.Fragment>
  );
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
