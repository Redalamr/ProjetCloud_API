FROM python:3.12-slim

RUN useradd -m appuser

WORKDIR /home/appuser

USER appuser

COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app.py .

EXPOSE 5000

CMD ["python", "app.py"]
