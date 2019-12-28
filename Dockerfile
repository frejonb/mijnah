FROM python:3.6.7-stretch

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip

RUN mkdir /opt/src
COPY . /opt/src
RUN cd /opt/src \
 && make install-test

WORKDIR /opt/src