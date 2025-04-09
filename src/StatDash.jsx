import StatCard from "./StatCard";
import "./StatDash.css"

export default function StatDash({data})
{
    const disasters =["Earthquake","Fire","Flood","Hurricane","Tornado"]
    
    return(
        <div className="statdash" > 
            {disasters.map((disaster1) =>
                <StatCard disaster={disaster1} count ={data.filter((disaster) => disaster.name == disaster1).length}></StatCard>
            )}
        </div>
    );
}