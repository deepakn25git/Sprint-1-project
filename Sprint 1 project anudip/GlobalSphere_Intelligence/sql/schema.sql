CREATE DATABASE IF NOT EXISTS globalsphere; USE globalsphere;
CREATE TABLE IF NOT EXISTS population(iso3 CHAR(3) NOT NULL,country VARCHAR(120) NOT NULL,region VARCHAR(100),year SMALLINT NOT NULL,population BIGINT,population_growth_pct DECIMAL(8,4),population_density_km2 DECIMAL(12,4),urban_population BIGINT,rural_population BIGINT,urban_population_pct DECIMAL(8,2),rural_population_pct DECIMAL(8,2),PRIMARY KEY(iso3,year),INDEX idx_year(year),INDEX idx_region(region));
SELECT year,SUM(population) AS population_total FROM population GROUP BY year ORDER BY year;
SELECT country,population FROM population WHERE year=(SELECT MAX(year) FROM population) ORDER BY population DESC LIMIT 10;
