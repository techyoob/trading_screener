

import React, { useState, useEffect } from 'react';
import './systemOverview.css';


import Spinner from "react-svg-spinner";


const SystemOverviewPage = (props) => {

    const [overviewItems, setOverviewItems] = useState([])
    const [isLoading, setIsLoading] = useState(false)

    useEffect(()=>{
                
      let isMounted = true;
        
      requestData(isMounted)
      return function cleanup() {
          isMounted = false;
      }
    }, [])

    
    const requestData = (isMounted) => {


      setIsLoading(true)
      fetch(
      `${process.env.REACT_APP_URL}manager?query=system overview`,
        {
        method: "GET",
        headers: { 'Content-Type': 'application/json' }
        })
      .then(res => {
        return res.json()
      })
      .then(response => {

          if(isMounted){
              if(response.status===200){

                setOverviewItems(response.results)
                setIsLoading(false)
              } else {
                  throw "error"
              }
          }

      })
      .catch(error => {

          if(isMounted){
            setOverviewItems([])
              setIsLoading(false)
            }
      });
    }




    return (
      <div className="system-overview-page-div">
        {isLoading? <Spinner  size="20px" color="white" /> : overviewItems.map((item, i)=>{

            return (
              <div
                className="overview-item-div"
                key={i}>
                  <div className="overview-item-name-div"> {item?.name} </div>
                  <div className="overview-item-status-div"> 
                      <span className="overview-item-status-logo"
                        style={{background:item?.isActive? `green` : `red`}}>
                        {item?.isActive? `Active` : `Inactive`}  
                      </span>
                  </div>
              </div>
            );

        })}
      </div>
    );
  }
  
export default SystemOverviewPage;

