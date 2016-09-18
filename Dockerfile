FROM python:3.5.2-alpine

COPY powerchart /app/powerchart
WORKDIR /app/powerchart

CMD python main.py