FROM python:3.10-slim
WORKDIR /usr/src/backend

COPY ./docker/backend/requirement.txt .
RUN pip install --no-cache-dir --upgrade -r requirement.txt

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY /src/backend/run.py /backend/
COPY /src/backend/scripts /backend/scripts

RUN echo 'export QT_X11_NO_MITSHM=1' >> ~/.bashrc && \
    source ~/.bashrc

CMD ["uvicorn", "run:app", "--reload", "--host", "0.0.0.0", "--port", "3001"]
