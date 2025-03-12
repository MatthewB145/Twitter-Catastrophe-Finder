import Map from "./Map";
import Menu from "./Menu";
import Graph from "./Graph";
import React, { useState } from 'react';
import "./Interactive-Map.css"

export default function InteractiveMap() {
  

    return(
        
        
        <div className='Map-Menu-Container'>
            
            <h2 className = "title">Disaster Alerts & Reports</h2>
            <div className='Map-Menu-Wrapper'>
                <Menu/>
                <div className='Graph-Container'>
                    <Map/>
                    <Graph/>
                    
                </div>
            </div>

            

        </div>
        
    );
}