#!/bin/bash
sudo raspistill -o /home/isis/ISIS-frontend/image.jpg
sleep 5
scp  /home/isis/ISIS-frontend/image.jpg isis@192.168.255.54:/home/isis/Afbeeldingen/image.jpg
