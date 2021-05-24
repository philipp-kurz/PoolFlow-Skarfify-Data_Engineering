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
* `airline`
* `visa_type`
* `residency`

## `temperatures` table
* `temperature_id`
* `city`
* `country`
* `date`
* `temperature`

## `us_demographics` table
* `us_city`
* `total_pop`
* `median_age`
* `foreign_born_pop`
* `fraction_foreign_born`
