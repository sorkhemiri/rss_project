#! /usr/bin/env bash
if [ $# -eq 0 ]
  then
    echo "Provide a valid Username"
  else
    docker exec -it rss_project_web_1 python generate_db.py $1
fi

