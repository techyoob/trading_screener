














import React, {useState} from 'react';
import './alerts.css'
import PropTypes from 'prop-types';


const AlertItem = (props) => {


    const alertLoader = (props) => ({
        'new high':<TypeOneAlert {...props}/>,
        'new low':<TypeOneAlert {...props}/>,
        'bollinger bands':<BollingerBandsAlert {...props}/>,    
        'moving average':<MovingAverageAlert {...props}/>
    })


    return (
        <React.Fragment>
            {alertLoader(props)['new high']}
        </React.Fragment>
    );
};

export default AlertItem;



// const index = props => {
//     return (
//         <div>
            
//         </div>
//     );
// };

// index.propTypes = {
    
// };

// export default index;





const TypeOneAlert = (props) => {
    
    const price = props?.item?.price ? props?.item?.price : 0
    const date = props?.item?.price_date ? props?.item?.price_date : ''

    return (
      <div className="type-I-alert-container">
        <div className="type-I-alert-title-div">
            {props?.name}
        </div>
        <div className="type-I-alert-price-div">
            {`Price: $${price.toFixed(2)}`}
        </div>
        <div className="type-I-alert-date-div">
            {`ON: ${date}`}
        </div>
      </div>
    )
}
  


const BollingerBandsAlert = (props) => {

    const signal = props?.item?.signal ? props?.item?.signal : '';
    const signalPrice = props?.item?.signal_price ? props?.item?.signal_price : ''
    const signalDate = props?.item.signal_date ? props?.item.signal_date : ''
    

  
    return (
      <div className="bollinger-band-alert-div">
        <div className="type-I-alert-title-div">
            {props?.name}
        </div>
        <div className="type-I-alert-price-div">
            {`Signal: $${signal}`}
        </div>
        <div className="type-I-alert-price-div">
            {`Price: $${signalPrice}`}
        </div>
        <div className="type-I-alert-date-div">
            {`ON: ${signalDate}`}
        </div>
      </div>
    )
}
  


const MovingAverageAlert = (props) => {

    const sma = props?.item?.sma ? props.item.sma : '';
    const smaDate = props?.item?.sma_date ? props?.item?.sma_date : '';

    const ema = props?.item?.ema ? props.item.ema : '';
    const emaDate = props?.item?.ema_date ? props?.item?.ema_date : '';

  
    return (
      <div className="bollinger-band-alert-div">
        <div className="type-I-alert-title-div">
            {props.name}
        </div>
        <div className="type-I-alert-price-div">
            {`SMA: $${sma} On ${smaDate}`}
        </div>
        <div className="type-I-alert-date-div">
            {`EMA: ${ema} On ${emaDate}`}
        </div>
      </div>
    )
}
  




