FROM    python:3.10-slim
RUN	mkdir /app
WORKDIR	/app
ADD	requirements.txt /app
RUN     apt update && pip install -r /app/requirements.txt
ADD	main.py /app

