import MySQLdb
from nltk.tokenize import word_tokenize

db = MySQLdb.connect(host="127.0.0.1", user="root", db="re2015_training_set") 
db.autocommit(True)
db.begin()

dbcur = db.cursor()

tables = ["Bug_Report_Data", "Bug_Report_Data_Test", "Bug_Report_Data_Train", "Feature_OR_Improvment_Request_Data", "Feature_OR_Improvment_Request_Data_Test", "Feature_OR_Improvment_Request_Data_Train", "Not_Bug_Report_Data", "Not_Bug_Report_Data_Test", "Not_Bug_Report_Data_Train", "Not_Feature_OR_Improvment_Request_Data", "Not_Feature_OR_Improvment_Request_Data_Test", "Not_Feature_OR_Improvment_Request_Data_Train", "Not_Rating_Data", "Not_Rating_Data_Test", "Not_Rating_Data_Train", "Not_UserExperience_Data", "Not_UserExperience_Data_Test", "Not_UserExperience_Data_Train", "Rating_Data", "Rating_Data_Test", "Rating_Data_Train", "UserExperience_Data", "UserExperience_Data_Test", "UserExperience_Data_Train"]
print('TABLE, SAME_SENTI, TOTAL_ITEMS')
for table in tables:
    dbcur.execute('SELECT count(id) FROM {} WHERE sentiScore_pos=-sentiScore_neg AND sentiScore != 0 '.format(table))
    same_cnt = dbcur.fetchone()[0]
    dbcur.execute('UPDATE {} SET sentiScore=0 WHERE sentiScore_pos=-sentiScore_neg'.format(table))

    dbcur.execute('SELECT count(id) FROM {}'.format(table))
    total_cnt = dbcur.fetchone()[0]

    print ('{}, {}, {}'.format(table, same_cnt, total_cnt))
    
    # for (id, score, pos, neg) in dbcur :
    #     if (pos != 1) :
    #     print ('[{}] POS: {}, NEG: {} SCORE: {}'.format(id, pos, neg, score))
db.commit()    
