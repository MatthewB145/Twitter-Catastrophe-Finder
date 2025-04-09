import "./StatCard.css"

export default function StatCard({disaster,count})
{
    
    let icon = `${disaster}.png`
    return(
        <div className="statcard" > 
            <div><img src = {icon} alt ={icon+ " logo"}></img></div>
            <h3>{count}</h3>
            <p>{disaster}</p>
        </div>
    );
}