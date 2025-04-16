import Map from "./Map";
import Menu from "./Menu";
import StatCard from "./StatCard";
import React, { useState } from 'react';
import "./Interactive-Map.css"
import Graph from "./Graph";
import StatDash from "./StatDash";
import SelectionMenu from "./SelectionMenu";
import { DISASTERS } from "./data";
import SignificantEvent from "./SignificantEvent";

export default function InteractiveMap({disasterData}) {
    const [selectedDisasters, setSelectedDisasters] = useState(["earthquake", "fire", "flood", "Hurricane","Tornado"]);

    const handleFilterChange = (disasterType) => {
        setSelectedDisasters((prev) =>
        prev.includes(disasterType)
            ? prev.filter((d) => d !== disasterType)
            : [...prev, disasterType]
        );
        
    };
    
    const filteredData= selectedDisasters.length? disasterData.filter((disaster) => selectedDisasters.includes(disaster.name)): disasterData;
    const pins = filteredData.filter((item) => item.location !== "");

    return(
        
        
        <div className='Map-Menu-Container'>
            <h1 className="heading">Disaster Alerts & Reports</h1>
           <StatDash data = {filteredData}></StatDash>
           <SelectionMenu selectedDisasters={selectedDisasters} onFilterChange={handleFilterChange}></SelectionMenu>
            <div className='Map-Menu-Wrapper'>
            
                <Menu disasters = {filteredData}/>
                <div className="Map-Graph-Contain">
                    <Map Disasters ={pins}/>
                    <Graph data = {disasterData}></Graph>
                </div>
                
            </div>
            <SignificantEvent data = {filteredData}></SignificantEvent>
        </div>
    );
}
