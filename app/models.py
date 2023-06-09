from dataclasses import dataclass


@dataclass
class CourseEssential:
    id: int
    title: str
    topic: str


@dataclass
class Course:
    id: int
    title: str
    topic: str
    requirements: list[str]
    suitable_for: list[str]


@dataclass
class Participant:
    user: int
    course: int
