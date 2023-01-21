import React, { ChangeEvent, useEffect, useState } from 'react';
import './App.css';
import { Chart as ChartJS, LineElement, CategoryScale, LinearScale, PointElement, Legend } from "chart.js";
import { Line } from "react-chartjs-2";
import { Api } from './api';


ChartJS.register(LineElement, CategoryScale, LinearScale, PointElement, Legend);




function App() {

  const [response, setResponse] = useState({
    "pnl": [{ "x": 0, "y": 0 }],
    "index_pnl": [{ "x": 0, "y": 0 }],
    "pnl_percent": [{ "x": 0, "y": 0 }],
    "date_from": "",
    "date_to": ""
  });
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

  useEffect(() => {
    if(startDate === "" && endDate === "") {
      Api.getData().then((res) => {
        setResponse({ ...res.data })
      })
    }
  }, [])

  useEffect(() => {
    let unixStartDate = Date.parse(startDate);
    let unixEndDate = Date.parse(endDate);
    if(startDate !== "" && endDate !== "" && startDate < endDate) {
      Api.getTimeData(unixStartDate, unixEndDate).then((res) => {
        setResponse({ ...res.data })
      })
    }
  }, [startDate, endDate])

  const data = {
    labels: response.pnl.map(el => {
      var a = new Date(el.x);
      var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      var year = a.getFullYear();
      var month = months[a.getMonth()];
      var date = a.getDate();
      var hour = a.getHours();
      var min = a.getMinutes();
      var sec = a.getSeconds().toString();
      if (sec.length === 1) sec = "0" + sec;
      var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
      return time;
    }),
    datasets: [{
      label: "P&L",
      data: response.pnl.map(el => el.y),
      backgroundColor: 'coral',
      borderColor: 'coral',
      pointBorderColor: 'coral',
      tension: 0.3
    }]
  }
  const data2 = {
    labels: response.pnl.map(el => {
      var a = new Date(el.x);
      var months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      var year = a.getFullYear();
      var month = months[a.getMonth()];
      var date = a.getDate();
      var hour = a.getHours();
      var min = a.getMinutes();
      var sec = a.getSeconds().toString();
      if (sec.length === 1) sec = "0" + sec;
      var time = date + ' ' + month + ' ' + year + ' ' + hour + ':' + min + ':' + sec;
      return time;
    }),
    datasets: [
      {
        label: "P&L %",
        data: response.pnl_percent.map(el => el.y),
        backgroundColor: 'purple',
        borderColor: 'purple',
        pointBorderColor: 'purple',
        tension: 0.3
      },
      {
        label: "P&L Index",
        data: response.index_pnl.map(el => el.y),
        backgroundColor: 'green',
        borderColor: 'green',
        pointBorderColor: 'green',
        tension: 0.3
      }]
  }


  return (
    <div className="App">
      <div className='TimeSelect'>
        <div className='DateFrom'>
          <h2>С</h2>
          <input type={'datetime-local'} onChange={(e: ChangeEvent<HTMLInputElement>) => {
            setStartDate(e.currentTarget.value)
            console.log(e.currentTarget.value);
          }}></input>
        </div>
        <div className='DateFrom'>
          <h2>ПО</h2 >
          <input type={'datetime-local'} onChange={(e: ChangeEvent<HTMLInputElement>) => {
            setEndDate(e.currentTarget.value)
            console.log(e.currentTarget.value);
          }}></input>
        </div>
      </div>
      <div className='LineChart'>
        <h1>График P&L</h1>
        <Line
          data={data}
        />
      </div>
      <div className='LineChart2'>
        <h1>Графики P&L % и Index P&L</h1>
        <Line
          data={data2}
        />
      </div>
    </div>
  );
}

export default App;
