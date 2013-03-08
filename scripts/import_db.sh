#! /bin/bash

#sudo chmod +x filename.bin
#exports the production database and imports into the dev database

echo "Starting"

echo "Exporting data..."
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME > dumpfile.sql

echo "Dropping old data"
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e DROP DATABASE $MYSQL_NAME_DEV; 
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e CREATE DATABASE $MYSQL_NAME_DEV;

echo "Importing data..."

echo "Importing data to dev..."
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME_DEV < dumpfile.sql;

echo "Importing data locally..."

echo "Cleaning up..."
rm dumpfile.sql

echo "Removing user access to dev site..."
python manage.py set_users_inactive

echo "Done."
