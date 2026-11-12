from pathlib import Path
import os,pandas as pd,mysql.connector
from dotenv import load_dotenv
R=Path(__file__).resolve().parents[1]; load_dotenv(R/".env"); f=R/"data"/"global_population_clean.csv"
if not f.exists(): raise FileNotFoundError("Run 01_fetch_clean.py first")
db=os.getenv("MYSQL_DATABASE","globalsphere")
cn=mysql.connector.connect(host=os.getenv("MYSQL_HOST","localhost"),port=int(os.getenv("MYSQL_PORT","3306")),user=os.getenv("MYSQL_USER","root"),password=os.getenv("MYSQL_PASSWORD",""))
cur=cn.cursor(); cur.execute(f"CREATE DATABASE IF NOT EXISTS `{db}`"); cur.execute(f"USE `{db}`")
cur.execute("""CREATE TABLE IF NOT EXISTS population(iso3 CHAR(3),country VARCHAR(120),region VARCHAR(100),year SMALLINT,population BIGINT,population_growth_pct DECIMAL(8,4),population_density_km2 DECIMAL(12,4),urban_population BIGINT,rural_population BIGINT,urban_population_pct DECIMAL(8,2),rural_population_pct DECIMAL(8,2),PRIMARY KEY(iso3,year),INDEX idx_year(year),INDEX idx_region(region))""")
cols=["iso3","country","region","year","population","population_growth_pct","population_density_km2","urban_population","rural_population","urban_population_pct","rural_population_pct"]
d=pd.read_csv(f)[cols].astype(object); d=d.where(pd.notna(d),None)
sql=f"INSERT INTO population ({','.join(cols)}) VALUES ({','.join(['%s']*len(cols))}) ON DUPLICATE KEY UPDATE "+",".join(f"{x}=VALUES({x})" for x in cols[1:])
cur.executemany(sql,list(d.itertuples(index=False,name=None))); cn.commit(); cur.execute("SELECT COUNT(*) FROM population"); print("Rows loaded:",cur.fetchone()[0]); cur.close(); cn.close()