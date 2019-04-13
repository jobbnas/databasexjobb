FROM python:3.7.1-alpine


COPY . /databasexjobb

WORKDIR /databasexjobb


RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]

