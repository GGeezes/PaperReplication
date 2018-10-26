import MySQLdb
import csv 
import fileinput

tables = ["Bug_Report_Data_Test", "Not_Bug_Report_Data_Test",
          "Feature_OR_Improvment_Request_Data_Test", "Not_Feature_OR_Improvment_Request_Data_Test",
          "Rating_Data_Test", "Not_Rating_Data_Test",
          "UserExperience_Data_Test", "Not_UserExperience_Data_Test"]

db = MySQLdb.connect(host="127.0.0.1", user="root", db="re2015_training_set") 

db.autocommit(True)
db.begin()
cur = db.cursor()

for table in tables:
    cur.execute('TRUNCATE TABLE `%s`;'%table)
    db.commit()


def insertRecord(tableName, values):     
    cur.execute('INSERT INTO '+ tableName +' (appId, reviewId, title, comment, rating, reviewer, fee, date, dataSource, sentiScore, sentiScore_pos, sentiScore_neg) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',values)
    db.commit()

def getSentiScores(fileName):
    with open(fileName, 'rb') as file:
        
        sentiScores = {}
        csv_reader = csv.reader(file,  delimiter=',')
        line = 0
        for row in csv_reader:
            if (line == 0) :
                line += 1
                continue
            else :
                line += 1
                id = row[0].split('|')[1]
                sentiscore = int(row[1])
                sentipos = int(row[2])
                sentineg = int(row[3])
                sentiScores[id] = (sentiscore, sentipos, sentineg)
    return sentiScores

sentiScores = getSentiScores('Sentiscores.csv')

with open("replication_data_labeled_final.csv", "rb") as file:
    file_reader = csv.reader(file, delimiter = ",")
    file_reader.next() #skip header
    seen = set()
    removed_rows = 0
    for row in file_reader:

        id = row[3]
        if row[3] in seen: 
            removed_rows = removed_rows + 1
            continue # skip duplicate
        seen.add(row[3])

        values = (
            row[2], # appId 
            hash(row[3]), # reviewId
            row[4], # title
            row[5], # comment
            row[6], # rating
            row[7], # reviewer 
            row[8], # fee
            row[9], # data
            row[11], #dataSource
            sentiScores[id][0], #sentiScore
            sentiScores[id][1], #sentiment pos
            sentiScores[id][2] #sentiment neg
            )
        
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


