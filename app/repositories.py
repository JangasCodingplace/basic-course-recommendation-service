from neo4j import GraphDatabase
from configs import NEO4J


class Neo4j:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            f"bolt://{NEO4J.host}:{NEO4J.port}",
            auth=(NEO4J.username, NEO4J.password),
        )


neo4j = Neo4j()


class TopicRepository:
    @staticmethod
    def create_node(name: str):
        with neo4j.driver.session() as session:
            session.run("MERGE (t:Topic {name: $name})", name=name)


class UseCaseRepository:
    @staticmethod
    def create_node(name: str):
        with neo4j.driver.session() as session:
            session.run("MERGE (u:UseCase {name: $name})", name=name)


class CourseRepository:
    @staticmethod
    def create_node(id_: int, name: str):
        with neo4j.driver.session() as session:
            session.run("MERGE (c:Course {id: $id, name: $name})", id=id_, name=name)

    @staticmethod
    def add_relationship_to_topic(course_id: int, topic_name: str):
        with neo4j.driver.session() as session:
            session.run(
                """
                MATCH (c:Course {id: $course_id}), (t:Topic {name: $topic_name})
                MERGE (c)-[:BELONGS_TO]->(t)
                """,
                course_id=course_id,
                topic_name=topic_name,
            )

    @staticmethod
    def add_relationship_to_use_case(course_id: int, use_case: str):
        with neo4j.driver.session() as session:
            session.run(
                """
                MATCH (c:Course {id: $course_id}), (u:UseCase {name: $use_case})
                MERGE (c)-[:SUITABLE_FOR]->(u)
                """,
                course_id=course_id,
                use_case=use_case,
            )


class UserRepository:
    @staticmethod
    def create_node(id_: int):
        with neo4j.driver.session() as session:
            session.run("MERGE (u:User {id: $id})", id=id_)


class ParticipantRepository:
    @staticmethod
    def create_relationship_from_user_to_course(user_id: int, course_id: int):
        with neo4j.driver.session() as session:
            session.run(
                """
                MATCH (u:User {id: $user_id}), (c:Course {id: $course_id})
                MERGE (u)-[:PARTICIPANT_OF]->(c)
                """,
                user_id=user_id,
                course_id=course_id,
            )
