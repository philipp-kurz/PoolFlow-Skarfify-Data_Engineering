# PoolFlow&Skarkify - Data pipeline of an imaginary company
This repo contains my self-contrived **capstone project** for Udacity's **Data Engineering Nano-Degree** (DEND).

During this online course I learned about various data engineering topics such as relational and NoSQL data modeling, data warehousing, data lakes and data pipelines and gained hands-on experience with their application through different projects. I got especially interested in **Apache Spark** and what it brings to the table in terms of big data processing, and decided to utilize my capstone project to further deepen my learning about Spark.

## :mag: Project Scope
![PF_and_S_logo](https://user-images.githubusercontent.com/54779918/117148216-506e6f80-adb6-11eb-9d19-88fe9b736387.png)

**PoolFlow and Skarfify are leading airport retail chains.** PoolFlow sells swimwear while Skarfify sells scarves, mittens and hats. As the companies grew and opened more stores, the executives of both companies realized that their businesses were heavily dependent on the season and the origin of travelers. To diversify their product portfolios and adapt better to the changing seasons, **PoolFlow and Skarfify decided to merge together**. From now on, all stores will be operated jointly under the original name PoolFlow&Skarfify and products from both companies will be sold at the shared store locations.

With this, **a few crucial questions remain** to be answered, such as: 
- What products should be sold at which locations? 
- How should the product portfolio change with the seasons? 
- Which products are likely to be bought at which airport?

PoolFlow&Skarfify's team of data scientists noticed early on that the type of products purchased (swimwear vs. cold-weather accessories) correlates heavily with the location of the airport and the climate in that region. Additionally, the amount of travellers entering the country at those airports, where they are from, and for what reason they are travelling also seems to have a strong impact on purchasing behavior.

## :dvd: Utilized Data Sets
To tackle the data challenges the team was facing, four data sources were used. The data sets were provided by Udacity, but no documentation was provided except the source URL.

### 1. Airport Code Table :airplane:
The data set features a table of airports around the world. It includes information about the name and IATA abbreviation code (e.g. SFO for San Francisco) of a airport, as well as its geographical location. The data set can be accessed [here](https://datahub.io/core/airport-codes#data).

This data set is useful, as it is a comprehensive list of all potential store locations for PoolFlow&Skarfify.

### 2. I94 Immigration Data :passport_control:
This data was released by the US National Tourism and Trade Office and contains information about travellers arriving in the US. It details the immigrant's date and port of arrival, gender, age, nationality, reason for immigration and much more. [This](https://www.trade.gov/national-travel-and-tourism-office) is where the data can be requested.

The data is very valuable for PF&S as it shows which airports attract the most travelers and where the travelers come from, which is an important detail for predicting their purchasing behavior.

### 3. World Temperature Data :thermometer:
This data set contains information about temperatures in the past in different locations all over the globe. It can be accessed from [Kaggle](https://www.kaggle.com/berkeleyearth/climate-change-earth-surface-temperature-data).

This data is crucial for the company as a location's temperature and climate directly influences what travelers will buy. For example, if a store is at an airport in Alaska, people entering the country are more likely to pick up mittens and scarves than swimwear. In addition, the temperature data grants insights on the climate of the places where travelers are from. This is useful because when a lot of travelers from let's say Scandinavia visit the state of Maine in the winter, they are likely more prepared for the cold weather than a traveler from South-East Asia and therefore less likely to purchase winter accessories.

### 4. US City Demographic Data :family:
This last data set includes information about US demographics and informs about cities' population and their distribution in terms of gender and country of birth. It comes from [OpenSoft](https://public.opendatasoft.com/explore/dataset/us-cities-demographics/export/).

The data is useful for PoolFlow&Skarfify, because in the recent past the company not only attracted travelers but also people living in cities closeby. More populous cities therefore mean more potential customers. Furthermore, a high proportion of immigrant population generally correllates with a high share of family members and friends visiting, which, according to the findings of the team of data scientists, are generally less prepared for the weather in a given location than the average traveller.

## Data Model :star:
