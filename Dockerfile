FROM selenium/standalone-chrome
ENV PYTHONUNBUFFERED 1

USER root
RUN apt update

RUN apt-get install python3-distutils -y
RUN apt-get install python3-apt -y
RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py

RUN apt install python3-dev build-essential -y
RUN apt install libssl1.1 -y
RUN apt install -y --allow-downgrades libssl1.1=1.1.1f-1ubuntu2
RUN apt install libssl-dev -y
RUN apt install libmysqlclient-dev -y



RUN python3 -m pip install selenium


WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
# Added this to prevent error in installing requirements
RUN pip install -U djoser
RUN pip install beautifulsoup4
COPY . .

RUN chmod 777 docker-entrypoint.sh

EXPOSE 8000

