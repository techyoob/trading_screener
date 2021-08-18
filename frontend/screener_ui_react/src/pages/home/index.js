

import React, { useState, useEffect } from 'react';
import './home.css';

import { FaSearch, FaCaretDown, FaCaretUp, FaSyncAlt } from 'react-icons/fa';
import Footer from '../../components/listFooter'
import LoadingSpinner from '../../components/loadingAnimation'

import {
  useQuery,
  useQueryClient,
  useMutation,
  QueryClient,
  QueryClientProvider,
} from 'react-query'




const HomePage = (props) => {
  
  
  const homePageItems = ["patterns analysis", "social trends", "most gainers"]


    function renderHOC(index) {

      switch(index) {
        case 0:
          return PatternsAnalysis ;
        case 1:
          return SocialTrends ;
        case 2:
        default:
          return MostGainers ;
      }

    }



    return (
      <div className="home-page-container">
        <div className="home-page-info">
          Welcome
        </div>
        <div className="home-page-lists">
          {homePageItems.map((item, index )=>{
              const WrappedComp = withLoadingQuery(renderHOC(index), item);
              
              return (
                <React.Fragment
                  key={index}>
                    <WrappedComp {...props} />
                </React.Fragment>
                );
              })
          }
        </div>
      </div>
    );
}

export default HomePage;



const withLoadingQuery = (WrappedComponent, componentName) => {

  function HOC(props) {

    const queryClient = useQueryClient();

    const { status, data, error, isFetching, refetch, dataUpdatedAt } = useQuery(
      componentName,
        () => fetch(`${process.env.REACT_APP_URL}screener?query=${componentName.replace(/\s+/g, '_').toLowerCase()}&filter=top30`).then(res =>
          res.json()
        )
    )

    const refreshData = () => {
      refetch()
    }


    return (
      <div className='ranking-list-component'>
        <div className='ranking-list-title'>
          {componentName}
        </div>
        <div className='ranking-list-body'>
          { isFetching && <LoadingSpinner /> }
          { !isFetching && <WrappedComponent data={data?.results} {...props}/> }
        </div>
        <div className='ranking-list-footer'>
          <Footer 
              refreshData={refreshData}
              lastUpdated={new Date(dataUpdatedAt).toLocaleString("en-US")}/>
        </div>
      </div>
    );
  }

  
  return HOC;
}




const PatternsAnalysis = (props) => {

  return (
    <React.Fragment>
      <div className="list-headers-container">
        <div className="most-bullish-title">
          Most Bullish
        </div>
        <div className="most-bearish-title">
          Most Bearish
        </div>
      </div>
      <div className="list-items">
        {props.data?.map((item, i)=> {
          
          return (
              <div className="patterns-analysis-item"
                    key={i}>
                  {item.map((company, j)=>{
                
                      return (
                        <div className="patterns-item-div"
                            onClick={()=>props.onSearchStockSymbol(company.ticker)}
                            key={j}>
                              <span className="company-symbol-item-span">{company.ticker}</span>          
                              <span className="company-name-item-span">{company.name?.substring(0, 22)}</span>    
                              <div className="patterns-score-item-div">
                                {company.hasOwnProperty('bulls') && <span> {`${company.bulls.toFixed(2)}%`} <FaCaretDown style={{color:"#14a52c", height:"100%"}}/> </span>}
                                {company.hasOwnProperty('bears') && <span> {`${company.bears.toFixed(2)}%`} <FaCaretUp style={{color:"red", height:"100%"}}/> </span>}
                              </div>
                        </div>
                        );
      
                      })
                  }
              </div>
            );
          })
        }
      </div>
      

    </React.Fragment>
  
    );
}



const SocialTrends = (props) => {

  return (
    <React.Fragment>
      <div className="list-headers-container">
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
      <div className="list-items">
        {props.data?.map((item, i)=> {
          
          return (
              <div className="social-trends-item"
                    key={i}
                    onClick={()=>props.onSearchStockSymbol(item.ticker)}>
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

              </div>
            );
          })
        }
      </div>
    </React.Fragment>
  );
}


const MostGainers = (props) => {


  return (
    <React.Fragment>
      <div className="list-headers-container">
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
      <div className="list-items">
        {props.data?.map((item, i)=> {
          
          return (
              <div className="most-gainers-item"
                    key={i}
                    onClick={()=>props.onSearchStockSymbol(item.ticker)}>
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
              </div>
            );
          })
        }
      </div>
    </React.Fragment>
  );
}

