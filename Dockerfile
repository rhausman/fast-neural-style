FROM python:3.9-slim-buster

ENV VIRTUAL_ENV=/opt/venv
# make the venv, and append to the PATH
RUN python -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
COPY ./requirements.txt ./requirements.txt
RUN pip install numpy
RUN pip install -r "requirements.txt" --verbose

COPY . .

ENTRYPOINT [ "uvicorn", "api:app", "--reload" ]