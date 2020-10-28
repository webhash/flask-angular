# flask-angular
experiments with flask, angular , redis, nginx and docker

for flask app 

docker build -t flask-app:v0 . --no-cache 
docker run -it -p 9999:9999 --link redis flask-app:v0


for angular app

docker build -t angular-app:v0 . --no-cache
docker run -it -p 8888:8888 angular-app:v0