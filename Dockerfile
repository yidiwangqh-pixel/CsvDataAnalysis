# Base image
FROM python:3.9-slim

# work directory
WORKDIR /app

# copy files
COPY . /app

# pip install
RUN pip install --no-cache-dir --no-warn-script-location openai pyyaml
RUN pip install --no-cache-dir --no-warn-script-location pandas numpy matplotlib pillow

# run script
CMD ["python", "DataAnalysis.py"]