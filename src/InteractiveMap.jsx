import Map from "./Map";
import Menu from "./Menu";
import React, { useState } from 'react';
import "./Interactive-Map.css"
import Graph from "./Graph";

export default function InteractiveMap() {
  

    return(
        
        
        <div className='Map-Menu-Container'>
            
            
            <div className='Map-Menu-Wrapper'>
                <Menu/>
                <div className="Map-Graph-Contain">
                    <Graph/>
                    <Map/>
                </div>
                
            </div>
        </div>
    );
}