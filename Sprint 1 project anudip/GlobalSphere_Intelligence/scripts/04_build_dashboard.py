from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
R=Path(__file__).resolve().parents[1]; f=R/"data"/"global_population_clean.csv"
if not f.exists(): f=R/"data"/"population_demo.csv"
d=pd.read_csv(f); y=int(d.year.max()); q=d[d.year==y]; t=d.groupby("year",as_index=False).population.sum()
top=q.nlargest(10,"population").sort_values("population"); reg=q.groupby("region",as_index=False).population.sum().sort_values("population",ascending=False)
urban=q.dropna(subset=["urban_population_pct"]).nlargest(8,"urban_population_pct")
fig=make_subplots(rows=2,cols=2,subplot_titles=("Population trend","Top 10 countries","Population by region","Urban population share"),specs=[[{"type":"scatter"},{"type":"bar"}],[{"type":"bar"},{"type":"pie"}]])
fig.add_trace(go.Scatter(x=t.year,y=t.population/1e9,mode="lines+markers",line=dict(color="#38bdf8",width=4),fill="tozeroy",name="Population (B)"),1,1)
fig.add_trace(go.Bar(x=top.population/1e6,y=top.country,orientation="h",marker=dict(color=top.population,colorscale="Teal"),name="Population (M)"),1,2)
fig.add_trace(go.Bar(x=reg.region,y=reg.population/1e9,marker=dict(color=reg.population,colorscale="Viridis"),name="Population (B)"),2,1)
fig.add_trace(go.Pie(labels=urban.country,values=urban.urban_population_pct,hole=.58),2,2)
fig.update_layout(height=850,paper_bgcolor="#0b1220",plot_bgcolor="#111c2e",font=dict(color="#e5edf8"),margin=dict(l=35,r=35,t=55,b=45),legend=dict(orientation="h",y=-.08))
fig.update_xaxes(gridcolor="#26364d"); fig.update_yaxes(gridcolor="#26364d")
plot=fig.to_html(full_html=False,include_plotlyjs="cdn",config={"responsive":True})
head="""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GlobalSphere Intelligence</title><style>
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 12% 0%,#17345a,#080f1c 48%);color:#edf5ff;font:15px Segoe UI,Arial}
.wrap{max-width:1450px;margin:auto;padding:28px}header{display:flex;justify-content:space-between;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:24px}
.brand{display:flex;gap:14px;align-items:center}.logo{width:54px;height:54px;border-radius:16px;background:linear-gradient(135deg,#06b6d4,#4f46e5);display:grid;place-items:center;font-size:30px}
h1{font-size:clamp(22px,3vw,32px);margin:0}.sub{color:#91a4bd;margin-top:5px}.tag{border:1px solid #1e8b85;color:#5eead4;background:#0d94881c;border-radius:25px;padding:9px 14px;font-size:12px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:15px;margin-bottom:18px}.card{background:linear-gradient(145deg,#142238,#0f1929);border:1px solid #263952;border-radius:17px;padding:20px;box-shadow:0 12px 35px #0003}
.label{font-size:12px;color:#91a4bd;text-transform:uppercase;letter-spacing:.08em}.value{font-size:clamp(24px,3vw,35px);font-weight:750;margin:12px 0 5px}.hint{font-size:12px;color:#5eead4}
.chart{padding:10px 14px;overflow:hidden}.note{color:#91a4bd;font-size:12px;line-height:1.6;margin:16px 2px}
@media(max-width:800px){.kpis{grid-template-columns:repeat(2,1fr)}}@media(max-width:480px){.wrap{padding:14px}.card{padding:13px}}</style></head><body><main class="wrap">"""
body=f"""<header><div class="brand"><div class="logo">◎</div><div><h1>GlobalSphere Intelligence</h1><div class="sub">Advanced Global Population Analytics &amp; Decision Intelligence</div></div></div><div class="tag">● ANALYTICS OVERVIEW</div></header>
<section class="kpis">
<div class="card"><div class="label">Population in dataset</div><div class="value">{q.population.sum()/1e9:.2f}B</div><div class="hint">Latest year: {y}</div></div>
<div class="card"><div class="label">Countries covered</div><div class="value">{q.country.nunique()}</div><div class="hint">With available observations</div></div>
<div class="card"><div class="label">Mean growth rate</div><div class="value">{q.population_growth_pct.mean():.2f}%</div><div class="hint">Average available country value</div></div>
<div class="card"><div class="label">Years covered</div><div class="value">{d.year.min()}–{d.year.max()}</div><div class="hint">Historical data window</div></div></section><section class="card chart">"""
tail="""</section><div class="note">World Bank source when using global_population_clean.csv. KPI totals include only countries in the selected dataset and may not equal the full world population. Charts support hover, zoom and legend filtering.</div></main></body></html>"""
out=R/"outputs"/"GlobalSphere_Dashboard.html"; out.parent.mkdir(exist_ok=True); out.write_text(head+body+plot+tail,encoding="utf-8"); print("Created",out)