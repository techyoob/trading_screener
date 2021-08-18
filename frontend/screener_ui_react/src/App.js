

// main comp


import React, { useState } from 'react';
import './App.css';


import {
  QueryClient,
  QueryClientProvider,
} from 'react-query'



import PageWapper from './pages'
import Menu from './menu/menu';
import ToolBar from './menu/toolBar';

const menuElements = ["home", "alerts", "stock watch",  "big bang"]



const queryClient = new QueryClient()






function App() {

  const [selectedPage, setSelectedPage] = useState(menuElements[0])
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
    <QueryClientProvider client={queryClient}>
      <div className="shares-screener-main-container">
        <div className="dashboard-menu-container">
          <Menu
              items={menuElements}
              selectedItem={selectedPage}
              onSelectPage={onSelectPage}
              onSearchStockSymbol={onSearchStockSymbol}/>
        </div>
        <div className="dashboard-body-container">
          <div className="dashboard-header-container">
            <ToolBar
              onSearchStockSymbol={onSearchStockSymbol}/>
          </div>
          <div className="dashboard-pages-container">
            <PageWapper
              selected={selectedPage}
              stock={stock}
              onSearchStockSymbol={onSearchStockSymbol}/>
          </div>
        </div>
      </div>
    </QueryClientProvider>
  );
}


export default App;
