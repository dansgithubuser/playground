build a named image from a Dockerfile:
`docker build -t my_image .`

run a container based on an image:
`docker run --name my_container --detach my_image:latest`

get a shell in a container:
`docker exec -it my_container /bin/bash`
