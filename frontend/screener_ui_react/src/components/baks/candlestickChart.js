


import React, { useRef, useState, useEffect } from 'react';

import './index.css';

import {  
    VictoryChart, 
    VictoryLine, 
    VictoryScatter, 
    VictoryAxis, 
    VictoryCandlestick, 
    VictoryTheme,
    VictoryLabel,
    VictoryTooltip
} from 'victory';


function CandlestickChart(props) {

    const containerRef = useRef(null);

    const [chartView, setChartView] = useState ({width:0, height:0})
    const [data, setData] = useState (props.data)

    useEffect( () => {

        if(containerRef.current){

            setChartView({
                height: containerRef.current.offsetHeight,
                width: containerRef.current.offsetWidth
            })
        }
    }, [containerRef]);

// TODO:
//  use this example to build candlestick zoomable chart
//  LINK: https://codesandbox.io/s/kind-paper-trk8u?from-embed=&file=/src/index.js


  return (
    <div className="candlestick-chart-div" ref={containerRef}>
        
        <VictoryChart polar={false}
                    height={chartView.height}
                    width={chartView.width}
                    scale={{ x: "time" }}
                    theme={VictoryTheme.material}>
            <VictoryAxis tickFormat={(t) => {
                            return new Date(t).getHours()+":"+new Date(t).getMinutes()
                        }}
                    tickCount={10}/>
            <VictoryAxis dependentAxis/>
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
    </div>);
}

export default CandlestickChart;





