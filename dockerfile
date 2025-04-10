# Base image
FROM python:3.11.2

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt ./


# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m textblob.download_corpora && \
    python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('stopwords')" && \
    pip install --upgrade pip && \
    python -m spacy download en_core_web_sm



# Copy project files
COPY . .

# Create directories for logs and temp files
RUN mkdir -p BackEnd/logs
RUN mkdir -p BackEnd/temp
RUN mkdir -p BackEnd/visualizations

# Set environment variables
ENV PYTHONPATH=/app

# Expose the port your API will run on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "BackEnd.src.main:app", "--host", "0.0.0.0", "--port", "8000"]