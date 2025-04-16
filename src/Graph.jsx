import React from "react";
import { LineChart, Legend, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Line} from "recharts";
import "./graph.css"; // Import CSS file


export default function Graph({data}){
  const disasterData = data;
  const today = new Date();
  const todayYear = today.getFullYear();
  const todayMonth = today.getMonth();
  const todayDate = today.getDate();

  const todaysData = disasterData.filter((report) => {
    const reportDate = new Date(report.date);
    return(
      reportDate.getFullYear() === todayYear &&
      reportDate.getMonth() === todayMonth &&
      reportDate.getDate() === todayDate
    )
  })


  const hourCounts = todaysData.reduce((acc, report) => {
    const date = new Date(report.date);
    const hour = date.getHours();
      const hourKey = `${hour.toString().padStart(2, "0")}:00`;
      acc[hourKey] = (acc[hourKey] || 0) + 1;
      return acc;
    }, {});

    const fullDayData = Array.from({ length: 24 }, (_, i) => {
      const hour = `${i.toString().padStart(2, "0")}:00`;
      return {
        hour,
        count: hourCounts[hour] || 0
      };
    });
  return (
    <div className="graph-container">
      <h2 className="graph-title">Today's Disaster Reports by Hour</h2>
      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={fullDayData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="hour" label={{ value: "Hour of the Day", position: "insideBottomLeft", offset: -10}} />
          <YAxis label={{value: "Number of Reports", position: 'insideLeft', angle: -90}} />
          <Tooltip  />
          <Legend />
          <Line type="monotone" dataKey="count" stroke="#000000" strokeWidth={2} dot = {{r: 4 }}/>
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
