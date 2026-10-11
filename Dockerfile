# Use a lightweight Python 3.11 base image
FROM python:3.11-slim

# Set /app as the working directory inside the container
WORKDIR /app

# Install Linux process monitoring utilities such as top and ps
# (--no-install-recommends skips optional packages to keep the image small)
RUN apt-get update \
    && apt-get install -y --no-install-recommends procps \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python dependencies file before the source code, so that this
# layer and the next one stay cached as long as requirements.txt is unchanged
COPY requirements.txt ./

# Install the required Python dependencies without caching package files
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code last, since it changes the most often
COPY src/ ./src/

# Add the source directory to Python's module search path
ENV PYTHONPATH=/app/src
