FROM python:3.12-slim

WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY app.py .
COPY assets/ ./assets/

# Exposer le port utilisé par Streamlit
EXPOSE 8501



# Commande pour démarrer l'application
CMD streamlit run app.py --server.port=$PORT --server.address=0.0.0.0