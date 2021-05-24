# :closed_book: Data Dictionary
![Proposed Data Model](https://user-images.githubusercontent.com/54779918/118850893-82f98b80-b8d1-11eb-8a4c-2ef5b21f7683.png)

## `airports` table
* `airport_id`
  - Unique identifier for each airport
  - Based on the airports' IATA codes in the airports data set (`iata_code` column)
* `airport_name`
  - Name of a given airport
  - Based on the `name` column in the airports data set
* `city`
  - City where the airport is located
  - Based on the `municipality` column of the airports data set
* `state`
  - US state of the airport
  - Obtained from the `region` column in the airports data set, which is in the format "US-XX"
* `elevation_ft`
  - Elevation above sea level
  - Directly based on the `elevation_ft` column in the airports data set

## `immigrants` table
* `immigration_id`
  - Unique identifier for each traveler entering the US at a given date
  - Based on the `cicid` column in the I94 immigration data set
* `airport_id`
  - Unique identifier of the airport at which the immigrant entered the US
  - Links to primary key of `airports` table
  - Based on the `i94port` column in the I94 immigration data set
* `arrival_date`
  - Date at which the given immigration of the traveler happened
  - Extracted from the `arrdate` column in the I94 immigration data set by transforming the SAS date to a YYYY-MM-DD date format
* `age`
  - Age of the traveler entering the US
  - Based on the `i94bir` column of the I94 immigration data set
* `gender`
  - Gender of a given traveler
  - Directly based on the `gender` column in the I94 immigration data set
* `airline`
  - Airline which the traveler used to fly to the US
  - Directly based on the `airline` column in the I94 immigration data set
* `visa_type`
  - Visa type (e.g. Business, Student, or Leisure) that the traveler has
  - Based on the `i94visa` column of the I94 immigration data set 
  - A value-to-string mapping of the individual values has to be applied to the raw data first (see `visa_type_mapping` in `data_mappings.py`)
* `residency`
  - The travelers' country of residency
  - Based on the `i94res` column of the I94 immigration data set
  - A value-to-string mapping of the individual values has to be applied to the raw data first (see `country_mapping` in `data_mappings.py`)

## `temperatures` table
* `temperature_id`
  - Unique identifier for a given temperature record
  - Randomly created UUID upon Spark job execution
* `city`
  - City in which a given temperature measurement was recorded
  - Based on the `City` column in the temperatures data set
* `country`
  - Country in which the temperature was recorded
  - Based on the `Country` column in the temperatures data set
* `date`
  - Date at which this temperature measurement was recorded
  - Based on the `dt` column in the temperatures data set
* `temperature`
  - Actual temperature measurement at the given time and location
  - Based on the `AverageTemperature` column in the temperatures data set

## `us_demographics` table
* `us_city`
* `total_pop`
* `median_age`
* `foreign_born_pop`
* `fraction_foreign_born`
