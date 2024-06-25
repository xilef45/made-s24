import sqlite3
import datetime
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import numpy as np

conn = sqlite3.connect("../data/data.sqlite")
cursor = conn.cursor()

cursor.execute("Select * from emissions;")
sql_result_emmissions = cursor.fetchall()

current_year = datetime.datetime.now().year
avg_year_parts = []
for year in range(1990, current_year + 1):
    avg_year_parts.append(f"AVG(\"{year}\")")
avg_year_query_part = ", ".join(avg_year_parts)
select_statement = f"\"Jurisdiction Covered\", Region, \"Start Date\", {avg_year_query_part}"
sql_query = f"SELECT {select_statement} FROM carbonprice GROUP BY \"Jurisdiction Covered\";"
cursor.execute(sql_query)
sql_result_carbonprice = cursor.fetchall()
conn.close()

# Match the jurisdictions in both tables
emmissions_jurisdictions = set([row[1] for row in sql_result_emmissions])
carbonprice_jurisdictions = set([row[0] for row in sql_result_carbonprice])
common_jurisdictions = emmissions_jurisdictions.intersection(carbonprice_jurisdictions)

result_emmissions = [row for row in sql_result_emmissions if row[1] in common_jurisdictions]
result_carbonprice = [row for row in sql_result_carbonprice if row[0] in common_jurisdictions]

# Merge the two tables
merged_data = []
for jurisdiction in common_jurisdictions:
    jurisdiction_emissions = [row for row in result_emmissions if row[1] == jurisdiction]
    jurisdiction_carbonprice = [row for row in result_carbonprice if row[0] == jurisdiction]
    emissions_data_juri = jurisdiction_emissions[0]
    carbonprice_data_juri = jurisdiction_carbonprice[0]
    merged_data_perCountry = []
    for year_index, year in enumerate(range(1990, current_year + 1)):
        emissions_index = year - 1970 + 2
        carbonprice_index = year_index + 4

        result_value = (jurisdiction, year,
                        emissions_data_juri[emissions_index] if emissions_index < len(emissions_data_juri) else None,
                        carbonprice_data_juri[carbonprice_index] if carbonprice_index < len(
                            carbonprice_data_juri) else None)
        merged_data_perCountry.append(result_value)
    merged_data.append(merged_data_perCountry)

merged_data = [[entry for entry in country_data if entry[2] is not None and entry[3] is not None] for country_data in
               merged_data]
merged_data = [country_data for country_data in merged_data if len(country_data) >= 1]

# Analyse the data
pearsonr_results = []
for country_data in merged_data:
    emissions = [row[2] for row in country_data]
    carbon_prices = [row[3] for row in country_data]
    if len(emissions) < 2 or len(carbon_prices) < 2:
        continue
    correlation_coefficient, p_value = pearsonr(emissions, carbon_prices)

    pearsonr_results.append((country_data[0][0], correlation_coefficient, p_value))

# Interpret the results
max_correlation_coefficient = max([row[1] for row in pearsonr_results])
min_correlation_coefficient = min([row[1] for row in pearsonr_results])
avg_correlation_coefficient = np.mean([row[1] for row in pearsonr_results])
std_correlation_coefficient = np.std([row[1] for row in pearsonr_results])

max_p_value = max([row[2] for row in pearsonr_results])
min_p_value = min([row[2] for row in pearsonr_results])
avg_p_value = np.mean([row[2] for row in pearsonr_results])
std_p_value = np.std([row[2] for row in pearsonr_results])

# draw a plot of the results
plt.scatter([row[1] for row in pearsonr_results], [row[2] for row in pearsonr_results])
plt.xlabel("correlation coefficient")
plt.ylabel("p-value")
plt.title("Analyse of the correlation between emissions and carbon prices")
plt.savefig('visualization/correlationScatter.png')
plt.show()


# draw a plot of the top ten emissions countries with carbon prices
emissions_sum = []
for row in result_emmissions:
    emissions_sum.append((row[1], sum(row[2:])))
latest_emissions_per_country = {}
sorted_emissions = sorted(emissions_sum, key=lambda x: x[1], reverse=True)
top_ten_emitting_countries = sorted_emissions[:10]
top_ten_emitting_countries_carbonPrice = []
top_ten_emitting_countries_emissions = []
for country in top_ten_emitting_countries:
    for row in result_carbonprice:
        if row[0] == country[0]:
            top_ten_emitting_countries_carbonPrice.append(row)
            break
    for row in result_emmissions:
        if row[1] == country[0]:
            top_ten_emitting_countries_emissions.append(row)
            break


years = list(range(1970, 2022))
for row in top_ten_emitting_countries_emissions:
    plt.plot(years, row[3:], label=row[1])
plt.title('Total Emissions of the top-ten emitting \n Jurisdictions with carbon price')
plt.xlabel('Year')
plt.ylabel('Total Emissions')
plt.legend(title='Jurisdiction', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualization/emissions-top10.png')
plt.show()

years = list(range(1990, current_year))
for row in top_ten_emitting_countries_carbonPrice:
    plt.plot(years, row[4:], label=row[0])
plt.title('Average Carbon Price of the top-ten emitting \n Jurisdictions with carbon price')
plt.xlabel('Year')
plt.ylabel('Carbon Price')
plt.legend(title='Jurisdiction', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('visualization/carbonprice-top10.png')
plt.show()
