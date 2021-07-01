sudo java -mx512m -jar ../tools/cooja/dist/cooja.jar -nogui='../../examples/scripted.csc' -contiki='../../' &
sleep 100
sudo python3 particle.py &
sudo ./border-router-udp-server.native fd00::1/64 -a 127.0.0.1 &