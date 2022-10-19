FROM python:3.8.3-alpine

RUN apk --update add \
curl \
musl-dev \
linux-headers \
build-base \
libffi-dev \
gcc \
ffmpeg

RUN pip install --upgrade pip
RUN pip install PyNaCl 
RUN pip install -U "discord.py[voice]"

WORKDIR /yomiage_VOICEVOX

CMD ["/bin/ash"]