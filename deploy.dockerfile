FROM python:3.9
# Set the working directory to /app
WORKDIR /robot

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \ 
    libffi-dev \ 
    python3-dev \
    python3-pip

    
# Copy the current directory contents into the container at /app
COPY . /robot

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "main.py"]