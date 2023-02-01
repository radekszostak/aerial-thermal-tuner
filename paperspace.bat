docker build -t rszostak/aerial-thermal-tuner:local -f Dockerfile_local .
docker push rszostak/aerial-thermal-tuner:local
docker build -t rszostak/aerial-thermal-tuner:paperspace -f Dockerfile_paperspace .
docker push rszostak/aerial-thermal-tuner:paperspace