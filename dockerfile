# Use an official Python runtime as the base image
FROM python:3.9
# Set metadata labels for best practices
LABEL authors="Adi Golan,George Pickers"
LABEL org.opencontainers.image.name="loggremlin"

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . .

# Install OpenTelemetry dependencies
RUN pip install --no-cache-dir \
    opentelemetry-api \
    opentelemetry-sdk \
    opentelemetry-exporter-otlp-proto-grpc

# Define the command to run the app using CMD
CMD ["python", "loggremlin.py"]