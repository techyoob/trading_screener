


import React, { useState, useEffect } from 'react';
import './menu.css';
import { 
  FaSearch, 
  FaSignOutAlt,
  FaHome,
  FaFireAlt,
  FaChartArea,
  FaAtom
} from 'react-icons/fa';






const Menu = (props) => {

  const [hover, setHover]=useState(false);

  const onSelectPage = (page) => {
    props.onSelectPage(page)
    }

    const onLogout = () => {
      console.log(" logging out... ");
    }



return (
  <React.Fragment>
    <div className="app-name-logo-container" >
      <span> {process.env.REACT_APP_NAME} </span>
    </div>
    <div className="menu-items-container" >
      {props.items.map((item, index)=>{
        return (
          <div 
            className={`menu-item-container${props?.selectedItem === item ? '-selected' : ''}`}
            key={index}
            onClick={()=>onSelectPage(item)}
            onMouseEnter={()=>setHover(true)} 
            onMouseLeave={()=>setHover(false)}>
              <span>{menuIcons[item]}</span>
              {item}
          </div> 
        );
                  
      })}
    </div>
    <div className="logout-button"
          onClick={onLogout}>
      <span>{menuIcons['logout']}</span>
      Logout
    </div>

  </React.Fragment>
);
}

export default Menu;









// Object literals for icons 
const menuIcons={
  "home":<FaHome />,
  "alerts":<FaFireAlt/>,
  "stock watch":<FaChartArea/>,
  "big bang":<FaAtom/>,
  "logout":<FaSignOutAlt/>
}




const styles = {
    menuItem:({op1, op2})=> ({
      backgroundColor: op1? "#ad9ac7": "inherit",
      color: op1?'#ffffff':'inherit'
    }),
}
