


import React, { useState, useEffect, Component } from 'react';
import './bigbang.css';


import {
    useQuery,
    useQueryClient,
    useMutation,
    QueryClient,
    QueryClientProvider,
  } from 'react-query'
  
import Footer from '../../components/listFooter' 
  

import Spinner from "react-svg-spinner";





const BigBangPage = (props) => {


    const [lastUpdated, setLastUpdated] = useState("")
    const [tableData, setTableData] = useState([]);    
    const [tableHeader, setTablHeader] = useState(["Ticker","Current", "Forecasting"]);

    const queryKey = 'picks'
    const queryClient = useQueryClient();
    
    const { status, data, error, isFetching, refetch, dataUpdatedAt } = useQuery(
      queryKey,
        () => fetch(`${process.env.REACT_APP_URL}screener?query=big_bang&filter=top50`).then(res =>
          res.json()
        ),
        {
          initialData:[]
        }
     
    )
  
    const refreshData = () => {
      refetch()
      
    }


    return (
        <div className="screener-picks-container">
            <div className="screener-picks-title">
                Screener Picks
            </div>
            {isFetching 
            ? <div className="spinner-container">
                <p>Please Wait ...</p>
                <Spinner size="20px" color="white" />
            </div>
            : <div className="big-bang-list-body-div">
                    <table id='tickers-list'>
                        <thead>
                            <tr>
                                {tableHeader.map((item, i)=>{
                                    return <th key={i}>{item}</th>
                                })}
                            </tr>
                        </thead>
                        <tbody>
                            {data.results?.map((item, j) => {

                                return (
                                    <tr
                                        onClick={()=>props.onSearchStockSymbol(item.ticker)}
                                        key={j}>
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
                </div>}
            <div className="big-bang-list-footer-div">
                <Footer
                    refreshData={refreshData}
                    lastUpdated={new Date(dataUpdatedAt).toLocaleString("en-US")}/>
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
