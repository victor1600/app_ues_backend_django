FROM python:3.9
ENV PYTHONUNBUFFERED 1
RUN apt update

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

EXPOSE 8000

CMD ["./docker-entrypoint.sh"]
