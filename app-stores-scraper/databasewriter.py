import MySQLdb
import csv 
import fileinput

tables = ["Bug_Report_Data_Test_Rep", "Not_Bug_Report_Data_Test_Rep",
    "Feature_OR_Improvment_Request_Data_Test_Rep", "Not_Feature_OR_Improvment_Request_Data_Test_Rep",
    "Rating_Data_Test_Rep", "Not_Rating_Data_Test_Rep",
    "UserExperience_Data_Test_Rep", "Not_UserExperience_Data_Test_Rep"]

db = MySQLdb.connect(host="127.0.0.1", 
                     user="root", 
                      db="re2015_training_set") 

db.autocommit(True)
db.begin()
cur = db.cursor()

for table in tables:
    try:
        cur.execute('DROP TABLE IF EXISTS `%s`;'%table)
        db.commit()
    except:
        print('fail')
        db.rollback()

    try:
        cur.execute('''CREATE TABLE `%s` (
            `id` int(11) NOT NULL DEFAULT '0',
            `appId` varchar(255) DEFAULT NULL,
            `reviewId` varchar(255) DEFAULT NULL,
            `title` varchar(255) DEFAULT NULL,
            `comment` varchar(32767) DEFAULT NULL,
            `rating` int(11) DEFAULT NULL,
            `reviewer` varchar(255) DEFAULT NULL,
            `fee` varchar(20) DEFAULT NULL,
            `date` varchar(255) DEFAULT NULL,
            `dataSource` varchar(255) DEFAULT NULL,
            `stopwords_removal` varchar(5535) DEFAULT NULL,
            `lemmatized_comment` varchar(5535) DEFAULT NULL,
            `stemmed` varchar(5535) DEFAULT NULL,
            `sentiScore` int(11) DEFAULT NULL,
            `sentiScore_pos` int(11) DEFAULT NULL,
            `sentiScore_neg` int(11) DEFAULT NULL,
            `stopwords_removal_nltk` varchar(5535) DEFAULT NULL,
            `stopwords_removal_lemmatization` varchar(5535) DEFAULT NULL,
            `length_words` int(11) DEFAULT NULL,
            `present_simple` int(11) DEFAULT NULL,
            `present_con` int(11) DEFAULT NULL,
            `past` int(11) DEFAULT NULL,
            `future` int(11) DEFAULT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=latin1;'''%(table))
        db.commit()
    except:
        print('fail')
        db.rollback()


def insertRecord(tableName, values):
    try:          
        cur.execute('''INSERT INTO '''+ tableName +'''(appId, reviewId, title, comment, rating, reviewer, fee, date, dataSource) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)''',values)
        db.commit()
    except Exception as e:
        print("ERROR app: %s (id: %s): %s"%(values[0], values[1], str(e)))
        db.rollback()


with open("replication_data _labeled.csv", "rb") as file:
    file_reader = csv.reader(file, delimiter = ",")
    print(file_reader.next())
    seen = set()
    removed_rows = 0
    for row in file_reader:

        if row[3] in seen: 
            removed_rows = removed_rows + 1
            continue # skip duplicate
        seen.add(row[3])
        
        try:
            values = (
                row[2], # appId 
                row[3], # reviewId
                row[4], # title
                row[5], # comment
                row[6], # rating
                row[7], # reviewer 
                row[8], # fee
                row[9], # data
                row[11]) # datasource
            
            if (int(row[12]) == 1): # is_userExperience
                insertRecord(tables[6], values)
            else:
                insertRecord(tables[7], values)

            if (int(row[13]) == 1): # is_bugReport
                insertRecord(tables[0], values)
            else:
                insertRecord(tables[1], values)

            if (int(row[14]) == 1): # is_featureRequest
                insertRecord(tables[2], values)
            else:
                insertRecord(tables[3], values)

            if (int(row[15]) == 1): # is_rating
                insertRecord(tables[4], values)
            else:
                insertRecord(tables[5], values)

        except Exception as e:
            print(e)


print("====================")
print("Removing duplicates ...")

print("Remaining number of rows: %d"%len(seen))
print("Removed duplicates: %d"%removed_rows)

print("====================")

for table in tables:
    cur.execute("SELECT COUNT(*) FROM %s"%(table))
    numRecords = cur.fetchone()[0]
    print("Table %s has %s records"%(table, numRecords))

cur.close()
db.close()


