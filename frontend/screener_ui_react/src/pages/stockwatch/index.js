


import React, { useState, useEffect, Component } from 'react';
import './stockwatch.css';
import '../pages.css';
import Carousel from "react-elastic-carousel";


import { 
    FaSearch,
    FaCaretDown,
    FaCaretUp,
    FaAngleLeft,
    FaAngleRight
} from 'react-icons/fa';

import Spinner from "react-svg-spinner";

import ChartComponent from '../../components/candlestickChart'
import MiniLineChart from '../../components/miniatureLineChart';
// import CandlestickChart from '../../components/candlestickChart';

// import { 
//     TypeOneAlert,
//     BollingerBandsAlert,
//     MovingAverageAlert
// } from '../../components/alerts'

import {
    useQuery,
    useQueryClient,
    useMutation,
    QueryClient,
    QueryClientProvider,
  } from 'react-query'
  
import LoadingSpinner from '../../components/loadingAnimation'
import AlertItem from '../../components/alerts'


const StockWatchPage = (props) => {
  
    const StockOverviewFetch = withFetchQuery(StockOverview, 'overview')
    const StockChartFetch = withFetchQuery(StockChart, 'chart')
    const StockAlertsFetch = withFetchQuery(StockAlerts, 'alerts')
    

    return (
        <div className="stock-watch-page-container">
            <div className="stock-watch-section-I">
                <StockOverviewFetch {...props}/>
            </div>
            <div className="stock-watch-section-II">
                <div className="stock-alerts-container">
                    <StockAlertsFetch {...props}/>
                </div>
                <div className="stock-chart-container">
                    <StockChartFetch {...props}/>
                </div>
            </div>
        </div>
    );
}

export default StockWatchPage;


const withFetchQuery = (WrappedComponent, componentName) => {

    function HOC(props) {
        const ticker = props.stock.ticker!=undefined? props.stock.ticker : "";
        const baseUrl = process.env.REACT_APP_URL;

        const [apiFilter, setApiFilter]=useState('def')
        const [apiURL, setApiURL] = useState(
                                  `${baseUrl}stock?ticker=${ticker}&query=${componentName}&filter=def`
                                )
                                
        const queryClient = useQueryClient();
  
        const { status, data, error, isFetching, refetch, dataUpdatedAt } = useQuery(
            componentName,
            () => fetch(apiURL).then(res =>
                res.json()
            ),
            {
                refetchInterval:300000,
            }
        )
  
        const refreshData = () => {
            refetch()
        }
        const setApiURLStr = (filter) => {
            setApiFilter(filter)
            
            refetch()
        }
        

        if(typeof data === 'undefined' || data === null || data.length === 0){            
            return (
                <LoadingSpinner />
            );
        }
  
        return (
            <React.Fragment>  
                <WrappedComponent data={data?.results} {...props} setApiFilter={setApiURLStr}/>
            </React.Fragment>
        );
    }
  
    
    return HOC;
  }
  
  




const StockOverview = (props) => {


    return(
        <div className="stock-overview">
            <div className="stock-overview-header">
                <div className="stock-ticker">
                    {props?.stock?.ticker}
                </div>
                <div className="stock-company">
                    {props?.data.length > 0 ? props?.data[1]['name'] : ''}
                </div>
            </div>
            <div className="stock-overview-details">
                {props?.data.map((item, i)=>{

                    const itemKey = Object.keys(item).length > 0 ? Object.keys(item)[0] : "";
                    const itemValue = item[itemKey]

                    if(i===0 || i===1)
                        return

                    return (
                        <div 
                            className="stock-overview-element"
                            key={i}>                    
                            <span className="overview-item-key"> {itemKey} </span>
                            <span className="overview-item-value"> {itemValue} </span>  
                        </div>
                    )
                    
                })}
            </div>
        </div>);
}




const StockChart = (props) => {


    const candleSize = ["def","1D", "5D"]
    const [selectedCandleSize, setSelectedCandleSize] = useState(candleSize[0]);


    const onSelectCandleSize = (size) => {
        setSelectedCandleSize(size)
    }

 
     return(
         <div className="candlestick-chart">
             <div className="candlestick-chart-header" >
                 {candleSize.map((item, index)=>{
 
                     return (item==='def' ? null : 
                        <button 
                            className={`${selectedCandleSize===item? "selected-" : ""}candle-size-div`}
                            key={index}
                            disabled={selectedCandleSize===item? true : false }
                            onClick={()=> onSelectCandleSize(item)}>
                            {item}
                        </button>)
 
                 })}
             </div>
             <div className="candlestick-chart-body">
                 <ChartComponent data={props.data}/>
             </div>
         </div>
     );
 }
 
 
 
const StockAlerts = (props) => {


    const breakPoints = [
        { width: 1, itemsToShow: 1 },
        { width: 550, itemsToShow: 3, itemsToScroll: 1 },
        { width: 768, itemsToShow: 4 },
        { width: 1200, itemsToShow: 4 }
      ];


    return (
        <div className="stock-alerts">
            <div className="stock-alerts-title">
                Alerts
            </div>
            <div className="stock-alerts-carousel">
                <Carousel 
                    breakPoints={breakPoints}
                    itemPadding={[0, 20]}
                    pagination={false}>
                    {props?.data?.map((item, i) => (
                        <div className="stock-alert-item" key={i}>
                            <AlertItem name={item.name} item={item.item} />
                        </div>
                    ))}
                </Carousel>
            </div>
        </div>
    );
}

