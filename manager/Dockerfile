FROM registry.access.redhat.com/ubi10/python-312-minimal:10.0-1750857030

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY manager/ ./manager/

RUN pip install -r manager/requirements.txt

EXPOSE 5000

CMD ["python", "-m", "manager.main"]
