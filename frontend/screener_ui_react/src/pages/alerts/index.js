


import React, { useState, useEffect, useRef } from 'react';
import './alerts.css';
import '../pages.css';

import CandlestickPatternsAnalysis from './candlestickPatternsAnalysis'

import { 
    FaSearch,
    FaCaretDown,
    FaCaretUp,
    FaAngleLeft,
    FaAngleRight,
    FaSyncAlt
} from 'react-icons/fa';

import alerts from './alerts.json'
import Spinner from "react-svg-spinner";



const AlertsPage = (props) => {

  const [isLoading, setIsLoading] = useState(false)
  const [selectedAlertName, setSelectedAlertName] = useState("new high")
  const [selectedAlertData, setSelectedAlertData] = useState([])
  
  const [lastUpdated, setLastUpdated] = useState("")


  const onAlertChange = (alertName) => {
    setSelectedAlertName(alertName)
  }

  useEffect(()=>{

    let isMounted = true;
      
    onRequestData(isMounted)
    return function cleanup() {
        isMounted=false;
    }
  }, [selectedAlertName])


  const onRequestData = (isMounted) => {

      if(isLoading){
        return;
      }
      

      setIsLoading(true)
      fetch( `${process.env.REACT_APP_URL}alert?name=${selectedAlertName}&filter=5days`,
      {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
      }
      )
      .then(res => res.json())
      .then(response => {
        
        
        if(isMounted){
          if(response.status===200){
            
            setSelectedAlertData(response.results)
            setLastUpdated(response.last_updated)
            setIsLoading(false)
          } else {
              throw "error"
          }
        }
  
        
      })
      .catch(error => {
          console.log("API request error at AlertsPage ", error)
          if(isMounted){
            setSelectedAlertData([])
            setIsLoading(false)
          }
        });



  }

    return (
      <div className="alerts-page-div">
        <section className="alerts-list-section">
          <AlertsList
            alertName={selectedAlertName}
            onAlertChange={onAlertChange}/>
        </section>
        <section className="selected-alert-section">
          <SelectedAlertBody 
              onRefreshAlertData={onRequestData}
              alertData={selectedAlertData}
              alertName={selectedAlertName}
              lastUpdated={lastUpdated}
              isLoading={isLoading}/>
        </section>

      </div>
    );
}







const AlertsList = (props) => {


    return (
      <div className="alerts-list-div">
        <div className="alerts-list-header-div">
          alerts
        </div>
        <div className="alerts-list-body-div">

          {alerts.map((item, i)=>{         

            return (
              <div className="alert-item-div"
                  key={i}
                  onClick={()=>props.onAlertChange(item.name)}>
                    {item.name}
              </div>
            );

          })}
        </div>
      </div>
    );
}




const SelectedAlertBody = (props) => {
  // props.isLoading

    const selectedAlert = props.alertName.replace(/\s/g , "_")
    

    return (
      <div className="alerts-body-div">
        <div className="alert-title-div">
          {`${props.alertName} alerts in last 5 days`}
        </div>
        <div className="alert-headers-div">
          <div className="ticker-alert-title-div">
            Name
          </div>
          <div className="ticker-alert-title-div">
            {props.alertName.toUpperCase()}
          </div>
          <div className="ticker-alert-title-div">
            Price Date
          </div>
          <div className="ticker-alert-title-div">
            
          </div>
        </div>
        <div className="alert-items-div">
          {props.isLoading 
            ? null
            : props.alertData.map((item, i)=>{
              
                return (
                  <div className="ticker-alert-item-div"
                      key={i}
                      onClick={()=>props.onAlertChange(item.name)}>
                        <div className="ticker-alert-title-div">
                          {item.ticker}
                        </div>
                        <div className="ticker-alert-title-div">
                          {`$ ${item[selectedAlert]?.price.toFixed(2)}`}
                        </div>
                        <div className="ticker-alert-title-div">
                          {item[selectedAlert]?.price_date}
                        </div>
                        <div className="ticker-alert-title-div">
                          
                        </div>
                  </div>);
              })
          }
        </div>
        <div className="alert-footers-div">
          <span className="last-list-update">
            {props.isLoading 
            ? <Spinner size="20px" color="white" /> 
            : ` Last Updated: ${props.lastUpdated}`}
            </span>
          <FaSyncAlt 
            onClick={props.onRefreshAlertData}
            className="refresh-icon-button"/>
        </div>
      </div>
    );
}






// const AlertsPage = (props) => {

//   const [ strategies, setStrategies ] = useState(["patterns rating", "ai model I prediction"])
  
//     return (
//       <div className="alerts-page-div">
//          <StrategiesLayoutTwo />
//       </div>
      
//     );
//   }
    
export default AlertsPage;
  




const StrategiesLayoutTwo = (props) => {


  const [lastUpdated, setLastUpdated] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const [data, setData] = useState([])
  const [strategiesList, setStrategiesList] = useState([
    {
      name:"Alert I",
      isChecked:false
    },
    {
      name:"Alert II",
      isChecked:false
    },
    {
      name:"Alert III",
      isChecked:false
    },
    {
      name:"Alert IV",
      isChecked:false
    }
  ])

  useEffect(()=>{

    let isMounted = true;      
    onRequestScreenerList(isMounted)
    return function cleanup() {
      isMounted=false;
    }
  }, [])

  const toggleCheckboxChange = (name, isChecked, index) => {

    const updatedList = Object.assign([], strategiesList, {[index]: {name:name, isChecked:!isChecked}});
      setStrategiesList(updatedList);
    }


  const onRequestScreenerList = (isMounted) => {

    const stratsQuery = strategiesList.reduce((accumulator, currentValue)=>{

        if(currentValue.isChecked===true){
          return accumulator.concat(currentValue.name, ",");
        }

        return accumulator
    }, "strats=")


    setIsLoading(true)
    fetch( `${process.env.REACT_APP_URL}screener?strat=most_actives&&filter=top30&${stratsQuery}`,
      {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
      }
    )
    .then(res => res.json())
    .then(response => {

      if(isMounted){
        if(response.status===200){
          setData(response.data)
          setIsLoading(false)
        } else {
            throw "error"
        }
      }

    })
    .catch(error => {
        console.log("am here at error ", error)
        if(isMounted){
          setData([])
          setIsLoading(false)
        }
    });

  }



  return (
    <React.Fragment>
      <div className="strategy-list-div">
          <div className="strategy-list-title-div">
            Alerts
          </div>
          <div className="strategy-list-body-div">
          {strategiesList.map((strategy, index )=>{

              return (
                <div
                  className="strategy-item-div"
                  key={index}
                  onClick={()=>toggleCheckboxChange(strategy.name, strategy.isChecked, index)}>
                        <input
                          type="checkbox"
                          checked={strategy.isChecked}
                        />
                        <span>{strategy.name}</span>
                </div>);
              })}
          </div>
          <div 
            className="strategy-list-footer-div">
            <label 
              className="strategy-filter-button"
              onClick={onRequestScreenerList}> 
              Filter 
            </label>            
          </div>
      </div>
      <div className="tickers-rank-div" >
          <div className="table-header-div">
            <div className="table-name-div">
              Picks
            </div>
            <div className="table-columns-div">
              <StrategiesTableHeader sampleItem={data.length > 0 ? data[0] : {}} />
            </div>
          </div>
          <div className="table-body-div">
              {data.length > 0 
                ?  <StrategiesTableBody data={data}/>
                : isLoading ? <span> Please Wait... </span> : ""
              }
          </div>
          <div className="table-footer-div">
            {isLoading ? <Spinner size="20px" color="white" /> : `Last Updated: ${lastUpdated}`}
            <FaSyncAlt 
              onClick={onRequestScreenerList}
              className="refresh-icon-button"/>
          </div>
      </div>
    </React.Fragment>
  );

}


const StrategiesTableHeader = (props) => {

  return (
  <React.Fragment>
    {Object.keys(props.sampleItem) < 3  
      ?  null 
      : <React.Fragment>
          <div className="symbol-column-title-div">
            Company
          </div>
          <div className="price-column-title-div">
            Price
          </div>
          <div className="changes-item-title-div">
            Changes
          </div>
          {'strategies' in props.sampleItem && Object.keys(props.sampleItem.strategies).map((strategy, i)=>{
              return <div key={i} className="strategy-item-title-div">{strategy}</div>;
            })
          }
        </React.Fragment>
    }
  </React.Fragment>
  )  
}


const StrategiesTableBody = (props) => {

  return (
  <div className="table-body-items-div">
    {props.data.map((item, j)=>{

        return (
          <div
            className="table-list-item-div"
            onClick={()=>props.onSearchStockSymbol(item.ticker)}
            key={j}>
              <div className="table-symbol-item-div">
                {item['ticker']}
              </div>
              <div className="table-price-item-div">
              {`$${item['price']}`}
              </div>
              <div className="table-changes-item-div">
                {`$${item['changes']}`}
              </div>
              {'strategies' in item && Object.keys(item.strategies).map((strategy, i)=>{
                  return <div key={i} className="table-strategy-item-div">{item.strategies[strategy]}</div>;
                })
              }
          </div>)

        })
    }
  </div>
  )  
}




const TickerRowItem = (props) => {


  return (
    <React.Fragment>
      {props.index === 0 && 
        <div className="ticker-list-header-div">
          <span className="ticker-name-column-text">Name</span>
          <span className="ticker-price-column-text">Price</span>
          <span  className="ticker-change-column-text">Changes</span>
          {Object.keys(props.item['strategies']).map((stratItem, index )=>{
                return (
                <span 
                  className="ticker-strat-column-text"
                  key={index}>
                    {stratItem}
                </span>);
            })
          }
        </div>
      }
      <div className="ticker-strats-row-item-div">
          <span className="ticker-name-column-text"><Name item={props.item} /></span>
          <span className="ticker-price-column-text"><Price item={props.item} /></span>
          <span  className="ticker-change-column-text"><Changes item={props.item} /></span>
          {Object.keys(props.item['strategies']).map((stratItem, index ) => {
                return (
                  <span 
                    className="ticker-strat-column-text"
                    key={index}>
                      <StartegyItemLoader item={props.item} strategy={stratItem} />                      
                  </span>);
            })
          }
      </div>
    </React.Fragment>);

}




const Name = (props) => {


  return (
    <div className="ticker-item-div">
        <span className="ticker-name-item-div" >{props.item.ticker}</span>
        <span className="ticker-symbol-item-div">{props.item.name}</span>
    </div>);
}



const Price = (props) => {

  return props.item.price;
}


const Changes = (props) => {

  return props.item.changes;
}


const StartegyItemLoader = (props) => {


  switch(props.strategy){
    case "patterns analysis":
      return (<CandlestickPatternsAnalysis {...props} />);
    default:
      return null;
  }
  
}