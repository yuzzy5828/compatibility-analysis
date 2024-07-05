# compatibility analysis
This repository was created for the UTokyo class. You can successfully complete this project by following the instructions below.

attention: This repository is suited for only ubuntuOS.

## Prerequisites
install Docker and docker-compose. If you haven't installed them yet, execute:
```
curl https://get.docker.com | sh
sudo usermod -aG docker $USER
sudo systemctl start docker
sudo systemctl enable docker
sudo curl -L https://github.com/docker/compose/releases/download/1.16.1(you have to find the latest version)/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## how to build container
```
docker-compose build
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix --device /dev/video0:/dev/video0 frontend sh -c 'npx create-react-app site --template typescript'
docker-compose up -d
```

## usage
if you want to edit the frontend codes, execute:
```
docker-compose exec frontend bash
```
after that, visit http://localhost:3000/ .

if you want to edit the backend codes, execute:
```
docker-compose exec backend bash
```
when you execute this project, 
1. execute:
```
python3 main.py
```
2. visit http://localhost:3000/ .
3. put the buttom in the page, which reset the data in http://127.0.0.1:3001/ and execute (or re-execute) the main function.
