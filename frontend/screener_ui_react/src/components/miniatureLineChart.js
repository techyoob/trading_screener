


import React, { useRef, useState, useEffect } from 'react';

import './index.css';

import {  VictoryChart, VictoryLine, VictoryScatter, VictoryAxis } from 'victory';


function MiniLineChart(props) {

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



    useEffect(() => {
    }, [props.data]);
    

  return (
    <div id="container" className="mini-line-chart" ref={containerRef}>
        <VictoryChart polar={false} height={chartView.height*4} width={chartView.width*4}>
            <VictoryLine
                data={props.data}
                x="date"
                y="price"
            />
            <VictoryAxis style={{ axis: {stroke: "none"} }} tickFormat={() => ''}/>
        </VictoryChart>
    </div>);
}

export default MiniLineChart;





