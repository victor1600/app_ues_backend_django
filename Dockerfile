FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN apt update
RUN apt install -y libmariadb-dev-compat

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
# Added this to prevent error in installing requirements
RUN pip install -U djoser
RUN pip install beautifulsoup4
COPY . .

EXPOSE 8000

