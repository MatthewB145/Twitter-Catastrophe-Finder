import MenuItem from "./MenuItem";
import { DISASTERS } from "./data";
import React, { useState } from 'react';
import "./Menu.css"

export default function Menu({disasters}) {
    return(
        
        <div className = "menu">
           
            <ul>
                {disasters.map((disaster) => <li>
                    <MenuItem name = {disaster.name} 
                    location = {disaster.location} report = {disaster.report} date = {disaster.date} level ={disaster.disaster_level} class1 = " "/>
                    
                    </li>)
                } 
            </ul>
        </div>
    );
}