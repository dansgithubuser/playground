FROM python:latest

RUN pip install psutil

COPY print_styled.py .
COPY use_cpu.py .

ENTRYPOINT python -u use_cpu.py
