"""Data models used by the hospital registration application."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class VitalSigns:
    """Representa os sinais vitais principais medidos na triagem."""

    temperature_c: float
    systolic_bp: int
    heart_rate: int

    def as_dict(self) -> dict[str, float | int]:
        """Retorna os sinais vitais em um formato serializável."""

        return {
            "temperature_c": self.temperature_c,
            "systolic_bp": self.systolic_bp,
            "heart_rate": self.heart_rate,
        }


@dataclass
class Patient:
    """Dados cadastrados do paciente que chega ao hospital."""

    name: str
    age: int
    symptoms: List[str] = field(default_factory=list)
    vital_signs: VitalSigns = field(default_factory=lambda: VitalSigns(36.5, 120, 80))
    arrival_time: datetime = field(default_factory=datetime.now)

    def add_symptom(self, symptom: str) -> None:
        """Adiciona um sintoma à lista do paciente."""

        sanitized = symptom.strip()
        if sanitized and sanitized.lower() not in (s.lower() for s in self.symptoms):
            self.symptoms.append(sanitized)

    def as_dict(self) -> dict[str, object]:
        """Converte o paciente em um dicionário serializável."""

        return {
            "name": self.name,
            "age": self.age,
            "symptoms": list(self.symptoms),
            "vital_signs": self.vital_signs.as_dict(),
            "arrival_time": self.arrival_time.isoformat(),
        }
