import React from "react";
import { BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, ResponsiveContainer, Cell, Text } from "recharts";
import "./graph.css"; // Import CSS file

const data = [
  { name: "Fire", value: 1020, color: "#1E5BFF" },
  { name: "Earthquake", value: 984, color: "#FF7F24" },
  { name: "Hurricane", value: 759, color: "#8A2BE2" },
  { name: "Tsunami", value: 1306, color: "#3D0C18" },
  { name: "Tornado", value: 834, color: "#B33A2B" }
];

const CustomLabel = ({ x, y, value

 }) => {
  return (
    <Text x={x + 25} y={y - 10} fill="#000" textAnchor="middle" fontSize={14} fontWeight="bold">
      {value}
    </Text>
  );
};

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip">
        <p>{`${payload[0].name}: ${payload[0].value}`}</p>
      </div>
    );
  }
  return null;
};

const Graph = () => {
  return (
    <div className="graph-container">
      <h2 className="graph-title">Disaster Reports</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip content={<CustomTooltip />} />
          <Bar dataKey="value" barSize={50} label={<CustomLabel />}>
          
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default Graph;