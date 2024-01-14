# Use an official base image from Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /genai-llm

# Copy the local contents into the container at /app
COPY . /genai-llm

# Install dependencies (if needed) using pip or package manager
RUN pip install -r requirements.txt

# Expose the port on which the application will run
EXPOSE 8080

# Specify the command to run your application
CMD streamlit run --server.port 8080 --server.enableCORS false app.py
