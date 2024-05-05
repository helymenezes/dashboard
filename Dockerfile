FROM ubuntu:latest

# Instale as dependências do sistema operacional
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    git \
    curl \
    software-properties-common

# Adicione o repositório deadsnakes PPA para instalar o Python 3.11
RUN add-apt-repository ppa:deadsnakes/ppa

# Instale o Python 3.11 e as ferramentas de desenvolvimento necessárias
RUN apt-get update && \
    apt-get install -y \
    dpkg-dev \
    python3.11 \
    python3.11-venv

# Crie e ative um ambiente virtual
RUN python3.11 -m venv /opt/venv
RUN /opt/venv/bin/python -m pip install --upgrade pip

# Instale as bibliotecas Python necessárias no ambiente virtual
RUN /opt/venv/bin/pip install streamlit pandas numpy openpyxl googlemaps plotly

# Copie o código fonte do seu aplicativo para a imagem
WORKDIR /app
COPY . /app

# Exponha a porta que o Streamlit usa (padrão: 8501)
EXPOSE 8501

# Comando para executar o aplicativo quando o contêiner for iniciado
CMD ["/opt/venv/bin/python", "-m", "streamlit", "run", "main.py"]
