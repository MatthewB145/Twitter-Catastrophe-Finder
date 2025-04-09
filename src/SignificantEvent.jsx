import "./SignificantEvent.css"

export default function SignificantEvent({data})
{
    const date = new Date().toISOString().slice(0, 7); // "YYYY-MM"
    const disastersToday = data.filter((disaster)=> disaster.date.slice(0,7) == date);

    const countOccurrences = (arr) => {
        const map = new Map();
        arr.forEach(item => map.set(item.name, (map.get(item.name) || 0) + 1));
        return Object.fromEntries(map);
      };    
    const DisasterCounts  = countOccurrences(disastersToday);
    let maxKey = '';
    let maxValue = 0; 

    // Loop through object entries
    for (const [key, value] of Object.entries(DisasterCounts)) {
        if (value > maxValue) {
            maxValue = value;
            maxKey = key;
        }
    }
    
    return(
       <div className="disaster-alert">
        <h3>{new Date(date + "-01").toLocaleString("en-US",{month: "long"})} Disaster Report: </h3>
        <p>{maxValue} {maxKey}s have impacted the United States this month. Filter by {maxKey} to explore discussions and see affected areas.</p>
       </div>
    );
}