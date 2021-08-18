


import React, { useState, useEffect, useRef } from 'react';
import './alerts.css';

import {
  useQuery,
  useQueryClient,
  useMutation,
  QueryClient,
  QueryClientProvider,
} from 'react-query'

import Footer from '../../components/listFooter'
import LoadingSpinner from '../../components/loadingAnimation'


import { 
  NewHighListItem,
  NewLowListItem,
  BollingerBandsListItem,
  MovingAverageListItem
 } from "./alertsListItems"


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

  const [selectedAlertName, setSelectedAlertName] = useState("new high")
  const queryKey = 'alerts'
  
  const queryClient = useQueryClient();

  const onAlertChange = (alertName) => {

    queryClient.resetQueries(queryKey, { exact: true })
    setSelectedAlertName(alertName)
  }

  const { status, data, error, isFetching, refetch, dataUpdatedAt } = useQuery(
    queryKey,
      () => fetch(`${process.env.REACT_APP_URL}alert?query=${selectedAlertName}&filter=all`).then(res =>
        res.json()
      ),
      {
        initialData:[],
        enabled: false
      }
   
  )

  const refreshData = () => {
    refetch()
    
  }


  useEffect(()=>{
    refreshData();
  },[selectedAlertName])

  return (
      <div className="alerts-page-div">
        <section className="alerts-list-section">
          <AlertsList
            alertName={selectedAlertName}
            onAlertChange={onAlertChange}/>
        </section>
        <section className="selected-alert-section">
          <SelectedAlertBody 
              onRefreshAlertData={refreshData}
              alertData={data?.results}
              alertName={selectedAlertName}
              lastUpdated={new Date(dataUpdatedAt).toLocaleString("en-US")}
              isLoading={isFetching}/>
        </section>
      </div>
    );
}

export default AlertsPage;






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
  
    const selectedAlert = props.alertName.replace(/\s/g , "_")
    
    return (
      <div className="alerts-body-div">
        <div className="alert-title-div">
          {`Selected Alert`}
        </div>
        <div className="alert-headers-div">
          <div className="ticker-alert-title-I-div">
            Name
          </div>
          <div className="ticker-alert-title-II-div">
            {props.alertName.toUpperCase()}
          </div>
        </div>
        <div className="alert-items-div">
          {props?.alertData?.map((item, i)=>{
            
              return (
                <div className="ticker-alert-item-div"
                    key={i}
                    onClick={()=>props.onAlertChange(item.name)}>
                      <div className="ticker-alert-title-I-div">
                        {item.ticker}
                      </div>
                      <div className="ticker-alert-title-II-div">
                        {props.alertName=='new high' && <NewHighListItem item={item} />}
                        {props.alertName=='new low' && <NewLowListItem item={item} />}
                        {props.alertName=='bollinger bands' && <BollingerBandsListItem item={item} />}
                        {props.alertName=='moving average' && <MovingAverageListItem item={item} />}
                        
                      </div>
                </div>);
          })}
        </div>
        <div className="alert-footers-div">
          <Footer 
            refreshData={props.onRefreshAlertData}
            lastUpdated={new Date(props.lastUpdated).toLocaleString("en-US")}/>
        </div>
      </div>
    );
}













