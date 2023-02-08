# Nicasource Data Engineering Challenge

First of, thank you very much for your consideration and the opportunity you've provided. My name is Daniel Ramirez and I'm a data engineer. I'm passionate about handling data and most of all, solving problems. Below you'll find the solution I developed for the challenge you sent me. If you have any questions or concerns, please contact me at urbdaniel.86@gmail.com.

## The Problem Solving Process:

I like to start tackling any problem by laying out a plan that will guide my solving process. First, I list the different parts of the problem in no particular order:

- The pipeline
- The SQL database
- The Git repository

I then fill in the different tasks, challenges, and/or requirements within each part of the problem:

- The pipeline:
    - Where to get the CSV source file? Link or local?
    - Script considerations:
        - Error handling and logging
        - High quality
        - Modular
        - Scalable
- The SQL database:
    - Where to store it?
    - How to handle credentials?
- The Git repository

Going through the list, the time to make decisions came:

- The CSV source file will be loaded locally: this means the pipeline script will only work once and for the csv file stored locally, so it won't be scalable (i.e. it won't read files with different names or stored online). BUT, the transformations will be modular, meaning that they'll be written in a different file and can be called from future hypothetical pipelines, which is scalable enough for this excersize.
- The SQL database will be stored in Amazon RDS: due to the constrains of this challenge, I'll limit myself to create an Amazon RDS where the transformed data from my python ETL script will be stored. But ideally, I'd build the whole pipeline in Azure as follows:
    - I'd setup an Azure Storage Account to store the source files. Periodically, files with the car sales will be loaded here to beging the ETL process.
    - I'd setup an Azure SQL Database to store the data once transformed.
    - I'd setup an Azure Data Factory with either event or schedule triggers to read the source files from the Storage Account, make the required transformations, then load the data into the SQL database.
- For handling the data base credentials, I'll store the SQL DB address, login and password in a JSON file and share it via email with the evaluation team.

### Additional considerations

The only CSV file I could find online was a Kaggle repository called Car_sales.csv. This file doesn't have a 'Sales Date' column and thus I can't store the year of the sale. Similarly, the 'Car Model' doesn't really store cathegorical values; transforming this column to numerical values will result in 158 values, one for each record. For this reason, and in order to follow the instructions as close a possible, the transformations will be as follows:

- Remove any rows with missing values
- Convert the date columns to a standard format
- Create a new column to store the year of the launch
- Replace the categorical values in the "Vehicle_type" column with numerical values


## Summary

In summary, the solution of this problem consists in the following:

- Utils.py: a library that contains the transformation and loading functions, allowing for modularity and scalability
- Pipeline.py: the ETL pipeline. It works specifically for the CSV source file, Car_sales.csv
- Reset.py: a script that wipes the database table so the pipeline can be ran again to load the data
- Query.py: a script to verify the data has been loaded to the SQL DB
- Car_sales.csv: the file containing the data
- Credentials.json: not included in the repo, it has all the information needed to connect to the Amazon RDS database

## Instructions

1. Clone this repository on your computer
2. From the email I sent, download Credentials.json and copy it in the folder where the repo was cloned
3. Open a terminal and run Queries.sql to verify the DB is running and it has no data
4. Run Pipeline.py
5. Run Query.py to verify the data was loaded
6. You can run Pipeline.py again to verify handling of duplicated data
7. If you want to start over, run Reset.py
8. You can also connect to the database with MySQL Workbench or any other SQL terminal and run queries using the credentials in the JSON file
