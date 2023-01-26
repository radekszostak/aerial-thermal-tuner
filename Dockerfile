FROM debian
RUN apt-get update
RUN apt-get install -y python3.9
RUN apt-get install -y python3-pip
RUN apt-get install -y git
RUN apt-get install -y exiftool
RUN apt-get install -y python3-opencv
#---
RUN apt-get install -y gdal-bin
RUN apt-get install -y libgdal-dev
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN pip install GDAL
RUN pip install gdal-utils
#---
ENV LOCALTILESERVER_CLIENT_PREFIX='proxy/{port}'
#---
RUN pip install jupyterlab
RUN pip install jupyter-server-proxy
RUN pip install rasterio --no-binary rasterio
RUN pip install rioxarray
RUN pip install geopandas
RUN pip install ipyleaflet
RUN pip install leafmap
RUN pip install xarray_leaflet
RUN pip install localtileserver
RUN pip install rasterstats
RUN pip install scipy
RUN pip install opencv-contrib-python
RUN pip install ipympl 
RUN pip install memory_profiler
RUN pip install line_profiler
RUN pip install rasterstats
RUN pip install torch
RUN pip install networkx
RUN pip install suncalc
RUN pip install pyexiftool
RUN pip install ipycanvas
#---

ENTRYPOINT ["jupyter", "lab", "--port=8888", "--ip=0.0.0.0", "--allow-root", "--no-browser", "--NotebookApp.token=''", "--NotebookApp.password=''"]
