import { useState } from "react";
import './alerts.css';













export const NewHighListItem = (props) => {

    const newHigh = props.item['new_high']

    return (
      <div className="alert-list-item-div">
          <div className="alert-list-item-I-div"> {`$${newHigh?.price.toFixed(2)} `} </div>
          <div className="alert-list-item-I-div"> on</div>
          <div className="alert-list-item-I-div"> {`${newHigh?.price_date} `}  </div>
      </div>
    )
}
  

export const NewLowListItem = (props) => {

    const newLow = props.item['new_low']
    
    return (
      <div className="alert-list-item-div">
          <div className="alert-list-item-I-div"> {`$${newLow?.price.toFixed(2)} `} </div>
          <div className="alert-list-item-I-div"> on</div>
          <div className="alert-list-item-I-div"> {`${newLow?.price_date} `}  </div>
      </div>
    )
}
  

export const BollingerBandsListItem = (props) => {

    const bollingerBands = props.item['bollinger_bands']
    
    return (
      <div className="alert-list-item-div">
          <div className="alert-list-item-I-div"> {`$${bollingerBands?.signal_price} `} </div>
          <div className="alert-list-item-I-div"> on</div>
          <div className="alert-list-item-I-div"> {`${bollingerBands?.signal_date} `}  </div>
          <div className="alert-list-item-I-div"> {`${bollingerBands?.signal} `}  </div>
      </div>
    )
}
  






export const MovingAverageListItem = (props) => {

  const movingAverage = props.item['moving_average']
  
  return (
    <div className="alert-list-item-div">
        <div className="alert-list-item-I-div"> {`SMA: ${movingAverage?.sma} `} </div>
        <div className="alert-list-item-I-div">  {`On ${movingAverage?.sma_date} `} </div>
        <div className="alert-list-item-I-div"> {`EMA: ${movingAverage?.ema} `}  </div>
        <div className="alert-list-item-I-div"> {`On ${movingAverage?.ema_date} `}  </div>
    </div>
  )
}


