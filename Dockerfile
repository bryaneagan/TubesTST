FROM python:3.9.0
WORKDIR /TubesTST
COPY requirements.txt /TubesTST/requirements.txt
RUN pip install -r requirements.txt
COPY . /TubesTST
RUN pip install uvicorn
CMD [ "uvicorn", "src.main:app" , "--host", "0.0.0.0", "--port", "8000", "--reload"]
