sudo java -mx512m -jar ../../tools/cooja/dist/cooja.jar -nogui='../random-45.csc' -contiki='../..' > cooja.log &
sleep 6
sudo ./border-router-udp-server.native fd00::1/64 -a 127.0.0.1 > border.log  &
sudo python3 particle-lazy.py > part.log &
