

import React, { useState } from 'react';
import './App.css';



import SystemOverviewPage from './pages/systemOverview';
import Menu from './menu/menu';



const menuElements = ["system overview"]

function App() {

  const [selectedPage, setSelectedPage] = useState(menuElements[0])

  const onSelectPage = (selected) => {
    
    setSelectedPage(selected)
  }

  return (
    <div className="screener-manager-app-div">
      <div className="menu-div">
        <Menu
            items={menuElements}
            onSelectPage={onSelectPage}/>
      </div>
      <div className="pages-container-div">
        <div className="pages-div">
          {pageLoader()[selectedPage]}
        </div>        
      </div>
    </div>
  );
}

export default App;



const pageLoader = () =>({
  "system overview":<SystemOverviewPage />
})