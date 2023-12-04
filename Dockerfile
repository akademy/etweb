FROM python:3.10 
ENV DockerHOME=/home/app/server 

RUN apt-get update \
	&& apt-get install -y --no-install-recommends \
		mariadb-client

RUN mkdir -p $DockerHOME  
 
WORKDIR $DockerHOME  
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

RUN pip install --upgrade pip  
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt 

COPY . $DockerHOME  

EXPOSE 8000 
CMD python ./web/manage.py runserver  