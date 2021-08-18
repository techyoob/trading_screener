import HomePage from './home';
import StockWatchPage from './stockwatch';
import BigBangPage from './bigbang';
import AlertsPage from './alerts';





const PageWapper = (props) => {


    return (
        <div className='page-wapper'>
            {pageSelector(props)[props.selected]}
        </div>
    );
}

export default PageWapper;



const pageSelector = (props) => ({
    "alerts":<AlertsPage {...props}/>,
    "stock watch":<StockWatchPage {...props} />,
    "big bang": <BigBangPage {...props} />,
    "home":<HomePage {...props}/>    
  })


