FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN apt update
RUN apt install -y libmariadb-dev-compat

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

