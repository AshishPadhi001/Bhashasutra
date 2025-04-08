@echo off

echo "DOCKER DOWN"

docker compose down --remove-orphans

echo "DOCKER UP"

docker compose up --build -d

echo "DOCKER PS"

docker ps
