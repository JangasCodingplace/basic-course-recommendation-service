from neo4j import GraphDatabase
from .configs import NEO4J
from .models import CourseEssential


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

    @staticmethod
    def add_relationship_to_course(source_id: int, target_id: int, rel_type: str = "REQUIRES"):
        # RM This Repository
        with neo4j.driver.session() as session:
            session.run(
                """
                MATCH (c1:Course {id: $source_id}), (c2:Course {id: $target_id})
                MERGE (c1)-[:"""
                + rel_type
                + """]->(c2)
                """,
                source_id=source_id,
                target_id=target_id,
                rel_type=rel_type,
            )


class UserRepository:
    @staticmethod
    def create_node(id_: int):
        with neo4j.driver.session() as session:
            session.run("MERGE (u:User {id: $id})", id=id_)

    @staticmethod
    def get_courses(id_: int) -> list[CourseEssential]:
        with neo4j.driver.session() as session:
            result = session.run(
                "MATCH (u: User {id: $user_id})-[p:PARTICIPANT_OF]->(c: Course)-[b:BELONGS_TO]->(t: Topic) RETURN c, b, t",  # noqa
                user_id=str(id_),
            )
            data = result.data()
        return [
            CourseEssential(id=row["c"]["id"], title=row["c"]["name"], topic=row["t"]["name"])
            for row in data
        ]


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


class RecommendationRepository:
    @staticmethod
    def get_course_recommendation_by_use_case(user_id: int) -> list[CourseEssential]:
        query = """
            MATCH (u:User {id: $user_id})-[:PARTICIPANT_OF]->(c:Course)-[:SUITABLE_FOR]->(uc:UseCase)<-[:SUITABLE_FOR]-(c2:Course)-[b:BELONGS_TO]->(t: Topic)
            WHERE NOT (u)-[:PARTICIPANT_OF]->(c2)
            RETURN DISTINCT c2, b, t, COUNT(DISTINCT uc) AS num_use_cases_in_common
            ORDER BY num_use_cases_in_common DESC
            LIMIT 10
        """  # noqa
        with neo4j.driver.session() as session:
            result = session.run(query, user_id=str(user_id))
            data = result.data()
        return [
            CourseEssential(
                id=row["c2"]["id"],
                title=row["c2"]["name"],
                topic=row["t"]["name"],
            )
            for row in data
        ]
