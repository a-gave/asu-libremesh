## utils
rm -rf /run/user/1000/podman.sock
podman system service --time=0 "unix://$CONTAINER_SOCK" &

chown -R 100471:$(id -u) grafana_data 
chown -R 100012:100012 squid

