"""Aplicação CLI para cadastro de pacientes e análise de risco."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from hospital import Patient, PatientRegistry, RiskAnalyzer, VitalSigns

DATA_FILE = Path("dados_pacientes.json")


def prompt_float(message: str, default: float) -> float:
    while True:
        raw = input(f"{message} [{default}]: ").strip()
        if not raw:
            return default
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            print("Valor inválido. Tente novamente.")


def prompt_int(message: str, default: int) -> int:
    while True:
        raw = input(f"{message} [{default}]: ").strip()
        if not raw:
            return default
        if raw.isdigit():
            return int(raw)
        print("Digite um número inteiro válido.")


def carregar_dados(registry: PatientRegistry) -> None:
    if not DATA_FILE.exists():
        return
    with DATA_FILE.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    for entry in data:
        vitals = entry.get("vital_signs", {})
        patient = Patient(
            name=entry["name"],
            age=entry["age"],
            symptoms=list(entry.get("symptoms", [])),
            vital_signs=VitalSigns(
                temperature_c=vitals.get("temperature_c", 36.5),
                systolic_bp=vitals.get("systolic_bp", 120),
                heart_rate=vitals.get("heart_rate", 80),
            ),
        )
        registry.add_patient(patient)


def salvar_dados(registry: PatientRegistry) -> None:
    data: list[Dict[str, Any]] = [patient.as_dict() for patient in registry.list_patients()]
    with DATA_FILE.open("w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)


def cadastrar_paciente(registry: PatientRegistry) -> None:
    print("\n=== Cadastro de Paciente ===")
    nome = input("Nome completo: ").strip()
    idade = prompt_int("Idade", 30)

    temperatura = prompt_float("Temperatura (°C)", 36.8)
    sistolica = prompt_int("Pressão sistólica (mmHg)", 120)
    frequencia = prompt_int("Frequência cardíaca (bpm)", 80)

    sintomas: list[str] = []
    print("Informe os sintomas (vazio para finalizar):")
    while True:
        sintoma = input("- ").strip()
        if not sintoma:
            break
        sintomas.append(sintoma)

    patient = Patient(
        name=nome,
        age=idade,
        symptoms=sintomas,
        vital_signs=VitalSigns(
            temperature_c=temperatura,
            systolic_bp=sistolica,
            heart_rate=frequencia,
        ),
    )

    assessment = registry.add_patient(patient)
    print("\nPaciente cadastrado com sucesso!")
    print(f"Risco: {assessment.level} (pontuação {assessment.score})")
    print("Recomendações:")
    for item in assessment.recommendations:
        print(f" - {item}")


def listar_pacientes(registry: PatientRegistry) -> None:
    print("\n=== Pacientes cadastrados ===")
    for idx, patient in enumerate(registry.list_patients(), start=1):
        print(f"{idx}. {patient.name} - {patient.age} anos")
        analyzer = RiskAnalyzer()
        assessment = analyzer.evaluate_patient(patient)
        print(f"   Risco: {assessment.level} (pontuação {assessment.score})")
        if patient.symptoms:
            print("   Sintomas: " + ", ".join(patient.symptoms))
        print(
            "   Sinais Vitais: T={:.1f}°C, PAS={}mmHg, FC={}bpm".format(
                patient.vital_signs.temperature_c,
                patient.vital_signs.systolic_bp,
                patient.vital_signs.heart_rate,
            )
        )


def buscar_paciente(registry: PatientRegistry) -> None:
    nome = input("Nome do paciente para buscar: ").strip()
    patient = registry.find_by_name(nome)
    if not patient:
        print("Paciente não encontrado.")
        return
    analyzer = RiskAnalyzer()
    assessment = analyzer.evaluate_patient(patient)
    print(f"\nPaciente: {patient.name}")
    print(f"Idade: {patient.age}")
    print(f"Sintomas: {', '.join(patient.symptoms) if patient.symptoms else 'Nenhum informado'}")
    print(
        "Sinais vitais: T={:.1f}°C, PAS={}mmHg, FC={}bpm".format(
            patient.vital_signs.temperature_c,
            patient.vital_signs.systolic_bp,
            patient.vital_signs.heart_rate,
        )
    )
    print(f"Risco: {assessment.level} (pontuação {assessment.score})")
    print("Recomendações:")
    for item in assessment.recommendations:
        print(f" - {item}")


def main() -> None:
    registry = PatientRegistry()
    carregar_dados(registry)

    menu = {
        "1": ("Cadastrar novo paciente", cadastrar_paciente),
        "2": ("Listar pacientes", listar_pacientes),
        "3": ("Buscar paciente por nome", buscar_paciente),
        "4": ("Salvar e sair", None),
    }

    while True:
        print("\n=== Sistema de Triagem Hospitalar ===")
        for option, (label, _) in menu.items():
            print(f"{option}. {label}")
        choice = input("Selecione uma opção: ").strip()

        if choice == "4":
            salvar_dados(registry)
            print("Dados salvos. Até logo!")
            break

        action = menu.get(choice)
        if not action:
            print("Opção inválida. Tente novamente.")
            continue

        _, handler = action
        if handler:
            handler(registry)


if __name__ == "__main__":
    main()
