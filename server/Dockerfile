FROM python:3.10

ENV PYTHONUNBUFFERED 1 
WORKDIR /app 
# Copy requirements from host, to docker container in /app 
EXPOSE 8000 
COPY ./requirements.txt .
# Copy everything from ./src directory to /app in the container
COPY ./ . 
RUN pip install -r requirements.txt
# Run the application in the port 8000
CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app:app"]