













export const TypeOneAlert = (props) => {

    return (
      <div className="type-I-alert-div">
        <div className="type-I-alert-title-div">
            {props.name}
        </div>
        <div className="type-I-alert-price-div">
            {`Price: $${props.item.price.toFixed(2)}`}
        </div>
        <div className="type-I-alert-date-div">
            {`ON: ${props.item.price_date}`}
        </div>
      </div>
    )
}
  


export const BollingerBandsAlert = (props) => {

    

  
    return (
      <div className="bollinger-band-alert-div">
        <div className="type-I-alert-title-div">
            {props.name}
        </div>
        <div className="type-I-alert-price-div">
            {`Signal: $${props.item?.signal}`}
        </div>
        <div className="type-I-alert-price-div">
            {`Price: $${props.item?.signal_price}`}
        </div>
        <div className="type-I-alert-date-div">
            {`ON: ${props.item.signal_date}`}
        </div>
      </div>
    )
}
  


export const MovingAverageAlert = (props) => {

    

  
    return (
      <div className="bollinger-band-alert-div">
        <div className="type-I-alert-title-div">
            {props.name}
        </div>
        <div className="type-I-alert-price-div">
            {`SMA: $${props.item?.sma} On ${props.item?.sma_date}`}
        </div>
        <div className="type-I-alert-date-div">
            {`EMA: ${props.item.ema_date} On ${props.item?.ema_date}`}
        </div>
      </div>
    )
}
  
