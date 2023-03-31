FROM python:3.8

WORKDIR /mfmpod
COPY ./*.py .
COPY ./*.json .
COPY ./setup.sh .
RUN mkdir out && \
    chmod +x ./setup.sh && \
    apt-get update && \
    apt-get -y install ffmpeg wget screen && \
    rm -rf /var/lib/apt/lists/*
CMD ["./setup.sh"]
