FROM python:3.11-slim

# katalog roboczy w kontenerze
WORKDIR /app

# skopiuj źródła aplikacji
COPY app-src/ /app/

# zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# zmienne środowiskowe dla Flaska
ENV FLASK_APP=app.py

EXPOSE 5000

# uruchom aplikację
CMD ["python", "app.py"]
