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


FROM python:3.11.0-bullseye

# define env vars

ENV FLASK_APP flasky.py
RUN useradd -ms /bin/sh flasky

ENV DEBIAN_FRONTEND=noninteractive


USER root

RUN apt update && apt install -y libtbb2 && rm -rf /var/lib/apt/lists/*


USER flasky

WORKDIR /home/flasky
COPY requirements.txt requirements.txt


ENV PATH="${PATH}:/home/flasky/.local/bin"
ENV FAKER='True'
RUN python -m venv venv
RUN python -m pip install --upgrade pip
RUN venv/bin/pip3 install -r requirements.txt

RUN mkdir out
RUN mkdir predictions
RUN mkdir predictions_file

COPY app app
COPY flasky.py config.py boot.sh ./


# runtime configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
