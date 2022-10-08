FROM ubuntu
RUN  apt-get update
RUN apt-get install -y wget
RUN apt-get install -y git

RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p /miniconda
ENV PATH=$PATH:/miniconda/condabin:/miniconda/bin
RUN rm Miniconda3-latest-Linux-x86_64.sh

RUN git clone https://radekszostak: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@github.com/radekszostak/aerial-thermal-tuner /home/aerial-thermal-tuner
WORKDIR /home/aerial-thermal-tuner
RUN conda env create -f environment.yml
SHELL ["conda","run","-n","app-env","/bin/bash","-c"]
EXPOSE 8888
ENTRYPOINT ["jupyter-lab"]