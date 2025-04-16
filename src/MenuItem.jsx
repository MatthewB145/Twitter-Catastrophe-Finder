import "./MenuItem.css"

export default function MenuItem({name,location,report,date,level,class1})
{
    let class2 = "menuitem";
    class2 = class2+" "+class1;
    return(
        <div className= {class2}> 
            <h3 >{name.charAt(0).toUpperCase() + name.slice(1)}</h3>
            <p>{report}</p>

            <div className = "tweet-info">

                <div className="tweet-location-date">
                    <p>{location} <br></br>{new Date(date).toDateString()}</p>
                    <p>{} </p>
                </div>
                {location ? <button><img src="locationpin.png" alt="location pin logo" /></button> : null}
            </div>
        </div>
    );
}
