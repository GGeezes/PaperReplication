import MySQLdb
from BeautifulSoup import BeautifulStoneSoup

db = MySQLdb.connect(host="127.0.0.1", user="root", db="re2015_training_set") 
db.autocommit(True)
db.begin()
dbcur = db.cursor()

tables = ["Bug_Report_Data", "Bug_Report_Data_Test", "Bug_Report_Data_Train", "Feature_OR_Improvment_Request_Data", "Feature_OR_Improvment_Request_Data_Test", "Feature_OR_Improvment_Request_Data_Train", "Not_Bug_Report_Data", "Not_Bug_Report_Data_Test", "Not_Bug_Report_Data_Train", "Not_Feature_OR_Improvment_Request_Data", "Not_Feature_OR_Improvment_Request_Data_Test", "Not_Feature_OR_Improvment_Request_Data_Train", "Not_Rating_Data", "Not_Rating_Data_Test", "Not_Rating_Data_Train", "Not_UserExperience_Data", "Not_UserExperience_Data_Test", "Not_UserExperience_Data_Train", "Rating_Data", "Rating_Data_Test", "Rating_Data_Train", "UserExperience_Data", "UserExperience_Data_Test", "UserExperience_Data_Train"]

def unescape(text):
    return unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.ALL_ENTITIES))

for table in tables :
    dbcur.execute('SELECT id, stopwords_removal_lemmatization FROM {} WHERE stopwords_removal_lemmatization LIKE \'%&#%\';'.format(table))
    row_cnt = dbcur.rowcount
    for (id, comment) in dbcur :
        comment_fixed = unescape(comment)
        assert (comment != comment_fixed)
        sql = 'UPDATE {} SET comment=\'{}\' WHERE id={} '.format(table, db.escape_string(comment_fixed), id)
        # dbcur.execute(sql)

    print ('Table {} DONE, fixed: {} rows'.format(table, row_cnt))

db.commit()
