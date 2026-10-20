"""Calibra el umbral de intención E5 sin modificar la aplicación."""
from ai_comparator import _best_intent


POSITIVAS = [
    ("qué cosas se me terminan", "reposicion"),
    ("qué me falta en la alacena", "reposicion"),
    ("tengo que reponer algo", "reposicion"),
    ("se me acabó algo", "reposicion"),
    ("hay promos de leche", "ofertas"),
    ("qué hay de barato", "ofertas"),
    ("mostrame las promociones", "ofertas"),
    ("cuánto llevo gastado", "presupuesto"),
    ("me alcanza la plata este mes", "presupuesto"),
    ("cómo estoy de gastos", "presupuesto"),
    ("cuánto me queda para gastar", "presupuesto"),
]

NEGATIVAS = [
    "contame un chiste",
    "qué hora es",
    "quién ganó el partido",
    "cómo está el clima hoy",
    "receta de milanesas",
    "cuál es la capital de Francia",
    "gracias",
    "quién sos",
]


def main() -> None:
    scores_positivos = []
    scores_negativos = []
    correctas = 0

    print(f"{'FRASE':35} {'ESPERADA':12} {'DETECTADA':12} SCORE")
    print("-" * 70)
    for phrase, expected in POSITIVAS:
        detected, score = _best_intent(phrase)
        correctas += detected == expected
        scores_positivos.append(score)
        print(f"{phrase:35} {expected:12} {detected or '-':12} {score:.3f}")

    print("-" * 70)
    for phrase in NEGATIVAS:
        detected, score = _best_intent(phrase)
        scores_negativos.append(score)
        print(f"{phrase:35} {'(ninguna)':12} {detected or '-':12} {score:.3f}")

    print(f"\nIntención correcta en positivas: {correctas}/{len(POSITIVAS)}")
    print(
        f"Scores positivas: mín {min(scores_positivos):.3f} / "
        f"máx {max(scores_positivos):.3f}"
    )
    print(
        f"Scores negativas: mín {min(scores_negativos):.3f} / "
        f"máx {max(scores_negativos):.3f}"
    )
    if min(scores_positivos) > max(scores_negativos):
        threshold = (min(scores_positivos) + max(scores_negativos)) / 2
        print(f"Hay separación en esta muestra. Umbral sugerido: {threshold:.2f}")
        return

    print("No hay separación limpia en esta muestra; revisar los falsos positivos:")
    for threshold in (0.80, 0.85, 0.88, 0.90, 0.92):
        false_positives = sum(score >= threshold for score in scores_negativos)
        false_negatives = sum(score < threshold for score in scores_positivos)
        print(
            f"  umbral {threshold:.2f}: falsos positivos "
            f"{false_positives}/{len(scores_negativos)}, falsos negativos "
            f"{false_negatives}/{len(scores_positivos)}"
        )


if __name__ == "__main__":
    main()
