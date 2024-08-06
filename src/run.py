import json
import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv

from api import Client

load_dotenv()

OUTPUT_DATA_DIR_PATH = Path(__file__).resolve().parent.parent / "output_data"
OUTPUT_DATA_DIR_PATH.mkdir(exist_ok=True)

TEACHERS_WITH_NO_CLASSES_FILEPATH = (
    OUTPUT_DATA_DIR_PATH / "teachers_with_no_classes.json"
)
TEACHERS_WITH_CLASSES_BUT_NO_STUDENTS_FILEPATH = (
    OUTPUT_DATA_DIR_PATH / "teachers_with_classes_but_no_students.json"
)
TEACHERS_WITH_CLASSES_AND_STUDENTS_FILEPATH = (
    OUTPUT_DATA_DIR_PATH / "teachers_with_classes_and_students.json"
)


def fetch_data() -> Dict[str, List[Dict[str, Any]]]:
    teachers_with_no_classes: List[Dict[str, Any]] = []
    teachers_with_classes_but_no_students: List[Dict[str, Any]] = []
    teachers_with_classes_and_students: List[Dict[str, Any]] = []

    client = Client(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))
    teachers = client.get_all_teachers(params={"filter": "email!=''", "limit": 1000})

    for teacher in teachers:
        teacher_data = teacher.to_dict()
        classes = client.get_classes_for_teacher(teacher.sourced_id)

        if len(classes) == 0:
            teachers_with_no_classes.append(teacher_data)
            continue

        teacher_data["classes"] = []
        for klass in classes:
            klass_data = klass.to_dict()
            students = client.get_students_for_class(klass.sourced_id)

            if len(students) > 0:
                klass_data["students"] = [student.to_dict() for student in students]

            teacher_data["classes"].append(klass_data)

        if any("students" in klass for klass in teacher_data["classes"]):
            teachers_with_classes_and_students.append(teacher_data)
        else:
            teachers_with_classes_but_no_students.append(teacher_data)

    return {
        "teachers_with_no_classes": teachers_with_no_classes,
        "teachers_with_classes_but_no_students": teachers_with_classes_but_no_students,
        "teachers_with_classes_and_students": teachers_with_classes_and_students,
    }


def persist_data(data: Dict[str, List[Dict[str, Any]]]) -> None:
    TEACHERS_WITH_NO_CLASSES_FILEPATH.write_text(
        json.dumps(data["teachers_with_no_classes"], indent=4) + "\n"
    )

    TEACHERS_WITH_CLASSES_BUT_NO_STUDENTS_FILEPATH.write_text(
        json.dumps(data["teachers_with_classes_but_no_students"], indent=4) + "\n"
    )

    TEACHERS_WITH_CLASSES_AND_STUDENTS_FILEPATH.write_text(
        json.dumps(data["teachers_with_classes_and_students"], indent=4) + "\n"
    )


if __name__ == "__main__":
    print("Fetching data...")
    data = fetch_data()

    print()
    print("Persisting fetched data...")
    persist_data(data)

    print()
    print("Data fetched and persisted successfully to the following file:")
    print(f"* {TEACHERS_WITH_NO_CLASSES_FILEPATH}")
    print(f"* {TEACHERS_WITH_CLASSES_BUT_NO_STUDENTS_FILEPATH}")
    print(f"* {TEACHERS_WITH_CLASSES_AND_STUDENTS_FILEPATH}")
    print()
