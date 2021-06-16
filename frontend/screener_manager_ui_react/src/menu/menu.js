


import React, { useState, useEffect } from 'react';
import './menu.css';





const Menu = (props) => {


    return (
      <React.Fragment>
        <div className="menu-header">          
          <span>BIG BANG SCREENER</span>
          <span>MANAGER</span>
        </div>
        {props.items.map((item, index)=>{
          return (
            <div className="menu-item-div"  key={index}>
              {MenuItemLoader({
                item, 
                onSelectPage:props.onSelectPage})}
            </div> 
          );
                     
        })}
      </React.Fragment>
    );
  }


export default Menu;



  
  const MenuItemLoader = (props) => {
  
  
    const onSelectPage = (page) => {
      props.onSelectPage(page)
    }
  
    switch(props.item){
      case "search":
      default:
        return(
          <div 
            className="default-menu-item-div" 
            onClick={()=>onSelectPage(props.item)}>
            {props.item}
          </div>
        );
    }
  
  }
  
  
  
  