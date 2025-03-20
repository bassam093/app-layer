"""CLI for student management."""

import argparse
import sys

from config import CONFIG
from student_api_shim import add_student, delete_student, update_student, list_of_students, get_student

def display_student_list():
    students = list_of_students()
    for student in students:
        print(f"{student['first_name']} {student['last_name']} - Email: {student['email']} - Phone: {student['phone']}")

def main():
    """Execute main function."""
    parser = argparse.ArgumentParser()
    operations = parser.add_mutually_exclusive_group(required=True)
    operations.add_argument("-a", "--add", action="store_true")
    operations.add_argument("-l", "--list", action="store_true")
    parser.add_argument("-s", "--surname")
    parser.add_argument("-f", "--firstname")
    parser.add_argument("-e", "--email")
    parser.add_argument("-p", "--phone")
    arguments = parser.parse_args()

    if arguments.list:
        display_student_list()

    if arguments.add:
        new_student_id = add_student(arguments.firstname, arguments.surname, arguments.email, arguments.phone)
        print(f"Student added with ID: {new_student_id}")

    return 0

# --- Program entry ---
if __name__ == "__main__":
    sys.exit( main() )
