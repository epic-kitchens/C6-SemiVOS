FROM python:3.9.7-slim-buster
#RUN pip install --upgrade pip
RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential netcat \
  && apt-get install -y libgl1-mesa-dev libglib2.0-0



ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1


WORKDIR /app

COPY codes ./codes
COPY requirements ./requirements
COPY Dockerfile ./Dockerfile

RUN pip install  --no-cache-dir -r requirements/requirements.txt


# put the command to run your inference script
WORKDIR /app/codes
CMD python dummy_inference.py -s test
