
import React, { useState } from 'react';
import "./SelectionMenu.css"

export default function SelectionMenu({selectedDisasters,onFilterChange}) {
    const disasterTypes = ["Earthquake", "Fire", "Flood", "Hurricane","Tornado"];
    

    return(
        
        <div className = "selection-menu">
            <h3>Filter by Disaster Type:   </h3>
            <ul>
               { disasterTypes.map((type)=> (
                    <div className = "filter-item">
                        <input type = "checkbox" checked ={selectedDisasters.includes(type)} onChange={()=> onFilterChange(type)} value="Submit"></input>   
                        <p>{type}</p>
                        
                       
                    </div>

               ))

               }
            </ul>
        </div>
    );
}