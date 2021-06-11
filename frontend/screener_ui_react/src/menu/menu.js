


import React, { useState, useEffect } from 'react';
import './menu.css';
import { FaSearch, FaCaretDown, FaCaretUp } from 'react-icons/fa';





const Menu = (props) => {


    return (
      <React.Fragment>
        <div className="menu-header">
          BIG BANG SCREENER
        </div>
        {props.items.map((item, index)=>{
          return (
            <div className="menu-item-div"  key={index}>
              {MenuItemLoader({
                item, 
                onSelectPage:props.onSelectPage,
                onSearchStockSymbol:props.onSearchStockSymbol})}
            </div> 
          );
                     
        })}
      </React.Fragment>
    );
  }


export default Menu;



  
  const MenuItemLoader = (props) => {
  
    const [searchKeywork, setSearchKeyword] = useState("");
  
    const updateSearchKeyWord = (e) => {
      setSearchKeyword(e.target.value)
    }
  
    const onSearch = () => {
        props.onSearchStockSymbol(searchKeywork)
        // props.onSelectPage('screener')
  
        setSearchKeyword("")
    }
  
  
    const onSelectPage = (page) => {
      props.onSelectPage(page)
    }
  
    switch(props.item){
      case "search":
        return(
          <div className="search-menu-item-div" >
            <input 
              className="search-input"
              type = "text"
              placeholder="Enter Share Symbol"
              onChange = {updateSearchKeyWord}
              value={searchKeywork}/>
            <button
              disabled={searchKeywork.length === 0 ? true : false}
              className="search-button"
              onClick={onSearch}>
                <FaSearch className="search-icon"/>
              </button>
                
          </div>
        );
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
  
  
  
  