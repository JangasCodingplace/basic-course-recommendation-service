import csv
from config import BASE_DIR
from models import Participant, Course

DATA_DIR = BASE_DIR / "initial-csv-data"


def load_data(file_name: str):
    with open(DATA_DIR / file_name) as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def get_courses() -> list[Course]:
    raw_course_data = load_data("courses.csv")
    return [
        Course(
            id=row["id"],
            title=row["title"],
            topic=row["topic"],
            requirements=row["requirements"].split(),
            suitable_for=row["suitable_for"].split(),
        )
        for row in raw_course_data
    ]


def get_participants() -> list[Participant]:
    raw_course_data = load_data("participants.csv")
    return [Participant(**row) for row in raw_course_data]


if __name__ == "__main__":
    courses = get_courses()
    participants = get_participants()
    print()
