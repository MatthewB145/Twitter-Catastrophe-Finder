import React, {useEffect, useRef,useState} from "react";
import {MapContainer, Marker,Popup, TileLayer} from "react-leaflet";
import HeatmapLayer from './HeatmapLayer'; 
import "leaflet/dist/leaflet.css";
import "./leaflet2.css"
import 'react-leaflet-markercluster/styles'
import MarkerClusterGroup from "react-leaflet-markercluster";
import {Icon, divIcon} from "leaflet"
import { DISASTERS } from "./data";
import MenuItem from "./MenuItem";

export default function Map({Disasters}) {
    const mapRef = useRef(null);
    let [latitude, setLatitude] = useState(35.0078);
    let [longitude, setLongitude] = useState(97.0929);
    const [isLoaded, setIsLoaded] = useState(false);
    const options = {
        enableHighAccuracy: true,
        timeout: 1000,
        maximumAge: 0,
    };
    const custumIcon = new Icon({
        iconUrl: "location-pin.png",iconSize: [38,38]
    });

    useEffect(()=> {
      function success(pos) {
          const crd = pos.coords;
           setLatitude(crd.latitude);
          setLongitude(crd.longitude);
          setIsLoaded(true);
          console.log(latitude+" "+longitude);
      }
        
      function error(err) {
          console.warn(`ERROR(${err.code}): ${err.message}`);
      }
        
      
      if ("geolocation" in navigator) {
          navigator.geolocation.getCurrentPosition(success, error, options);    
      } 

    },[]);

    if (!isLoaded) {
        return <div>Waiting For Your Location...</div>; // Show a loading message while waiting for geolocation data
    }
    
    const points = Disasters.map((d) => [d.latitude, d.longitude]); // 0.5 = intensity (0–1)

    return(
        <MapContainer center={[latitude, longitude]} zoom={10} ref={mapRef} style={{height: "750px", width: "1000px"}}>
            
            <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />

            <HeatmapLayer points={points} />
            <MarkerClusterGroup>
            {Disasters.map((disaster,index) => (    
                
                <Marker key ={index} position = {[disaster.latitude,disaster.longitude]} icon ={custumIcon}>
                    <Popup> <MenuItem name = {disaster.name} 
                                        location = {disaster.location} report = {disaster.report} date = {disaster.date} level ={disaster.disaster_level} class1 = "popup" /> </Popup>
                </Marker>
                
            ))}
            </MarkerClusterGroup>
            
        

        </MapContainer>

    );
}
