

// main comp


import React, { useState, useEffect } from 'react';
import './App.css';
import { FaSearch, FaCaretDown, FaCaretUp } from 'react-icons/fa';

import { useInterval } from './hooks/useInterval'


import HomePage from './pages/home';
import StockWatchPage from './pages/stockwatch';
import BigBangPage from './pages/bigbang';
import AlertsPage from './pages/alerts';
import Menu from './menu/menu';
import TestPage from './pages/tests';

const menuElements = ["home", "alerts", "stock watch",  "big bang", "search"]

function App() {

  const [selectedPage, setSelectedPage] = useState(menuElements[2])
  const [stock, setStock] = useState({
    name:"",
    ticker:"AAPL"
  })
  

  const onSelectPage = (selected) => {
    setSelectedPage(selected)
  }

  const onSearchStockSymbol = (ticker) => {
    setStock({...stock, ticker:ticker.toUpperCase()})
    onSelectPage('stock watch')
  }

  return (
    <div className="shares-screener-app-div">
      <div className="menu-div">
        <Menu
          items={menuElements}
          onSelectPage={onSelectPage}
          onSearchStockSymbol={onSearchStockSymbol}/>
      </div>
      <div className="pages-container-div">
        <Pages 
          selected={selectedPage}
          stock={stock}
          onSearchStockSymbol={onSearchStockSymbol}/>
      </div>
    </div>
  );
}

export default App;







const Pages = (props) => {
  


  return (
    <div className="pages-div">
      {PagesPicker({
        selected:props.selected,
        ...props})}
    </div>
  );
}


const PagesPicker = (props) => {
  

  switch(props.selected){
    case "alerts":
      return (
        <React.Fragment >
          <AlertsPage {...props}/>
        </React.Fragment>
      );
    case "stock watch":
      return (
        <React.Fragment >
          <StockWatchPage {...props} />
        </React.Fragment>
      );
    case "test page":
      return (
        <React.Fragment >
          <TestPage {...props} />
        </React.Fragment>
      );
    case "big bang":
      return (
        <React.Fragment >
          <BigBangPage {...props} />
        </React.Fragment>
      );
    case "home":
    default:
      return (
        <React.Fragment >
          <HomePage {...props}/>
        </React.Fragment>
      );
  }

}

