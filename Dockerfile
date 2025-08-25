 # app/Dockerfile
FROM python:3.12-slim
 
WORKDIR /app
 
RUN apt-get update && apt-get install -y \
  build-essential \
  curl \
  software-properties-common \
  git \
  python3-pip \
  python3-lxml \
  python3-pil \
  xvfb \
  libgl-dev \
&& rm -rf /var/lib/apt/lists/*

RUN curl -LO https://files.pythonhosted.org/packages/b4/8c/4065950f9d013c4b2e588fe33cf04e564c2322842d84dbcbce5ba1dc28b0/PyQt5-5.15.11-cp38-abi3-manylinux_2_17_x86_64.whl

RUN pip install PyQt5-5.15.11-cp38-abi3-manylinux_2_17_x86_64.whl

# RUN pip install PyQt5

RUN pip install git+https://github.com/etetoolkit/ete.git@3.1.3

RUN pip install streamlit

RUN pip install pandas

RUN pip install numpy

RUN pip install lxml

# RUN pip3 install -r requirements.txt

ADD . /app/cohn-treemaker/

WORKDIR /app/cohn-treemaker/

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "1_🐨_Homepage.py"]
