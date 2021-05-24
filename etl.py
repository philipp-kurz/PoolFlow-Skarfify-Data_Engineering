import configparser
import os
from pyspark.sql import SparkSession
from data_mappings import *
import pyspark.sql.functions as F
import pyspark.sql.types as T
from itertools import chain
import datetime


def create_spark_session():
    '''
    Returns a Spark session for the ETL job.

            Returns:
                    spark: Spark session object
    '''
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
    os.environ["PATH"] = "/opt/conda/bin:/opt/spark-2.4.3-bin-hadoop2.7/bin:/opt/conda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/java-8-openjdk-amd64/bin"
    os.environ["SPARK_HOME"] = "/opt/spark-2.4.3-bin-hadoop2.7"
    os.environ["HADOOP_HOME"] = "/opt/spark-2.4.3-bin-hadoop2.7"
    
    return SparkSession.builder.getOrCreate()


def process_immigration_data(spark, input_data):
    '''
    Processes I94 immigration data SAS files and returns a Spark data frame of the resulting immigration table

            Parameters:
                    spark (object): A Spark session object
                    input_data (str): Input path to the data
            Returns:
                    A spark dataframe for the resulting immigration table    
    '''
    print('Processing immigration data')
    
    df_immigration_data = spark.read.load(input_data)
    
    immigration_columns = {
        'cicid': ('immigration_id', 'int'),
        'i94port': ('airport_id', 'string'),
        'i94res': ('residency_unmapped', 'int'),
        'i94addr': ('destination_state', 'string'),
        'arrdate': ('arrival_date_unmapped', 'int'),
        'i94bir': ('age', 'int'),
        'gender': ('gender', 'string'),
        'airline': ('airline', 'string'),
        'i94visa': ('visa_type_unmapped', 'int')
    }
    
    drop_columns = [value[0] for value in immigration_columns.values() if 'unmapped' in value[0]]

    # https://stackoverflow.com/questions/42980704/pyspark-create-new-column-with-mapping-from-a-dict
    # Accessed: 18/05/2021
    country_mapping_expr = F.create_map([F.initcap(F.lit(x)) for x in chain(*country_mapping.items())])
    visa_type_mapping_expr = F.create_map([F.lit(x) for x in chain(*visa_type_mapping.items())])

    # https://stackoverflow.com/questions/26923564/convert-sas-numeric-to-python-datetime
    # Accessed: 18/05/2021
    epoch_start = datetime.datetime(1960, 1, 1)
    sas_date_udf = F.udf(lambda sas_date_int: epoch_start + datetime.timedelta(days=sas_date_int), T.TimestampType())

    selectExpressions = [f'cast({old} as {new[1]}) as {new[0]}' for old, new in immigration_columns.items()]
    df_immigration_table = df_immigration_data.selectExpr(*selectExpressions)\
                                              .withColumn('residency', country_mapping_expr.getItem(F.col("residency_unmapped")))\
                                              .withColumn('visa_type', visa_type_mapping_expr.getItem(F.col("visa_type_unmapped")))\
                                              .withColumn('arrival_date', sas_date_udf(F.col('arrival_date_unmapped')))\
                                              .drop(*drop_columns)
    return df_immigration_table

    
def process_airport_data(spark, input_data):
    '''
    Processes the airport data set and returns a Spark data frame of the resulting airports table

            Parameters:
                    spark (object): A Spark session object
                    input_data (str): Input path to the data
            Returns:
                    A spark dataframe for the resulting airports table      
    '''
    print('Processing airport data')
    
    df_airports_data = spark.read.option("header",True).csv(input_data)
    
    airport_columns = {
        'iata_code': ('airport_id', 'string'),
        'name': ('airport_name', 'string'),
        'municipality': ('city', 'string'),
        'iso_region': ('state_unmapped', 'string'),
        'elevation_ft': ('elevation_ft', 'string')
    }
    
    selectExpressions = [f'cast({old} as {new[1]}) as {new[0]}' for old, new in airport_columns.items()]
    drop_columns = [value[0] for value in airport_columns.values() if 'unmapped' in value[0]]
    state_mapping_udf = F.udf(lambda state_code: state_code[3:])


    df_airports_table = df_airports_data.filter(F.col('iata_code').isNotNull())\
                                        .filter(F.col('iso_country') == 'US')\
                                        .filter(F.col('type') != 'closed')\
                                        .selectExpr(*selectExpressions)\
                                        .withColumn('state', state_mapping_udf(F.col('state_unmapped')))\
                                        .drop(*drop_columns)
    return df_airports_table

    
def process_temperature_data(spark, input_data):
    '''
    Processes temperature data files and returns a Spark data frame of the resulting temperatures table

            Parameters:
                    spark (object): A Spark session object
                    input_data (str): Input path to the data
            Returns:
                    A spark dataframe for the resulting temperatures table      
    '''
    print('Processing temperature data')
    
    df_temperature_data = spark.read.option("header",True).csv(input_data)
    
    temperature_columns = {
        'dt': ('date', 'date'),
        'City': ('city', 'string'),
        'Country': ('country', 'string'),
        'AverageTemperature': ('temperature', 'float')
    }
    selectExpressions = [f'cast({old} as {new[1]}) as {new[0]}' for old, new in temperature_columns.items()]

    df_temperature_table = df_temperature_data.filter(F.col('AverageTemperature').isNotNull())\
                                              .filter(F.col('dt') >= '2010-01-01')\
                                              .selectExpr(*selectExpressions)\
                                              .withColumn('temperature_id', F.monotonically_increasing_id())
    return df_temperature_table
    
    
def process_demographics_data(spark, input_data):
    '''
    Processes US demographics data set and returns a Spark data frame of the resulting demographics table

            Parameters:
                    spark (object): A Spark session object
                    input_data (str): Input path to the data
            Returns:
                    A spark dataframe for the resulting demographics table      
    '''
    print('Processing demographics data')
    
    df_us_demographics_data = spark.read.option("header",True).option("delimiter",';').csv(input_data)
    
    us_demographics_columns = {
        'City': ('us_city', 'string'),
        '`State Code`': ('state', 'string'),
        '`Total Population`': ('total_pop', 'int'),
        '`Median Age`': ('median_age', 'int'),
        '`Foreign-born`': ('foreign_born_pop', 'int')
    }
    selectExpressions = [f'cast({old} as {new[1]}) as {new[0]}' for old, new in us_demographics_columns.items()]

    df_us_demographics_table = df_us_demographics_data.selectExpr(*selectExpressions)\
                                                      .withColumn('fraction_foreign_born', F.col('foreign_born_pop') / F.col('total_pop'))
    return df_us_demographics_table


def check_immigration_data(spark, df_immigration_table):
    '''
    Runs quality checks on immigration data and prints results

            Parameters:
                    spark (object): A Spark session object
                    df_immigration_table (object): A spark data frame with the immigration table   
    '''
    print('Checking immigration table.')
    
    num_rows = df_immigration_table.count()
    print(f"{num_rows} of new immigration entries were found! Should be > 0.")
    
    num_negative_age = df_immigration_table.filter(F.col('age') < 0).count()
    print(f"{num_negative_age} records with negative age found! Should be 0.")
    
    min_date = '2000-01-01' # Retrieve date from Airflow DAG run instead
    num_old_date = df_immigration_table.filter(F.col('arrival_date') < min_date).count()
    print(f"{num_old_date} records with too old date found! Should be 0.")
          
          
def check_airports_data(spark, df_airports_table):
    '''
    Runs quality checks on airports data and prints results

            Parameters:
                    spark (object): A Spark session object
                    df_airports_table (object): A spark data frame with the airports table   
    '''
    print('Checking airports table.')
    
    # https://stackoverflow.com/questions/48229043/python-pyspark-count-null-empty-and-nan
    # Accessed: 24/05/2021
    num_empty_rows = df_airports_table.filter((F.col("airport_id") == "") | 
                                               F.col("airport_id").isNull() | 
                                               F.isnan(F.col("airport_id"))).count()
    print(f"{num_empty_rows} records empty airport ID! Should be 0.")
          

def check_temperature_data(spark, df_temperature_table):
    '''
    Runs quality checks on temperature data and prints results

            Parameters:
                    spark (object): A Spark session object
                    df_temperature_table (object): A spark data frame with the temperature table   
    '''
    print('Checking temperature table.')

    num_null_rows = df_temperature_table.filter(F.col("temperature").isNull()).count()
    print(f"{num_null_rows} records with empty temperature found! Should be 0.")
          
          
def check_demographics_data(spark, df_us_demographics_table):
    '''
    Runs quality checks on demographics data and prints results

            Parameters:
                    spark (object): A Spark session object
                    df_us_demographics_table (object): A spark data frame with the US demographics table   
    '''
    print('Checking demographics table.')

    num_negative_rows = df_us_demographics_table.filter(F.col("total_pop") <= 0).count()
    print(f"{num_negative_rows} records with negative total population found! Should be 0.")
              

def store_df_as_parquet(input_df, output_path):
    '''
    Stores given Spark dataframes as Parquet files

            Parameters:
                    input_df (object): A spark data frame 
                    output_path (str): Path where the parquet files should be stored
    '''
    print(f'Writing Spark dataframe to {output_path}')
    input_df.write.parquet(output_path)

          
def main():
    config = configparser.ConfigParser()
    config.read('configs.ini')
    
    spark = create_spark_session()
    
    df_immigration_table = process_immigration_data(spark, config['input']['immigration'])
    df_airports_table = process_airport_data(spark, config['input']['airports'])
    df_temperature_table = process_temperature_data(spark, config['input']['temperatures'])
    df_us_demographics_table = process_demographics_data(spark, config['input']['demographics'])
    
    check_immigration_data(spark, df_immigration_table)
    check_airports_data(spark, df_airports_table)
    check_temperature_data(spark, df_temperature_table)
    check_demographics_data(spark, df_us_demographics_table)
          
    store_df_as_parquet(df_immigration_table, config['output']['folder_path'] + 'immigrants')
    store_df_as_parquet(df_airports_table, config['output']['folder_path'] + 'airports')
    store_df_as_parquet(df_temperature_table, config['output']['folder_path'] + 'temperatures')
    store_df_as_parquet(df_us_demographics_table, config['output']['folder_path'] + 'demographics')


if __name__ == "__main__":
    main()
