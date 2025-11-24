# ===== Build stage =====
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first (leverage Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# ===== Final stage =====
FROM python:3.11-slim

WORKDIR /app

# Create non-root user (security best practice)
RUN adduser --disabled-password --gecos '' streamlituser

# Copy Python packages from builder
COPY --from=builder /root/.local /home/streamlituser/.local

# Copy app code
COPY app.py .

# Make sure scripts are in PATH
ENV PATH=/home/streamlituser/.local/bin:$PATH

# Switch to non-root user
USER streamlituser

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]