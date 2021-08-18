









import React, { useState, useEffect, useLayoutEffect, useRef, Component } from 'react';


import {  
    VictoryChart, 
    VictoryLine, 
    VictoryScatter, 
    VictoryAxis, 
    VictoryCandlestick, 
    VictoryTheme,
    VictoryLabel,
    VictoryTooltip,
    VictoryZoomContainer,
    VictoryVoronoiContainer,
    VictoryBrushContainer,
    VictoryCursorContainer,
    createContainer,
} from 'victory';

const ChartComponent = (props) => {
    
    const RESET_TIMEOUT = 200;
    let movement_timer = null;
    const [zoomDomain, setZoomDomain] = useState({})
    const [selectedDomain, setSelectedDomain] = useState({})
    const candlesChartRef = useRef(null);
    const [chartSize, setChartSize] = useState({
        width:0,
        height:0,
    });

    useEffect(() => {

        const resizeListener = () => {
            clearInterval(movement_timer);

            movement_timer = setTimeout(()=>{

                if (candlesChartRef.current){

                    setChartSize({
                        width:candlesChartRef.current.offsetWidth,
                        height:candlesChartRef.current.offsetWidth
                    });
                }

            }, RESET_TIMEOUT);

        };

        resizeListener();
        window.addEventListener('resize', resizeListener);    
        return () => {
          window.removeEventListener('resize', resizeListener);
        }
    }, [])




    function handleZoom(domain) {        
        setSelectedDomain(domain);
    }

    function handleBrush(domain) {
        
        setZoomDomain(domain);
    }
    const VictoryZoomVoronoiContainer = createContainer("zoom", "voronoi");

    return (    
        <div className="candlestick-chart-div" ref={candlesChartRef}>
            <VictoryChart
                polar={false}
                width={chartSize.width}
                height={chartSize.height*0.40}
                scale={{x: "time"}}
                containerComponent={
                    <VictoryZoomVoronoiContainer 
                        responsive={false}
                        zoomDomain={zoomDomain}
                        onZoomDomainChange={handleZoom}
                    />
                }
            >
                <VictoryAxis tickFormat={(t) => {
                            return new Date(t).getMonth()+"/"+new Date(t).getDay()
                        }}
                    tickCount={10}
                    style={{ tickLabels: { fill: "#a7a7a7" } }}/>
                <VictoryAxis 
                        dependentAxis
                        style={{ tickLabels: { fill: "#a7a7a7" } }}/>
                <VictoryCandlestick
                    x="date"
                    candleColors={{ positive: "#30ff4f", negative: "#ff6730" }}
                    data={props.data}
                    labels={({ datum }) =>{
                        const textTip = [
                            `open: ${datum.open}`,
                            `close: ${datum.close}`,
                            `high: ${datum.high}`,
                            `low: ${datum.low}`
                        ]
                        return [...textTip, ...datum.date.split(" ")]
                    }}
                    labelComponent={<VictoryTooltip pointerLength={0}/>}
                    events={[{
                        target: "data",
                        eventHandlers: {
                            onMouseOver: () => ({
                            target: "labels", mutation: () => ({ active: true })
                            }),
                            onMouseOut: () => ({
                            target: "labels", mutation: () => ({ active: false })
                            })
                        }
                    }]}
                />
            </VictoryChart>
            <VictoryChart
                width={chartSize.width}
                height={chartSize.height*0.10}
                scale={{x: "time"}}
                padding={{top: 0, left: 50, right: 50, bottom: 30}}
                containerComponent={
                    <VictoryBrushContainer responsive={false}
                        brushDimension="x"
                        brushDomain={selectedDomain}
                        onBrushDomainChange={handleBrush}
                        brushStyle={{stroke: "transparent", fill: "white", fillOpacity: 0.2}}
                    />
                }
            >

                <VictoryAxis tickFormat={(t) => {
                                return new Date(t).getHours()+":"+new Date(t).getMinutes()
                            }}
                    tickCount={10}  
                    style={{ tickLabels: { fill: "#a7a7a7" } }}/>
                <VictoryCandlestick
                    x="date"
                    candleColors={{ positive: "#30ff4f", negative: "#ff6730" }}
                    data={props.data}
                />
            </VictoryChart>
    </div>
    );
}


export default ChartComponent;


