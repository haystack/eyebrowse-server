#! /bin/bash

#sudo chmod +x filename.bin
#exports the production database and imports into the dev database

echo "Starting"

echo "Exporting data..."
mysqldump -h$MYSQL_HOST -u$MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME --set-gtid-purged=OFF > dumpfile.sql

echo "Dropping old data"

echo "Dropping old data dev"
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e DROP DATABASE $MYSQL_NAME_DEV; 
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e CREATE DATABASE $MYSQL_NAME_DEV;


echo "Dropping old data local"
mysql -h $MYSQL_HOST_LOCAL -u $MYSQL_USER_LOCAL -p$MYSQL_PASSWORD_LOCAL -e DROP DATABASE $MYSQL_NAME_LOCAL; 
mysql -h $MYSQL_HOST_LOCAL -u $MYSQL_USER_LOCAL -p$MYSQL_PASSWORD_LOCAL -e CREATE DATABASE $MYSQL_NAME_LOCAL;

echo "Importing data..."

echo "Importing data to dev..."
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME_DEV < dumpfile.sql;

echo "Importing data locally..."
mysql -h $MYSQL_HOST_LOCAL -u $MYSQL_USER_LOCAL -p$MYSQL_PASSWORD_LOCAL $MYSQL_NAME_LOCAL < dumpfile.sql;

echo "Cleaning up..."
rm dumpfile.sql

echo "Removing user access to dev site..."
python manage.py set_users_inactive

echo "Done."
