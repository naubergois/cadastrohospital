"""Risk analysis utilities for hospital patients."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .models import Patient


@dataclass
class RiskAssessment:
    """Resultado de uma análise de risco."""

    score: int
    level: str
    recommendations: list[str]

    def as_dict(self) -> dict[str, object]:
        """Representação serializável da avaliação."""

        return {
            "score": self.score,
            "level": self.level,
            "recommendations": list(self.recommendations),
        }


class RiskAnalyzer:
    """Calcula o risco clínico de um paciente com base em sinais vitais e sintomas."""

    HIGH_RISK_SYMPTOMS = {"dor no peito", "falta de ar", "confusao", "desmaio"}

    def __init__(self) -> None:
        self.recommendations_map = {
            "Alto": [
                "Encaminhar imediatamente para emergência",
                "Monitorar sinais vitais continuamente",
            ],
            "Moderado": [
                "Encaminhar para avaliação médica prioritária",
                "Reavaliar sinais vitais a cada 30 minutos",
            ],
            "Baixo": [
                "Aguardar na triagem com monitoramento periódico",
                "Fornecer orientações básicas de cuidados",
            ],
        }

    def evaluate_patient(self, patient: Patient) -> RiskAssessment:
        """Calcula a pontuação e o nível de risco de um paciente."""

        score = 0
        score += self._score_age(patient.age)
        score += self._score_temperature(patient.vital_signs.temperature_c)
        score += self._score_blood_pressure(patient.vital_signs.systolic_bp)
        score += self._score_heart_rate(patient.vital_signs.heart_rate)
        score += self._score_symptoms(patient.symptoms)

        if score >= 6:
            level = "Alto"
        elif score >= 3:
            level = "Moderado"
        else:
            level = "Baixo"

        return RiskAssessment(
            score=score,
            level=level,
            recommendations=self.recommendations_map[level],
        )

    @staticmethod
    def _score_age(age: int) -> int:
        if age >= 75:
            return 3
        if age >= 65:
            return 2
        if age >= 45:
            return 1
        return 0

    @staticmethod
    def _score_temperature(temperature: float) -> int:
        if temperature >= 39:
            return 2
        if temperature >= 37.5:
            return 1
        if temperature < 35:
            return 2
        return 0

    @staticmethod
    def _score_blood_pressure(systolic_bp: int) -> int:
        if systolic_bp < 90:
            return 3
        if systolic_bp < 100:
            return 2
        if systolic_bp < 110:
            return 1
        return 0

    @staticmethod
    def _score_heart_rate(heart_rate: int) -> int:
        if heart_rate >= 130:
            return 3
        if heart_rate >= 120:
            return 2
        if heart_rate >= 100:
            return 1
        if heart_rate < 50:
            return 2
        return 0

    def _score_symptoms(self, symptoms: Iterable[str]) -> int:
        score = 0
        for symptom in symptoms:
            normalized = symptom.strip().lower()
            if normalized in self.HIGH_RISK_SYMPTOMS:
                score += 2
            elif normalized in {"febre", "vomito", "intensa dor"}:
                score += 1
        return score
