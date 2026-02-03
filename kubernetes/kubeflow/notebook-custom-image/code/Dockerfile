# Use Kubeflow's official notebook image as base
FROM docker.io/kubeflownotebookswg/jupyter-scipy:v1.8.0

# Set working directory
WORKDIR /home/jovyan

# Switch to root to install system packages
USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    vim \
    curl \
    wget \
    build-essential \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /tmp/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Install Jupyter extensions
RUN pip install --no-cache-dir \
    jupyter_contrib_nbextensions \
    jupyter_nbextensions_configurator \
    jupyterlab-git \
    && jupyter contrib nbextension install --sys-prefix \
    && jupyter nbextensions_configurator enable --sys-prefix

# Enable useful Jupyter extensions
RUN jupyter nbextension enable collapsible_headings/main --sys-prefix && \
    jupyter nbextension enable codefolding/main --sys-prefix && \
    jupyter nbextension enable execute_time/ExecuteTime --sys-prefix

# Create directories for ML workflows
RUN mkdir -p /home/jovyan/work/data \
             /home/jovyan/work/models \
             /home/jovyan/work/notebooks \
             /home/jovyan/work/scripts

# Copy custom startup scripts (if any)
# COPY start-notebook.sh /usr/local/bin/

# Set proper permissions
RUN chown -R jovyan:users /home/jovyan

# Switch back to jovyan user
USER jovyan

# Set environment variables
ENV JUPYTER_ENABLE_LAB=yes \
    SHELL=/bin/bash

# Expose Jupyter port
EXPOSE 8888

# Default command
CMD ["sh", "-c", "jupyter lab --notebook-dir=/home/jovyan/work --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password: "${GENERIC_PASSWORD}" --NotebookApp.allow_origin='*' --NotebookApp.base_url=${NB_PREFIX}"]
