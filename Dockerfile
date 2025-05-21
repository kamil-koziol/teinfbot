FROM python:3.10-bookworm

WORKDIR /app

# Install pip + build tools
RUN pip install --upgrade pip setuptools wheel

# Copy source and config first — they’re both needed for pip install .
COPY pyproject.toml ./
COPY src/ ./src

# Now install your package
RUN pip install .

# Set the command to run your script
CMD ["python", "src/main.py"]
