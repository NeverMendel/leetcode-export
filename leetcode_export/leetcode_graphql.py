from dataclasses import dataclass

from dataclasses_json import dataclass_json

GRAPHQL_URL = "https://leetcode.com/graphql"


@dataclass_json
@dataclass
class Problem:
    question_id: int
    difficulty: str
    stats: str
    title: str
    title_slug: str
    content: str


def question_detail_json(slug):
    return {
        "operationName": "getQuestionDetail",
        "variables": {"titleSlug": slug},
        "query": """query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                difficulty
                stats
                title
                titleSlug
                content
            }
        }""",
    }
