docker build -t aerial-thermal-tuner .
call start cmd /C docker run ^
-v %cd%:/home/workdir ^
-v %cd%/.docker/.vscode-server:/root/.vscode-server ^
-v %cd%/.docker/.vscode-server-insiders:/root/.vscode-server-insiders ^
-w /home/workdir ^
-p 8888:8888 ^
-e LD_LIBRARY_PATH=/home/workdir/lib ^
--rm ^
--shm-size 8G ^
aerial-thermal-tuner