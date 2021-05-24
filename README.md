# <p align="center"> :swimmer: PoolFlow&Skarkify :snowboarder: </p>
# <p align="center">Data challenges of an imaginary airport retail company </p>
This repository contains my **capstone project** implementation for Udacity's **Data Engineering Nano-Degree** (DEND).

During this online course I learned about various data engineering topics such as relational and NoSQL data modeling, data warehousing, data lakes and data pipelines, and gained hands-on experience with their application through different projects. I got especially interested in **Apache Spark** and what it brings to the table in terms of big data processing, and decided to utilize my capstone project to further deepen my learning about Spark.

## :mag: Project Scope
![PF_and_S_logo](https://user-images.githubusercontent.com/54779918/117148216-506e6f80-adb6-11eb-9d19-88fe9b736387.png)

**PoolFlow and Skarfify are leading airport retail chains.** PoolFlow sells swimwear while Skarfify sells scarves, mittens, and hats. As the companies grew and opened more stores, the executives of both companies realized that their businesses were heavily dependent on the season and the origin of travelers. To diversify their product portfolios and adapt better to the changing seasons, **PoolFlow and Skarfify decided to merge together**. From now on, all stores will be operated jointly under the original name PoolFlow&Skarfify and products from both companies will be sold at the shared store locations.

With this, **a few crucial questions remain** to be answered, such as: 
- What products should be sold at which locations? 
- How should the product portfolio change with the seasons? 
- Which products are likely to be bought at which airport?

PoolFlow&Skarfify's team of data scientists noticed early on that the type of products purchased (swimwear vs. cold-weather accessories) correlates heavily with the location of the airport and the climate in that region. Additionally, the amount of travellers entering the country at those airports, where they are from, and for what reason they are travelling also seems to have a strong impact on purchasing behavior.

## :dvd: Utilized Data Sets
To tackle the data challenges the team was facing, four data sources were used. The data sets were provided by Udacity, but no documentation was provided except the source URL.

### 1. Airport Code Table :airplane:
The data set features a table of airports around the world. It includes information about the name and IATA abbreviation code (e.g. SFO for San Francisco) of airports, as well as their geographical location. The data set can be accessed [here](https://datahub.io/core/airport-codes#data).

This data set is useful, as it is a comprehensive list of all potential store locations for PoolFlow&Skarfify.

### 2. I94 Immigration Data :passport_control:
This data was released by the US National Tourism and Trade Office and contains information about travellers arriving in the US. It details the immigrant's date and port of arrival, gender, age, nationality, reason for immigration and much more. [This](https://www.trade.gov/national-travel-and-tourism-office) is where the data can be requested.

The data is very valuable for PoolFlow&Skarfify as it shows which airports attract the most travelers and where the travelers come from, which is an important detail for predicting their purchasing behavior.

### 3. World Temperature Data :thermometer:
This data set contains information about temperatures in the past in different locations all over the globe. It can be accessed from [Kaggle](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data).

This data is crucial for the company as a location's temperature and climate directly influence what travelers will buy. For example, if a store is at an airport in Alaska, people entering the country there are more likely to pick up mittens and scarves than swimwear. In addition, the temperature data grants insights on the climate of the places where travelers are from. This is useful because when a lot of travelers from, for example, Scandinavia visit the state of Maine in the winter, they are likely better prepared for the cold weather than a traveler from South-East Asia, and therefore less likely to purchase winter accessories.

### 4. US City Demographic Data :family:
This last data set includes information about US demographics and informs about cities' population and their distribution in terms of gender and country of birth. It comes from [OpenSoft](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).

The data is useful for PoolFlow&Skarfify, because in the recent past the company not only attracted travelers but also people who are living in cities closeby. More populous cities therefore mean more potential customers. Furthermore, a high proportion of immigrant population generally correllates with a high share of family members and friends visiting, which, according to the findings of the team of data scientists, are generally less prepared for the weather in a given location than the average traveller, and thus more likely to be customers.

## :star: Data Model 
![Data Model](https://user-images.githubusercontent.com/54779918/118850893-82f98b80-b8d1-11eb-8a4c-2ef5b21f7683.png)

The central piece of information for PoolFlow&Skarfify is the list of airports that serve as potential store locations. That is why the `airports` table is at the center of the relational star schema. Using airport codes, traveller information from the `immigrants` table can be joined if necessary. Additional temperature information can be added by joining the `temperatures` table to the `airports` and `immigrants` tables either on the city of the airport or the traveler's country of origin. Lastly, data on demographics can be joined from the `us_demographics` table based on a given airport's city.

This schema is ideal for PoolFlow&Skarfify's business use case as it is the company's goal to find ideal store locations, and to figure out which products to sell at each given location. Hence, the company's data scientists always need information that is joined together with a given store location.

## :eyes: Data Exploration and Cleaning ##

* ### Airports
  - The data set includes airports from all around the world. For now, however, PoolFlo&Skarfify is only operating in the US, so all airports outside the US can be dropped from the data.
  - The data set also contains many smaller airports at which it would be generally impossible to set up a store for the company. Hence, only airports that have an actual IATA code, which indicates busier and generally more important airports, are used.
* ### Immigration
  - The immigration data set also includes travellers that enter the US by other means than using an aircraft, i.e. through a land border or by boat. PoolFlow&Skarfify is not interested in the statistics on such travelers, and they are therefore filtered out.
  - The country of residency is encoded with an integer identifier. The data scientists, however, are using the country name for their analysis. Therefore, the country strings have to be mapped to the country identifiers first (provided in `data_mappings.py`).
  - A similar mapping has to be applied to the visa type, which is also only in the form of an integer identifier in the raw data.
  - The arrival date is encoded in the SAS date format, i.e. the number of days since January 1st, 1960. The data scientists use a standard YYYY-MM-DD format, i.e. the data has to be cleaned accordingly.
* ### Temperatures
  - There is one row for every combination of city and month, however many of them have `None` values since no data was available for that month. These rows without actual numerical measurements have to be dropped first.
  - PoolFlow&Skarfify is only interested in relatively recent temperature data, so all data points before 2010 can be dropped.

## :dash: Intended Data Pipeline
- First, the individual data sets are loaded from the data lake using Spark.
- Using Spark, rows and columns of interest are selected and the remaining data is cleaned according to the steps outlined before.
- The data is shaped into Spark dataframes that adhere to the previously outlined data model.
- Data quality Spark jobs are run to make sure that the data has the required quality.
- Then, the resulting tables are stored in the read-optimized Parquet data format.

Spark is used exensively for the data pipeline, as it allows PoolFlow&Skarfify for high flexibility when implementing the pipeline and enormous horizontal scalability when expanding the business to more stores or other countries.

Further intended steps/improvements:
- The parquet files are used to driectly populate a data warehouse, e.g. Amazon Redshift, which uses the provided data model. This data warehouse is where the company's data scientists access the data for their analyses.
- The individual steps of the data pipeline can be executed using Apache Airflow to improve the pipeline's maintainability.

## :question: Data Quality Checks

## :thought_balloon: Specific Scenario Considerations

