#! /bin/bash

echo "Starting..."
echo "Pulling staging"
git pull staging
echo "Pushing staging"
git push staging

echo "Push production?(y/n) \c"
read  MASTER

if [ $MASTER == "y" ] ; then
    git checkout master
    git fetch staging
    git reset --hard staging/master
    echo "Pushing to origin master"
    git push origin master --force
fi

git checkout staging

echo "Done!"