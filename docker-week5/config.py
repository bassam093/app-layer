import configparser

CONFIG = configparser.ConfigParser()
CONFIG.read("student.ini")

CONFIG = {
    "database": {
        "name": "/app/db/students.db"  # Path inside the container
    }
}

