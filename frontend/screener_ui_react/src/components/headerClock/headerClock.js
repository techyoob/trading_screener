













const HeaderClock = (props) => {



    const [clockData, setClockData ] = useState({
      day:new Date().toLocaleDateString("en-US", {weekday: 'short', month:"short", day:"2-digit"}),
      time:new Date().toLocaleTimeString("en-US", {hour:"2-digit", minute:"2-digit"})
    })
  
    useEffect(() => {
  
        const onSetClock = () => {
          
          const day  = new Date().toLocaleDateString("en-US", {weekday: 'short', month:"short", day:"2-digit"});
          const time = new Date().toLocaleTimeString("en-US", {hour:"2-digit", minute:"2-digit"});
          setClockData({day, time})
        }
    
      var dateUpdateTimer = setInterval(()=>{
          onSetClock();
        }, 60000 )
      
  
      return function cleanup() {
          clearInterval(dateUpdateTimer)
      }
    }, []);
  
  
  
    return (
      <div className="header-clock-div">
        <span className="date-div"> {clockData.day} </span>
        <span className="time-div"> {clockData.time} </span>
      </div>
    )
  }
  



  export default HeaderClock;