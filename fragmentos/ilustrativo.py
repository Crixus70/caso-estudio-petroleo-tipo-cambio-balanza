"""Ejemplo didáctico: relacionar un precio mensual con un saldo comercial.

Usa datos sintéticos generados para este ejemplo; no contiene cifras reales.
El flujo es el que se aplicaría a series públicas: periodo explícito,
validación de cobertura, agregación mensual y correlación con rezago.
"""

import numpy as np
import pandas as pd


def precio_mensual(inicio: str, fin: str, semilla: int = 42) -> pd.Series:
    fechas = pd.bdate_range(inicio, fin)
    rng = np.random.default_rng(semilla)
    precio_diario = 75 + rng.normal(0, 0.8, len(fechas)).cumsum()
    serie = pd.Series(precio_diario, index=fechas)
    return serie.resample("MS").mean().rename("precio_usd_bbl")


def saldo_sintetico(precio: pd.Series, semilla: int = 7) -> pd.Series:
    # Relación construida a propósito: el saldo responde al precio del mes anterior
    rng = np.random.default_rng(semilla)
    precio_previo = precio.shift(1).bfill()
    saldo = 25 * (precio_previo - 75) + rng.normal(0, 40, len(precio))
    return pd.Series(saldo.values, index=precio.index, name="saldo_mdd")


def analizar(inicio: str, fin: str, rezago: int = 1) -> dict:
    precio = precio_mensual(inicio, fin)
    if len(precio) < 12:
        raise ValueError("Se requieren al menos 12 meses para el análisis.")
    saldo = saldo_sintetico(precio)
    alineado = pd.concat([precio.shift(rezago), saldo], axis=1).dropna()
    return {
        "periodo": f"{precio.index[0]:%Y-%m} a {precio.index[-1]:%Y-%m}",
        "meses": len(precio),
        "rezago_meses": rezago,
        "correlacion": round(float(alineado.iloc[:, 0].corr(alineado.iloc[:, 1])), 3),
        "precio_promedio": round(float(precio.mean()), 2),
    }


if __name__ == "__main__":
    for inicio, fin in [("2025-01-01", "2025-12-31"), ("2025-07-01", "2026-06-30")]:
        print(analizar(inicio, fin))
