from pathlib import Path
import requests, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"data"/"global_population_clean.csv"
IND={"population":"SP.POP.TOTL","population_growth_pct":"SP.POP.GROW","population_density_km2":"EN.POP.DNST","urban_population":"SP.URB.TOTL","rural_population":"SP.RUR.TOTL"}
def get(code):
 u=f"https://api.worldbank.org/v2/country/all/indicator/{code}"
 r=requests.get(u,params={"format":"json","per_page":20000,"date":"2015:2024"},timeout=90); r.raise_for_status(); j=r.json()
 if len(j)<2 or j[1] is None: raise RuntimeError("No data for "+code)
 return pd.DataFrame([{"iso3":x["countryiso3code"],"country":x["country"]["value"],"year":int(x["date"]),code:x["value"]} for x in j[1] if x.get("countryiso3code") and len(x["countryiso3code"])==3 and x.get("value") is not None])
def main():
 fs=[]
 for n,code in IND.items(): print("Fetching",n); fs.append(get(code).rename(columns={code:n}))
 df=fs[0]
 for f in fs[1:]: df=df.merge(f.drop(columns="country"),on=["iso3","year"],how="left")
 r=requests.get("https://api.worldbank.org/v2/country?format=json&per_page=400",timeout=60); r.raise_for_status()
 meta=[]
 for x in r.json()[1]:
  region=(x.get("region") or {}).get("value"); iso=x.get("id")
  if iso and len(iso)==3 and region and region!="Aggregates": meta.append({"iso3":iso,"region":region})
 df=df.merge(pd.DataFrame(meta),on="iso3",how="inner").dropna(subset=["population"])
 df["urban_population_pct"]=(df.urban_population/df.population*100).round(2)
 df["rural_population_pct"]=(df.rural_population/df.population*100).round(2)
 df["population"]=df.population.round().astype("int64")
 df.sort_values(["country","year"]).to_csv(OUT,index=False); print("Saved",len(df),"rows:",OUT)
if __name__=="__main__": main()