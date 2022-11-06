docker build -t aerial-thermal-tuner .
docker run ^
-v %cd%:/home/workdir ^
-v %cd%/.docker/.vscode-server:/root/.vscode-server ^
-v %cd%/.docker/.vscode-server-insiders:/root/.vscode-server-insiders ^
-w /home/workdir ^
-p 8888:8888 ^
-e LD_LIBRARY_PATH=/home/workdir/lib ^
--rm ^
aerial-thermal-tuner