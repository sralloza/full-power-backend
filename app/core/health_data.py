from app.schemas.health_data import HealthDataCreate
from typing import Dict, Union
from app.models.health_data import HealthData

problem_names = ["vitamines", "sleep", "diet", "stress"]
problem_text = {
    "es": "Tu principal problema es %s",
    "en": "Your main problem is %s",
    "fr": "votre problème principal est %s",
}
problem_names_international = {
    "vitamines": {
        "es": "vitaminas",
        "en": "vitamines",
        "fr": "vitamines",
    },
    "sleep": {
        "es": "dormir",
        "en": "sleep",
        "fr": "sommeil",
    },
    "diet": {"es": "alimentación", "en": "diet", "fr": "alimentation"},
    "stress": {"es": "estrés", "en": "stress", "fr": "stress"},
}

coefficients = {
    "energy": (1, 0, 0, 0),
    "restful_sleep": (1, 2, 0, 0),
    "fall_asleep_easily": (1, 1, 0, 0),
    "deep_sleep": (1, 1, 0, 0),
    "enough_sleep": (0, 1, 0, 0),
    "energy_morning": (1, 1, 0, 0),
    "uniform_mood": (1, 0, 0, 1),
    "memory": (1, 0, 0, 0),
    "concentration": (1, 0, 0, 1),
    "creativity": (1, 0, 0, 1),
    "stress": (1, 0, 0, 2),
    "cramps": (1, 0, 0, 0),
    "dagger": (1, 0, 0, 1),
    "pump_strokes": (0, 0, 1, 0),
    "uplifts": (0, 0, 1, 0),
    "swollen_belly": (0, 0, 1, 0),
    "gases": (0, 0, 1, 0),
    "bowel_movement": (0, 0, 1, 0),
    "sheet_wipe": (0, 0, 1, 0),
}


sums = {x: 0 for x in problem_names}
for coeffs in coefficients.values():
    for i, problem_name in enumerate(problem_names):
        sums[problem_name] += coeffs[i] * 4


def process_health_data(data: Union[HealthData, HealthDataCreate]):
    problems = {k: 0 for k in problem_names}

    for question_id, coeffs in coefficients.items():
        try:
            value = 5 - getattr(data, question_id)
            for coef_idx, coef in enumerate(coeffs):
                problem_name = problem_names[coef_idx]
                problems[problem_name] += value * coef
        except:
            print(repr(data))
            raise

    problems = {k: v / sums[k] for k, v in problems.items()}
    return problems


def detect_main_problem(health_data_result: Dict[str, float], lang:str):
    max_ratio = max(health_data_result.values())
    for key, value in health_data_result.items():
        if value == max_ratio:
            template = problem_text[lang]
            return template % problem_names_international[key][lang]
    return None
