import MySQLdb
from contractions import expandContractions

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, TweetTokenizer, RegexpTokenizer
from nltk.corpus import stopwords

db = MySQLdb.connect(host="127.0.0.1", user="root", db="re2015_training_set") 
db.autocommit(True)
db.begin()

dbcur = db.cursor()

lemm = WordNetLemmatizer()
lemm.lemmatize("test") #force word-cache load

#tok = TweetTokenizer() #TwitterTokenizer hadles smileys and contractions
tok = RegexpTokenizer(r'\w+') #Removes all non-words

#stop_words = set(stopwords.words('english'))
stop_words = set([u'all', u'just', u"don't", u'being', u'over', u'both', u'through', u'yourselves', u'its', u'o', u'don', u'hadn', u'herself', u'll', u'had', u'to', u'only', u'won', u'under', u'ours', u'has', u"haven't", u'do', u'them', u'his', u"you've", u'they', u'during', u'him', u'nor', u'd', u'this', u'she', u'each', u'further', u"won't", u'where', u"isn't", u'few', u"you'd", u'doing', u'some', u'hasn', u"hasn't", u'are', u'our', u'ourselves', u'out', u'what', u'for', u"needn't", u'below', u're', u'does', u'above', u'between', u't', u'be', u'we', u'who', u"mightn't", u"doesn't", u'were', u'here', u'hers', u"aren't", u'by', u'on', u'about', u'couldn', u'of', u"wouldn't", u'against', u's', u'isn', u'or', u'own', u'into', u'yourself', u"hadn't", u'mightn', u"couldn't", u'wasn', u'your', u"you're", u'from', u'her', u'their', u'aren', u"it's", u'there', u'been', u'whom', u'wouldn', u'themselves', u'weren', u'was', u'until', u'more', u'himself', u'that', u"that'll", u'with', u'than', u'those', u'he', u'me', u"wasn't", u'myself', u'ma',
u"weren't", u'these', u'will', u'ain', u'theirs', u'my', u'and', u've', u'then', u'is', u'am', u'it', u'doesn', u'an', u'as', u'itself', u'at', u'have', u'in', u'any', u'if', u'again', u'no', u'when', u'same', u'how', u'other', u'which', u'you', u"shan't", u'shan', u'needn', u'haven', u'after', u'most', u'such', u'why', u'a', u'off', u'i', u'm', u'yours', u"you'll", u'so', u'y', u"she's", u'the', u'having', u'once']);

tables = ["Bug_Report_Data", "Bug_Report_Data_Test", "Bug_Report_Data_Train", "Feature_OR_Improvment_Request_Data", "Feature_OR_Improvment_Request_Data_Test", "Feature_OR_Improvment_Request_Data_Train", "Not_Bug_Report_Data", "Not_Bug_Report_Data_Test", "Not_Bug_Report_Data_Train", "Not_Feature_OR_Improvment_Request_Data", "Not_Feature_OR_Improvment_Request_Data_Test", "Not_Feature_OR_Improvment_Request_Data_Train", "Not_Rating_Data", "Not_Rating_Data_Test", "Not_Rating_Data_Train", "Not_UserExperience_Data", "Not_UserExperience_Data_Test", "Not_UserExperience_Data_Train", "Rating_Data", "Rating_Data_Test", "Rating_Data_Train", "UserExperience_Data", "UserExperience_Data_Test", "UserExperience_Data_Train"]

for table in tables:
    dbcur.execute('SELECT id, comment, stopwords_removal, stopwords_removal_lemmatization FROM {}'.format(table))
    
    for (id, comm, sw_orig, sw_lemm_orig) in dbcur :
        if (comm is not None) :
            lower = comm.lower()
            exp = expandContractions(lower)
            decoded = exp.decode('utf-8', errors = 'ignore')  #ugly hack from orig codebase
            words = tok.tokenize(decoded)
            words_filtered = [lemm.lemmatize(w, 'v') for w in words if w not in stop_words]
            comm_sw_new = ' '.join(words_filtered)

            # print('OURS: {}'.format(comm_sw_new))
            # print('ORIG: {} '.format(sw_lemm_orig))
            #print("---------------------------------")
            
            #UPDATE DATA - be careful :)
            #dbcur.execute('UPDATE {} SET stopwords_removal_lemmatization="{}" WHERE id={} '.format(table, comm_sw_new, id))
    
    print ('Table: {} DONE'.format(table))

db.commit()