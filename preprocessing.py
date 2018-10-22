import MySQLdb
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

db = MySQLdb.connect(host="127.0.0.1", user="root", db="re2015_training_set") 
db.autocommit(True)
db.begin()

dbcur = db.cursor()

lemm = WordNetLemmatizer()
lemm.lemmatize("test") #force word-cache load

#stop_words = set(stopwords.words('english'))
stop_words = set([u'all', u'just', u"don't", u'being', u'over', u'both', u'through', u'yourselves', u'its', u'o', u'don', u'hadn', u'herself', u'll', u'had', u'to', u'only', u'won', u'under', u'ours', u'has', u"haven't", u'do', u'them', u'his', u"you've", u'they', u'not', u'during', u'him', u'nor', u'd', u'this', u'she', u'each', u'further', u"won't", u'where', u"isn't", u'few', u"you'd", u'doing', u'some', u'hasn', u"hasn't", u'are', u'our', u'ourselves', u'out', u'what', u'for', u"needn't", u'below', u're', u'does', u'above', u'between', u't', u'be', u'we', u'who', u"mightn't", u"doesn't", u'were', u'here', u'hers', u"aren't", u'by', u'on', u'about', u'couldn', u'of', u"wouldn't", u'against', u's', u'isn', u'or', u'own', u'into', u'yourself', u"hadn't", u'mightn', u"couldn't", u'wasn', u'your', u"you're", u'from', u'her', u'their', u'aren', u"it's", u'there', u'been', u'whom', u'wouldn', u'themselves', u'weren', u'was', u'until', u'more', u'himself', u'that', u"that'll", u'with', u'than', u'those', u'he', u'me', u"wasn't", u'myself', u'ma',
u"weren't", u'these', u'will', u'ain', u'can', u'theirs', u'my', u'and', u've', u'then', u'is', u'am', u'it', u'doesn', u'an', u'as', u'itself', u'at', u'have', u'in', u'any', u'if', u'again', u'no', u'when', u'same', u'how', u'other', u'which', u'you', u"shan't", u'shan', u'needn', u'haven', u'after', u'most', u'such', u'why', u'a', u'off', u'i', u'm', u'yours', u"you'll", u'so', u'y', u"she's", u'the', u'having', u'once']);
#print(stop_words)

# dbcur.execute("SELECT * FROM Bug_Report_Data_Train" )

# for row in dbcur.fetchall() :
#     print(row[2])

dbcur.execute("SELECT reviewID, comment, stopwords_removal FROM Bug_Report_Data LIMIT 0,10" )

for (reviewID, comm, comm_sw_orig) in dbcur :
        words = word_tokenize(comm)
        words_lower = [x.lower() for x in words]
        words_filtered = [w for w in words_lower if w not in stop_words]
        comm_sw_new = ' '.join(words_filtered)
        print('ORIG: {}'.format(comm))
        print('STOP WORDS RM OURS: {}'.format(comm_sw_new))
        print('STOP WORDS RM ORIG: {} '.format(comm_sw_orig))
        #print('STOP WORDS RM ARR: {}'.format(words_filtered))
        #print(lemm.lemmatize(title))
        print("---------------------------------")

db.commit()