"""Fragmento ilustrativo con datos sintéticos. No es el pipeline completo."""

import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

# Precios diarios sintéticos de referencia (USD por barril)
fechas = pd.bdate_range("2025-01-01", "2026-11-08")
precio = 75 + rng.normal(0, 0.8, len(fechas)).cumsum()
precios = pd.DataFrame({"fecha": fechas, "precio_usd_bbl": precio})

# Agregación mensual para alinear con series de comercio
mensual = (
    precios.set_index("fecha")
    .resample("MS")["precio_usd_bbl"]
    .mean()
    .rename("precio_promedio_mensual")
)
print(mensual.round(2))
