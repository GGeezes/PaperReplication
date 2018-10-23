SELECT reviewID, comment, stopwords_removal 
    FROM Bug_Report_Data

SELECT GROUP_CONCAT(TABLE_NAME SEPARATOR '", "')
    FROM INFORMATION_SCHEMA.TABLES
    WHERE TABLE_SCHEMA = 're2015_training_set'
    GROUP BY TABLE_SCHEMA

SELECT GROUP_CONCAT(COLUMN_NAME SEPARATOR ', ')
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = 're2015_training_set'
    GROUP BY TABLE_NAME


SELECT * FROM INFORMATION_SCHEMA.COLUMNS

SELECT *
    FROM re2015_training_set.Feature_OR_Improvment_Request_Data 
    WHERE comment LIKE '%&#%';
