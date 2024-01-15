
build: 
	podman-compose up -d; podman-compose logs -f

reset:
	podman-compose down && podman rmi localhost/asu:latest

rebuild: reset build

redis_start: 
	podman run -d --name redis_localhost --network="host" docker.io/library/redis:alpine
redis_kill:
	podman rm -vf redis_localhost
