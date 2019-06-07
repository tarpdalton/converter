FROM ubuntu:latest
EXPOSE 80
RUN apt-get update -y
RUN apt-get install -y python3-pip python3.7-dev build-essential ffmpeg
RUN pip3 install Flask youtube-dl
WORKDIR /app
COPY . /app
ENTRYPOINT ["python3"]
CMD ["app.py"]
