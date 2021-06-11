


import React, { useState, useEffect, useRef } from 'react';
import './testPage.css';
import { 
    FaSearch,
    FaCaretDown,
    FaCaretUp,
    FaAngleLeft,
    FaAngleRight
} from 'react-icons/fa';


import Spinner from "react-svg-spinner";
import * as d3 from 'd3';
import ChartTest from './chartTest'


import './index.css';


import MiniLineChart from '../../components/miniatureLineChart'
import {  VictoryChart, VictoryLine, VictoryScatter, VictoryAxis } from 'victory';



const datas = [
  {
      time:"",
      price:95
  },
  {
      time:"",
      price:80
  },
  {
      time:"",
      price:45
  },
  {
      time:"",
      price:85
  },
  {
      time:"",
      price:95
  },
  {
      time:"",
      price:95
  },
  {
      time:"",
      price:95
  }
]


const TestPage = (props) => {

  const [data, setData] = useState([]);

  useEffect(() => {
    regenerateData();
  }, []);

  function regenerateData() {
    const chartData = [];
    for (let i = 0; i < 20; i++) {
      const value = Math.floor(Math.random() * i + 3);
      chartData.push({
        label: i,
        value,
      });
    }
    setData(chartData)
  }

  const datat = [
    {date: '2019-12-10', volume: 16197},
    {date: '2019-12-9', volume: 32010},
    {date: '2019-12-8', volume: 26518},
    {date: '2019-12-7', volume: 18606},
    {date: '2019-12-6', volume: 16795},
    {date: '2019-12-5', volume: 28607},
    {date: '2019-12-4', volume: 23621}
  ];


  return (
    <div className="test-view">
      <button onClick={regenerateData}>Change Data</button>
    </div>
  );

}




export default TestPage;




function LineChart(props) {
  const { data, width, height } = props;

  useEffect(() => {
    drawChart();
  }, [data]);
  
  function drawChart() {
    // Add logic to draw the chart here


    const margin = { top: 50, right: 50, bottom: 50, left: 50 };
    const yMinValue = d3.min(data, d => d.value);
    const yMaxValue = d3.max(data, d => d.value);
    const xMinValue = d3.min(data, d => d.label);
    const xMaxValue = d3.max(data, d => d.label);

    d3.select('#container')
      .select('svg')
      .remove();
    d3.select('#container')
      .select('.tooltip')
      .remove();


    const svg = d3
      .select('#container')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    const xScale = d3
        .scaleLinear()
        .domain([xMinValue, xMaxValue])
        .range([0, width]);
    const yScale = d3
        .scaleLinear()
        .range([height, 0])
        .domain([0, yMaxValue]);
    const line = d3
        .line()
        .x(d => xScale(d.label))
        .y(d => yScale(d.value))    
        .curve(d3.curveMonotoneX);



    // svg
    //     .append('g')
    //     .attr('class', 'grid')
    //     .attr('transform', `translate(0,${height})`)
    //     .call(
    //     d3.axisBottom(xScale)
    //         .tickSize(-height)
    //         .tickFormat(''),
    //     );
    // svg
    //     .append('g')
    //     .attr('class', 'grid')
    //     .call(
    //         d3.axisLeft(yScale)
    //         .tickSize(-width)
    //         .tickFormat(''),
    //     );
    // svg
    //     .append('g')
    //     .attr('class', 'x-axis')
    //     .attr('transform', `translate(0,${height})`)
    //     .call(d3.axisBottom().scale(xScale).tickSize(15));
    // svg
    //     .append('g')
    //     .attr('class', 'y-axis')
    //     .call(d3.axisLeft(yScale));
    svg
        .append('path')
        .datum(data)
        .attr('fill', 'none')
        .attr('stroke', '#f6c3d0')
        .attr('stroke-width', 4)
        .attr('class', 'line') 
        .attr('d', line);




    const focus = svg
        .append('g')
        .attr('class', 'focus')
        .style('display', 'none');
    focus.append('circle').attr('r', 5).attr('class', 'circle');
    const tooltip = d3
        .select('#container')
        .append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0);



  }
  return <div id="container" />;
}
