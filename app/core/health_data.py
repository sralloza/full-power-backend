import logging
from collections import namedtuple
from pathlib import Path
from typing import Dict, List, Union

from fastapi import HTTPException
from pydantic import parse_file_as

from app.models.health_data import HealthData
from app.schemas.health_data import (
    HealthDataCreate,
    HealthDataProccessResult,
    ProblemResultI18n,
    ProblemsI18n,
    QuestionCoefficients,
)
from app.utils.translate import i18n

HealthDataLike = Union[HealthData, HealthDataCreate]
logger = logging.getLogger(__name__)
Problem = namedtuple("Problem", "name severity")


class _HealthDataProcessor:
    problem_names = ("vitamines", "sleep", "diet", "stress")

    def __init__(self):
        self.problem_result_text = self._get_problem_result_text()
        self.question_coeffs = self._get_question_coeffs()
        self.problem_translation = self._get_problem_translation()
        self.sums = self._sum_coefficients()

    @staticmethod
    def _get_problem_result_text() -> ProblemResultI18n:
        return ProblemResultI18n.parse_file(
            Path(__file__).resolve().parent.parent / "db/files/problem_result_i18n.json"
        )

    @staticmethod
    def _get_question_coeffs() -> List[QuestionCoefficients]:
        return parse_file_as(
            List[QuestionCoefficients],
            Path(__file__).resolve().parent.parent / "db/files/coefficients.json",
        )

    @staticmethod
    def _get_problem_translation() -> ProblemsI18n:
        return ProblemsI18n.parse_file(
            Path(__file__).resolve().parent.parent / "db/files/problem_names_i18n.json"
        )

    def _sum_coefficients(self) -> Dict[str, int]:
        sums = {x: 0 for x in self.problem_names}
        for question_coeffs in self.question_coeffs:
            for problem_name in self.problem_names:
                sums[problem_name] += question_coeffs.dict()[problem_name] * 4
        return sums

    def process_health_data(self, data: HealthDataLike) -> HealthDataProccessResult:
        problems = {k: 0 for k in self.problem_names}

        for question_coeffs in self.question_coeffs:
            try:
                value = 5 - getattr(data, question_coeffs.question_id)
                for problem_name in self.problem_names:
                    problems[problem_name] += (
                        value * question_coeffs.dict()[problem_name]
                    )
            except Exception as exc:
                logger.exception("Found error processing health data (%r)", data)
                raise HTTPException(500, "Fatal error processing health data") from exc

        problems = {k: v / self.sums[k] for k, v in problems.items()}
        return HealthDataProccessResult.parse_obj(problems)

    def classify_problems(self, hd_result: HealthDataProccessResult) -> List[Problem]:
        problems = []
        for problem, severity in hd_result:  # noqa
            if 0.333333 <= severity < 0.666666:
                problems.append(Problem(problem, "light"))
            elif severity >= 0.666666:
                problems.append(Problem(problem, "serious"))

        return problems

    @classmethod
    def advanced_join(cls, iterable, join_str):
        if len(iterable) < 2:
            return f" {join_str} ".join(iterable)
        return ", ".join(iterable[:-1]) + f" {join_str} {iterable[-1]}"


hdprocessor = _HealthDataProcessor()
