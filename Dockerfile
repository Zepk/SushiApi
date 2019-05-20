FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN mkdir /root/.ssh
RUN ssh-keyscan -t rsa fierro.ing.puc.cl >> ~/.ssh/known_hosts
RUN pip install -r requirements.txt
COPY . /code/
