export default function HealthGauge({score=0}) {
  const s=Math.max(0,Math.min(100,Number(score)||0));
  const label=s>=85?'Excellent':s>=70?'Good':s>=50?'Fair':'Needs work';
  return <section className="panel health"><div className="heading"><span>Repository health</span><h2>Engineering health</h2></div>
    <div className="gauge" style={{'--score':`${s*3.6}deg`}}><div><strong>{s}</strong><small>/ 100</small></div></div>
    <b className="health-label">{label}</b><p className="muted center">Maintainability, structure, testing, and risk signals.</p></section>;
}
