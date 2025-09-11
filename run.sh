#!/usr/bin/env bash

downloadSelf(){
    if [ ! -f "run.sh" ]; then
        wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/run.sh -O run.sh
        chmod +x run.sh
    fi
}

downloadDockerCompose(){
    if [ ! -f "docker-compose.yml" ]; then
        if curl -s http://cip.cc | grep -q "中国"; then
            wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/docker-compose_cn.yml -O docker-compose.yml
        else
            wget https://raw.githubusercontent.com/SecAegis/SecAutoBan/main/docker-compose.yml -O docker-compose.yml
        fi
    fi
}

createPassword(){
    if [ ! -f ".env" ]; then
        touch .env
    fi
    if ! grep -q "db_password=" .env; then
        echo "db_password=$(uuidgen | sed 's/-//g')" >> .env
    fi
    if ! grep -q "mq_password" .env; then
        echo "mq_password=$(uuidgen | sed 's/-//g')" >> .env
    fi
}

exec() {
    if [ "$1" = "changeUserPassword" ]
    then
        docker compose exec sec-auto-ban /sec_report $1 $2 $3 $4 $5
    fi
}

run(){
    downloadDockerCompose
    createPassword
    docker compose up -d
}

stop(){
    docker compose down
}

update(){
    if [ -f "docker-compose.yml" ]; then
         rm docker-compose.yml
         downloadDockerCompose
    fi
    if [ -f "run.sh" ]; then
         rm run.sh
         downloadSelf
    fi
    docker compose pull
}

if [ "$1" = "stop" ]
then
    stop
    exit
elif [ "$1" = "update" ]
then
    update
    exit
elif [ "$1" = "exec" ]
then
    exec $2 $3 $4 $5 $6
    exit
fi

run
