# Use an official Python image as the base
FROM python:3.13.2

# Set working directory
WORKDIR /app

# Copy necessary files
COPY static .
COPY templates .
COPY student_frontend.py .
COPY student_api_shim.py .
COPY requirements.txt .
COPY config.py .
COPY student.ini .

# install all required modules described in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 80

# Run the application.
ENTRYPOINT ["python"]
CMD ["student_frontend.py"]