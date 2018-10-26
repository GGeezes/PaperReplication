# PaperReplication
```
sudo apt-get install mysql-server
sudo apt-get install libmysqlclient-dev
sudo service mysql start
echo "create database `re2015_training_set`" | mysql -p -u root
mysql -p -u root re2015_training_set < Re2015_Training_Set.sql
pip install -r requirements.txt
```
TEST
