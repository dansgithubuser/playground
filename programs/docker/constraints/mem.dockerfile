FROM python:latest

RUN pip install psutil

COPY print_styled.py .
COPY use_memory.py .

ENTRYPOINT python -u use_memory.py
