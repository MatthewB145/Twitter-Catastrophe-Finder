import Map from "./Map";
import Menu from "./Menu";
import React, { useState } from 'react';
import "./Interactive-Map.css"

export default function InteractiveMap() {
  

    return(
        
        
        <div className='Map-Menu-Container'>
            
            <h2 className = "title">Disaster Alerts & Reports</h2>
            <div className='Map-Menu-Wrapper'>
                <Menu/>
                <Map/>
            </div>
        </div>
    );
}