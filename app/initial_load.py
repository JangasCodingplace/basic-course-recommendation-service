import csv
from config import BASE_DIR

DATA_DIR = BASE_DIR / "initial-csv-data"


def load_data(file_name: str):
    with open(DATA_DIR / file_name) as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


if __name__ == "__main__":
    data = load_data("courses.csv")
    print()
