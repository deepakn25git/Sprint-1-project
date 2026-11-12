from pathlib import Path
import pandas as pd, matplotlib.pyplot as plt, seaborn as sns
R=Path(__file__).resolve().parents[1]; f=R/"data"/"global_population_clean.csv"
if not f.exists(): f=R/"data"/"population_demo.csv"
d=pd.read_csv(f); y=int(d.year.max()); q=d[d.year==y]; o=R/"outputs"; o.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid",palette="viridis")
for name, data, x, yy, title in [
("top_10_countries.png",q.nlargest(10,"population").sort_values("population"),"population","country",f"Top 10 Countries ({y})"),
("regional_population.png",q.groupby("region",as_index=False).population.sum().sort_values("population"),"population","region",f"Population by Region ({y})")]:
 plt.figure(figsize=(12,7)); sns.barplot(data=data,x=x,y=yy); plt.title(title,weight="bold"); plt.tight_layout(); plt.savefig(o/name,dpi=220); plt.close()
t=d.groupby("year",as_index=False).population.sum()
plt.figure(figsize=(12,6)); sns.lineplot(data=t,x="year",y="population",marker="o",linewidth=3); plt.title("Population Trend"); plt.tight_layout(); plt.savefig(o/"population_trend.png",dpi=220); plt.close()
print("Year:",y,"Countries:",q.country.nunique(),"Population in coverage:",f"{q.population.sum():,}")