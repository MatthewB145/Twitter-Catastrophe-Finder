import "./StatCard.css"

export default function StatCard({disaster,count})
{
    let disasterName = disaster.charAt(0).toUpperCase() + disaster.slice(1);
    let icon = `${disasterName}.png`
    return(
        <div className="statcard" > 
            <div><img src = {icon} alt ={icon+ " logo"}></img></div>
            <h3>{count}</h3>
            <p>{disasterName}</p>
        </div>
    );
}
