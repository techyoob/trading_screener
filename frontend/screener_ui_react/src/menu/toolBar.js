


import React, { useState, useEffect } from 'react';
import './menu.css';
import { 
  FaSearch,
  FaBell,
  FaRegUser,
  FaUserCircle 
} from 'react-icons/fa';





const ToolBar = (props) => {
    const [searchKeywork, setSearchKeyword] = useState("");
  
    const updateSearchKeyWord = (e) => {
      setSearchKeyword(e.target.value)
    }
  

    const onSearch = () => {
      
        props.onSearchStockSymbol(searchKeywork)  
        setSearchKeyword("")
    }
  
  
    return (
      <div className="toolbar-container">
        <div className="tools-container">
          <div className="search-bar">
            <input 
                  className="search-input"
                  type = "text"
                  placeholder="Enter Share Symbol"
                  onChange = {updateSearchKeyWord}
                  onKeyPress={(e) => e.key === 'Enter' && searchKeywork.length > 0? onSearch() : null}
                  value={searchKeywork}/>
              <FaSearch 
                    className="search-button"
                    onClick={()=> searchKeywork.length > 0 ? onSearch() : null}/>
          </div>
        </div>        
        <div className="user-notifications-container">
          <div className="user-notifications-button"
                onClick={()=>console.log("user notification overlay box")}>
            <FaBell />
          </div>
        </div>
        <div className="user-profile-container">
          <div className="user-name">John Doe</div>
          <div 
            className="user-logo"
            onClick={()=>console.log("user profile overlay box")}>
            <FaUserCircle />    
          </div>
        </div>
      </div>
    );
  }


export default ToolBar;


