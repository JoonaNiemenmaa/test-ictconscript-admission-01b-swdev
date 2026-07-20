FROM        python:3.13
WORKDIR     /code
COPY        ./requirements.txt requirements.txt
RUN         pip install --no-cache-dir --upgrade -r requirements.txt
COPY        ./backend.py .
COPY        ./insert_sample_data.py .
COPY        ./data.json .
RUN         python3 insert_sample_data.py
CMD         [ "fastapi", "run", "--entrypoint", "backend:app" ]
