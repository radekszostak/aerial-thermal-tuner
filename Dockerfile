FROM debian
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-pip \
    git \
    exiftool \
    python3-opencv \
    gdal-bin \
    libgdal-dev

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal C_INCLUDE_PATH=/usr/include/gdal LOCALTILESERVER_CLIENT_PREFIX='proxy/{port}'

RUN pip install GDAL gdal-utils
RUN pip install jupyterlab jupyter-server-proxy
RUN pip install shapely --no-binary shapely
RUN pip install rasterio --no-binary rasterio
RUN pip install cartopy --no-binary cartopy
RUN pip install rioxarray
RUN pip install geopandas
RUN pip install rasterstats
RUN pip install scipy
RUN pip install opencv-contrib-python
RUN pip install torch
RUN pip install networkx
RUN pip install suncalc

#---

ENTRYPOINT ["jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
