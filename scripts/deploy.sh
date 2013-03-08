#! /bin/bash

echo "Starting..."
echo "Pulling staging master"
git pull staging master
echo "Pushing staging master"
git push staging master --force

echo "Push production?(y/n) \c"
read  MASTER

if [ $MASTER == "y" ] ; then
    echo "Pushing to origin master"
    git push origin master --force
fi

echo "Done!"