FROM python:3-alpine
RUN mkdir /ANZ-Code
WORKDIR /ANZ-Code
COPY requirements.txt /my_flask_app
RUN pip install - upgrade pip
RUN pip install - no-cache-dir -r requirements.txt
COPY . /ANZ-Code
EXPOSE 5000
CMD [ "flask", "--app", "apis.py". "run" ]