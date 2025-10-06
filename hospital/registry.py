"""Gerenciamento de pacientes cadastrados."""

from __future__ import annotations

from typing import Iterable, List, Optional

from .models import Patient
from .risk_analyzer import RiskAnalyzer, RiskAssessment


class PatientRegistry:
    """Mantém uma lista de pacientes cadastrados com avaliação de risco."""

    def __init__(self, analyzer: RiskAnalyzer | None = None) -> None:
        self._patients: List[Patient] = []
        self._analyzer = analyzer or RiskAnalyzer()

    def add_patient(self, patient: Patient) -> RiskAssessment:
        """Adiciona um paciente e retorna sua avaliação de risco."""

        assessment = self._analyzer.evaluate_patient(patient)
        self._patients.append(patient)
        return assessment

    def list_patients(self) -> Iterable[Patient]:
        """Retorna um iterador de pacientes na ordem de chegada."""

        return tuple(self._patients)

    def find_by_name(self, name: str) -> Optional[Patient]:
        """Pesquisa um paciente pelo nome (case insensitive)."""

        name_lower = name.lower()
        for patient in self._patients:
            if patient.name.lower() == name_lower:
                return patient
        return None
