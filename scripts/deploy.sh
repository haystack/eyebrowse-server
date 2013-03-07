#! /bin/bash

echo "Starting..."
echo "Pulling staging staging"
git pull staging staging
echo "Pushing staging staging"
git push staging staging
echo "Pushing staging to staging-master"
git push staging staging:master --force


echo "Push production?(y/n) \c"
read  MASTER

if [ $MASTER == "y" ] ; then
    git checkout master
    git fetch staging
    git reset --hard staging/master
    echo "Pusing to origin master"
    git push origin master --force
fi

git checkout staging

echo "Done!"