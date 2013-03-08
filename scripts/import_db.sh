#! /bin/bash

#sudo chmod +x filename.bin
#exports the production database and imports into the dev database

echo "Starting"

echo "Exporting data..."
<<<<<<< HEAD
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME > dumpfile.sql
=======
mysqldump -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME > dumpfile.sql;
>>>>>>> 588e0d9366546d1ca8694d3242f9618e8bd5a3db

echo "Dropping old data"
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e DROP DATABASE $MYSQL_NAME_DEV; 
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD -e CREATE DATABASE $MYSQL_NAME_DEV;

echo "Importing data..."

<<<<<<< HEAD
echo "Importing data to dev..."
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME_DEV < dumpfile.sql;

echo "Importing data locally..."
=======
echo "Import to dev..."
mysql -h $MYSQL_HOST -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_NAME_DEV < dumpfile.sql;

echo "Importing to local..."
>>>>>>> 588e0d9366546d1ca8694d3242f9618e8bd5a3db
mysql -h $MYSQL_HOST_LOCAL -u $MYSQL_USER_LOCAL -p$MYSQL_PASSWORD_LOCAL $MYSQL_NAME_LOCAL < dumpfile.sql;

echo "Cleaning up..."
rm dumpfile.sql

echo "Removing user access to dev site..."
python manage.py set_users_inactive

echo "Done."
