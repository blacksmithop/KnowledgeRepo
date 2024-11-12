FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip install torch==2.3.0+cpu -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8001"]