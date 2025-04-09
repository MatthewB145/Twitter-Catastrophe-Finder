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
    const [selectedDisasters, setSelectedDisasters] = useState(["Earthquake", "Fire", "Flood", "Hurricane","Tornado"]);

    const handleFilterChange = (disasterType) => {
        setSelectedDisasters((prev) =>
        prev.includes(disasterType)
            ? prev.filter((d) => d !== disasterType)
            : [...prev, disasterType]
        );
        
    };
    
    const filteredData= selectedDisasters.length
    ? disasterData.filter((disaster) => selectedDisasters.includes(disaster.name))
    : DISASTERS;

    return(
        
        
        <div className='Map-Menu-Container'>
            <h1 className="heading">Disaster Alerts & Reports</h1>
           <StatDash data = {disasterData}></StatDash>
           <SelectionMenu selectedDisasters={selectedDisasters} onFilterChange={handleFilterChange}></SelectionMenu>
            <div className='Map-Menu-Wrapper'>
                <Menu disasters = {filteredData}/>
                <div className="Map-Graph-Contain">
                    <Map Disasters ={filteredData}/>
                    <SignificantEvent data = {disasterData}></SignificantEvent>
                </div>
                
                
            </div>
        </div>
    );
}