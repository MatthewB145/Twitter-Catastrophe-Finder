import MenuItem from "./MenuItem";
import { DISASTERS } from "./data";
import React, { useState } from 'react';
import "./Menu.css"

export default function Menu() {
    const [currentIndex, setCurrentIndex] = useState(0); // Track the start index of the current 5 tweets
    
    const showDistasters = DISASTERS.slice(currentIndex, currentIndex + 5); 
    function handleNext() {
            setCurrentIndex((index) => (index+5) <DISASTERS.length? index + 5:index=0); // Move to the next set of 5 tweets
            
    
        
    };

    const handlePrevious = () => {
        setCurrentIndex((index) => (index-5) >=0? index - 5:index=DISASTERS.length-5);
    };


    return(
        
        <div className = "menu">
           
            <ul>
                {showDistasters.map((disaster) => <li>
                    <MenuItem name = {disaster.name} 
                    location = {disaster.location} report = {disaster.report} date = {disaster.date} level ={disaster.disaster_level} class1 = " "/>
                    
                    </li>)
                } 
            </ul>
            <div class="prev-next">
                    <button onClick = {handlePrevious} class="arrowbutton" id="prevBtn"> <img class="arrows" src = "arrow-back.svg" alt = "previous location"></img> </button>
                    <button onClick={handleNext} class="arrowbutton" id="nextBtn"> <img class="arrows" src = "arrow-forward.svg" alt = "next location"></img> </button>
            </div>
        </div>
    );
}