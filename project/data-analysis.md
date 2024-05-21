# Analysis of the datasets 

## Datasource1: World Bank's Carbon Pricing Dashboard
File: `data-latest.xlsx`

Sheet: `Compliance_Price`

The first row must be deleted because of modification timestamp.

Some cells are empty, thats because not every country has a carbon pricing policy. These rows mustn't be deleted.

For the analysis, the following columns are relevant:
- Jurisdiction Covered
- Income group
- Start date
- Price rate label
- Metric
- 1990

...
- 2024





## Datasource2: Emissions Database for Global Atmospheric Research: Greenhouse Gas emissions of all world countries
File: `EDGARv8.0_FT2022_GHG_booklet_2023.xlsx`

Sheet: `GHG_totals_by_country`

The last two rows contain sums of `EU27` and `GLOBAL TOTAL`


For the analysis, the following columns are relevant:
- Country
- 1970

...

- 2022