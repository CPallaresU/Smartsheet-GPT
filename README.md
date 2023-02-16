docker build -t hola-image .

docker container kill hola-container

docker container rm hola-container

docker create --name hola-container -it \
    -v $(pwd):/code \
    -v $(pwd)/conf.d:/etc/supervisor/conf.d \
    -v /code/venv \
    hola-image

docker start hola-container

docker exec -it hola-container bash
docker exec -it hola-container service supervisor start

