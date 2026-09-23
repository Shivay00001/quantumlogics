# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the 8 pillar directories and the API directory
COPY vq-logics-opt/ ./vq-logics-opt/
COPY vq-logics-crypto/ ./vq-logics-crypto/
COPY vq-logics-ai/ ./vq-logics-ai/
COPY vq-logics-chem/ ./vq-logics-chem/
COPY vq-logics-sim/ ./vq-logics-sim/
COPY vq-logics-fin/ ./vq-logics-fin/
COPY vq-logics-geo/ ./vq-logics-geo/
COPY vq-logics-sys/ ./vq-logics-sys/
COPY vq-logics-api/ ./vq-logics-api/

# Entrypoint shim (vq-logics-api/ is not a valid Python module name)
COPY serve.py ./

# Expose the FastAPI port
EXPOSE 8000

# Run the UQEOS central API
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8000"]
