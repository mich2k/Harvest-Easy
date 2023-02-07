# syntax=docker/dockerfile:1

#
#
#
#    EDIT ONLY IF YOU KNOW WHAT YOU ARE DOING
#
#
#
#
#
#
#
#    EDIT ONLY IF YOU KNOW WHAT YOU ARE DOING
#
#
#
#
#
#
#    EDIT ONLY IF YOU KNOW WHAT YOU ARE DOING
#
#
#
#
#

#FROM python:3.11.0-alpine
#ENV FLASK_APP flasky.py
#ENV FLASK_CONFIG docker
#RUN adduser -D flasky
#USER flasky
#
#WORKDIR /home/flasky
#COPY requirements requirements
#RUN python -m venv venv
#RUN venv/bin/pip install -r requirements/docker.txt
#
#COPY app app
##COPY migrations migrations
#COPY flasky.py config.py boot.sh ./
## runtime configuration
#EXPOSE 5000
#ENTRYPOINT ["./boot.sh"]
#


FROM python:3.11.0-bullseye

# define env vars

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG docker
RUN useradd -ms /bin/sh flasky
USER flasky

WORKDIR /home/flasky
COPY requirements.txt requirements.txt


ENV PATH="${PATH}:/home/flasky/.local/bin"
ENV FAKER='True'
RUN python -m venv venv
RUN  python -m pip install --upgrade pip
RUN  python3 -m pip install --upgrade pip

RUN venv/bin/pip3 install -r requirements.txt

RUN mkdir out
#RUN mkdir predictions

#COPY app app
##COPY migrations migrations
# manca config.py


COPY app app
COPY flasky.py config.py boot.sh ./


# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
