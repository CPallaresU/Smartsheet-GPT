FROM python:3.11.0-bullseye

RUN apt-get update && apt-get install -y supervisor xvfb \
    && mkdir -p /home/logs/

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR /code
COPY . .

COPY conf.d /etc/supervisor/conf.d 
#El supervisor va a trabajar con el conf.d


COPY requirements.txt .
RUN pip install -r requirements.txt