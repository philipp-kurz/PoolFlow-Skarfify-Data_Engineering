# PoolFlow&Skarkify - Data pipeline of an imaginary company
This repo contains my self-contrived capstone project for Udacity's Data Engineering Nano-Degree (DEND). Month-long learning on topics such as relational and NoSQL data modeling, data warehousing, data lakes and data pipelines culimnate in this project.

The project implements a data pipeline that fetches data residing in an **AWS S3** data lake, cleans and transforms the data using **Apache Spark** and **AWS EMR**, and stores it back to S3. The data is then loaded into **AWS Redshift**, where it is reshaped into a **relational/SQL star schema** with fact and dimension tables for analytics workloads. The data pipeline is managed by **Apache Airflow** running on an **AWS EC2** instance and the required AWS infrastructure is provisioned and deployed using **AWS CloudFormation**.

## Introductory Narrative & Project Idea
![PF_and_S_logo](https://user-images.githubusercontent.com/54779918/117148216-506e6f80-adb6-11eb-9d19-88fe9b736387.png)

PoolFlow and Skarfify are leading airport retail chains. PoolFlow sells swimwear while Skarfify sells scarves, mittens and hats. As the companies grew and opened more stores, the executives of both companies realized that their businesses were heavily dependent on the season and the origin of travelers. To diversify their product portfolios and adapt better to the changing seasons, PoolFlow and Skarfify decided to merge together. From now on, all stores will be operated jointly under the original name PoolFlow&Skarfify and products from both companies will be sold at the shared store locations.

With this, a few crucial questions remain to be answered: What products should be sold at which locations? How should the product portfolio change with the seasons? Which products are likely to be bought at which airport?

PoolFlow&Skarfify's team of data scientists noticed early on that the type of products purchased (swimwear vs. cold-weather accessories) correlates heavily with the location of the airport and the climate in that region, and also with the amount and origin of immigrants arriving in the States at a certain airport. While the latter is surprising, the data scientists found a simple yet intuitive explanation: Immigrants are often visited by family and friends, and if they don't own swimwear or winter clothing (based on where they are from and whichever is more suitable at their destination), they tend to purchase them at the airport.
