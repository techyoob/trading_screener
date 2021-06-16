













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
  


export const BollingerBandSqueezeAlert = (props) => {

    

  
    return (
      <div className="bollinger-band-alert-div">

      </div>
    )
}
  
