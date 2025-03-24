# Which base image is used (in this case a simple python image)
FROM python:3.13.2

# The workdirectory where all files will be copied.
WORKDIR /app

# copy all from source to destination
COPY student_api.py .
COPY create_db.py .
COPY student.py .
COPY requirements.txt .
COPY config.py .
COPY student.ini .

# install all required modules described in requirements.txt
RUN pip install -r requirements.txt

# Expose the port that the application listens on.
EXPOSE 81

# Run the application.
ENTRYPOINT ["python"]
CMD ["student_api.py"]