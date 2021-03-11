BUILDING

First build app development docker with these command,

This command build image
~$ docker build -t youtube-bot .

For build to selenium-hub first you need to add docker network.
~$ docker network create grid

This command up container with builded image
~$ docker run -it --net grid -v ${PWD}:/app -w /app --name youtube-bot youtube-bot

After that you need to build selenium-hub and selenium-node.

Then add selenium-hub image and up container
~$ docker run -d -p 4444:4444 --net grid --name selenium-hub selenium/hub

Then add selenium-node image and up container
~$ docker run -d --net grid -e HUB_HOST=selenium-hub -v /dev/shm:/dev/shm --name selenium-node selenium/node-firefox:latest

For debugging with vnc viewer add selenium-node-debug image and up container
~$ docker run -d --net grid -e HUB_HOST=selenium-hub -v /dev/shm:/dev/shm --name selenium-node selenium/node-firefox-debug:latest
VNC CONNECTION PASS = secret
172.18.0.4:5900

Open the grid console on the browser
http://localhost:4444/grid/console
and find the ip adress and port number of selenium-client
then, start the script on youtube-bot container
~$ python bot.py
