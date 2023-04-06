import csv
from .configs import BASE_DIR
from .models import Course, Participant
from .repositories import (
    TopicRepository,
    CourseRepository,
    UserRepository,
    ParticipantRepository,
    UseCaseRepository,
)


INITIAL_DATA_DIR = BASE_DIR / "initial-csv-data"


def load_raw_data(file_name: str):
    with open(BASE_DIR / "initial-csv-data" / file_name) as csv_file:
        reader = csv.DictReader(csv_file)
        return [row for row in reader]


def get_courses() -> list[Course]:
    raw_course_data = load_raw_data("courses.csv")
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
    raw_participant_data = load_raw_data("participants.csv")
    return [Participant(**row) for row in raw_participant_data]


def exec_initial_load():
    courses = get_courses()
    participants = get_participants()

    # Create Topics
    for course in courses:
        TopicRepository.create_node(course.topic)

    # Create Use-cases
    for course in courses:
        for usecase in course.suitable_for:
            UseCaseRepository.create_node(usecase)

    # Create Courses Only
    for course in courses:
        CourseRepository.create_node(id_=course.id, name=course.title)

    # Create Topic Dependency
    for course in courses:
        CourseRepository.add_relationship_to_topic(course_id=course.id, topic_name=course.topic)

    # Create Requirements
    # RM This for the example
    for course in courses:
        for requirement in course.requirements:
            rel_course = [c.id for c in courses if c.title == requirement][0]
            CourseRepository.add_relationship_to_course(
                source_id=course.id,
                target_id=rel_course,
                rel_type="REQUIRES",
            )

    # Create Suitables
    for course in courses:
        for suitable in course.suitable_for:
            CourseRepository.add_relationship_to_use_case(
                course_id=course.id,
                use_case=suitable,
            )

    # Create Users
    for user in participants:
        UserRepository.create_node(user.user)

    # Create Participants
    for user in participants:
        ParticipantRepository.create_relationship_from_user_to_course(
            user_id=user.user,
            course_id=user.course,
        )
