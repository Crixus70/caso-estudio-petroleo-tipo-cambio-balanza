import csv
from collections import defaultdict
from datetime import date
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

DIR = Path(__file__).resolve().parent
SALIDA = DIR / "PRECIO DE PETROLEO Y BALANZA - verificado ene-sep 2026.pdf"
CONSULTA = "2026-11-08"
MESES = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep"]

# PEMEX BDI, consultado el 2026-11-08. INDI09 (USD/b) e INDI10 (MMUS$), ene-sep 2026.
PRECIO_TOTAL = [56.004, 67.625, 89.031, 87.598, 88.634, 81.831, 81.465, 84.025, 91.035]
PRECIO_ISTMO = [57.829, 77.741, 88.739, 92.128, 94.168, 84.576, 82.930, 81.456, 92.938]
PRECIO_MAYA = [55.695, 62.151, 88.770, 84.505, 86.979, 78.390, 80.122, 80.002, 85.957]
EXPORTACIONES = [799.734, 1377.447, 1620.106, 1636.064, 1808.809, 1713.922,
                 1547.174, 1313.027, 1411.850]
IMPORTACIONES = [1213.762, 1178.216, 1400.823, 2021.582, 2997.147, 2676.614,
                 2391.693, 2013.310, 2170.173]
SALDO = [round(x - m, 3) for x, m in zip(EXPORTACIONES, IMPORTACIONES)]


def leer_mensual(nombre):
    with open(DIR / f"{nombre}.csv", encoding="utf-8") as f:
        filas = list(csv.reader(f))[1:]
    return [float(v) for _, v in filas if v]


def promedio_mensual_diario(nombre):
    grupos = defaultdict(list)
    with open(DIR / f"{nombre}.csv", encoding="utf-8") as f:
        for fecha, valor in list(csv.reader(f))[1:]:
            if valor:
                grupos[date.fromisoformat(fecha).month].append(float(valor))
    return [sum(grupos[m]) / len(grupos[m]) for m in range(1, 10)]


BRENT = leer_mensual("MCOILBRENTEU")
WTI = leer_mensual("MCOILWTICO")
MXN = promedio_mensual_diario("DEXMXUS")


def grafica_precios():
    fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=150)
    ax.plot(MESES, BRENT, marker="o", label="Brent (EIA/FRED)")
    ax.plot(MESES, WTI, marker="o", label="WTI (EIA/FRED)")
    ax.plot(MESES, PRECIO_TOTAL, marker="s", label="PEMEX, promedio de exportación")
    ax.set_ylabel("USD por barril")
    ax.grid(alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    return fig


def grafica_comercio():
    fig, ax = plt.subplots(figsize=(7.5, 3.6), dpi=150)
    x = range(len(MESES))
    ancho = 0.4
    ax.bar([i - ancho / 2 for i in x], EXPORTACIONES, ancho, label="Exportaciones")
    ax.bar([i + ancho / 2 for i in x], IMPORTACIONES, ancho, label="Importaciones")
    ax.plot(list(x), SALDO, color="black", marker="d", label="Saldo")
    ax.axhline(0, color="gray", linewidth=0.8)
    ax.set_xticks(list(x), MESES)
    ax.set_ylabel("Millones de USD")
    ax.grid(alpha=0.3, axis="y")
    ax.legend(fontsize=8)
    fig.tight_layout()
    return fig


def imagen(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    buf.seek(0)
    return buf


def f1(x):
    return f"{x:,.1f}"


def f2(x):
    return f"{x:,.2f}"


def f3(x):
    return f"{x:,.3f}"


estilos = getSampleStyleSheet()
normal = ParagraphStyle("n", parent=estilos["Normal"], fontSize=9.5, leading=13)
titulo = ParagraphStyle("t", parent=estilos["Title"], fontSize=17, leading=21)
h2 = ParagraphStyle("h2", parent=estilos["Heading2"], fontSize=12.5, spaceBefore=8)
chica = ParagraphStyle("c", parent=normal, fontSize=8, leading=10.5, textColor=colors.HexColor("#444444"))


def tabla(filas, anchos):
    t = Table(filas, colWidths=anchos, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDE5EE")),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def construir():
    spread_brent = BRENT[6] - PRECIO_TOTAL[6]
    spread_wti = WTI[6] - PRECIO_TOTAL[6]
    meses_negativos = [MESES[i] for i, s in enumerate(SALDO) if s < 0]
    pico_imp = max(range(9), key=lambda i: IMPORTACIONES[i])
    pico_brent = max(range(9), key=lambda i: BRENT[i])
    brecha = [b - p for b, p in zip(BRENT, PRECIO_TOTAL)]
    pico_brecha = max(range(9), key=lambda i: brecha[i])

    historia = []
    historia.append(Paragraph("Escenario petrolero: precios, tipo de cambio y comercio exterior de PEMEX", titulo))
    historia.append(Paragraph(
        f"Enero a septiembre de 2026. Cifras consultadas el {CONSULTA}. Analista: Mtro. Cristóbal Hernández.",
        chica))
    historia.append(Spacer(1, 8))

    historia.append(Paragraph("Resumen", h2))
    historia.append(Paragraph(
        f"Este informe reemplaza las cifras del reporte anterior por valores verificados en el BDI de PEMEX "
        f"y en FRED (series de EIA y de la Reserva Federal). El periodo cubierto es de enero a septiembre de 2026, "
        f"porque los años 2022 a 2025 no pudieron consultarse en el BDI en esta versión.", normal))
    historia.append(Spacer(1, 6))
    historia.append(Paragraph(
        f"En julio de 2026, el promedio de exportación de PEMEX fue de USD {f2(PRECIO_TOTAL[6])} por barril, "
        f"Brent promedió USD {f2(BRENT[6])} y WTI USD {f2(WTI[6])}. El tipo de cambio promedió "
        f"{f2(MXN[6])} pesos por dólar. El saldo de hidrocarburos de PEMEX fue de "
        f"{f1(SALDO[6])} millones de USD.", normal))

    historia.append(Paragraph("Cifras de julio de 2026: nuevo contra reporte anterior", h2))
    filas = [
        ["Concepto", "Nuevo (verificado)", "Reporte anterior", "Fuente"],
        ["Precio promedio de exportación PEMEX, USD/b", f2(PRECIO_TOTAL[6]), "74.66 (Mezcla Mexicana)", "BDI, INDI09 (Total)"],
        ["Brent, USD/b", f2(BRENT[6]), "83.76", "FRED, MCOILBRENTEU"],
        ["WTI, USD/b", f2(WTI[6]), "80.46", "FRED, MCOILWTICO"],
        ["Tipo de cambio USD/MXN (promedio)", f2(MXN[6]), "No incluido", "FRED, DEXMXUS"],
        ["Exportaciones de hidrocarburos, MMUS$", f1(EXPORTACIONES[6]), "1,531.3", "BDI, INDI10"],
        ["Importaciones de hidrocarburos, MMUS$", f1(IMPORTACIONES[6]), "2,211.8", "BDI, INDI10"],
        ["Saldo, MMUS$", f1(SALDO[6]), "-680.5", "BDI, INDI10"],
    ]
    historia.append(tabla(filas, [6.6 * cm, 3.2 * cm, 3.9 * cm, 4.2 * cm]))
    historia.append(Spacer(1, 4))
    historia.append(Paragraph(
        "La Mezcla Mexicana no aparece como fila en el BDI (INDI09). Se usa el total de exportación, que "
        "promedia todos los crudos. La cifra previa de 74.66 no coincide con ninguna fila del BDI para julio de 2026. "
        "Las cifras previas de PEMEX para exportaciones, importaciones y saldo tampoco coinciden con el BDI. "
        "La causa (versión de datos, categoría o error) no está confirmada.", chica))

    historia.append(Paragraph("Precios: referencias internacionales y precio de exportación de PEMEX", h2))
    historia.append(Image(imagen(grafica_precios()), width=16 * cm, height=7.7 * cm))
    historia.append(Paragraph(
        f"Figura 1. Precios mensuales, enero a septiembre de 2026. USD por barril.", chica))
    historia.append(Spacer(1, 4))
    historia.append(Paragraph(
        f"En julio, el precio de exportación de PEMEX quedó {f2(abs(spread_brent))} USD "
        f"{'por debajo' if spread_brent > 0 else 'por encima'} de Brent y {f2(abs(spread_wti))} USD "
        f"{'por debajo' if spread_wti > 0 else 'por encima'} de WTI. Brent alcanzó su máximo mensual en "
        f"{MESES[pico_brent]} ({f2(BRENT[pico_brent])}). Brent superó el precio de exportación de PEMEX en todos "
        f"los meses; la diferencia fue mínima en {MESES[min(range(9), key=lambda i: brecha[i])]} "
        f"({f2(min(brecha))}) y máxima en {MESES[pico_brecha]} ({f2(brecha[pico_brecha])}). Esto refleja que el "
        f"precio de PEMEX depende de la mezcla exportada, el destino y el calendario de venta.", normal))

    filas_p = [["Mes", "Brent", "WTI", "PEMEX total", "Istmo", "Maya", "USD/MXN"]]
    for i, m in enumerate(MESES):
        filas_p.append([m, f2(BRENT[i]), f2(WTI[i]), f2(PRECIO_TOTAL[i]), f2(PRECIO_ISTMO[i]),
                        f2(PRECIO_MAYA[i]), f2(MXN[i])])
    historia.append(tabla(filas_p, [2.2 * cm] + [2.5 * cm] * 6))
    historia.append(Paragraph("Tabla 1. Precios mensuales y tipo de cambio promedio. Istmo y Maya son crudos de PEMEX; "
                              "USD/MXN es el promedio diario del mes.", chica))

    historia.append(Paragraph("Comercio exterior de hidrocarburos de PEMEX", h2))
    historia.append(Image(imagen(grafica_comercio()), width=16 * cm, height=7.7 * cm))
    historia.append(Paragraph("Figura 2. Exportaciones, importaciones y saldo mensual de PEMEX, MMUS$.", chica))
    historia.append(Spacer(1, 4))
    historia.append(Paragraph(
        f"El saldo fue negativo en {len(meses_negativos)} de 9 meses ({', '.join(meses_negativos)}). "
        f"Las importaciones alcanzaron su máximo en {MESES[pico_imp]} ({f1(IMPORTACIONES[pico_imp])} MMUS$), "
        f"mientras las exportaciones fueron de {f1(EXPORTACIONES[pico_imp])}. El saldo de julio es "
        f"{f1(SALDO[6])} MMUS$. El saldo es una resta descriptiva de valores comerciales; no es utilidad, flujo "
        f"de efectivo ni la balanza comercial del país.", normal))

    filas_c = [["Mes", "Exportaciones", "Importaciones", "Saldo"]]
    for i, m in enumerate(MESES):
        filas_c.append([m, f1(EXPORTACIONES[i]), f1(IMPORTACIONES[i]), f1(SALDO[i])])
    historia.append(tabla(filas_c, [2.6 * cm, 3.6 * cm, 3.6 * cm, 3.6 * cm]))
    historia.append(Paragraph("Tabla 2. Comercio de hidrocarburos de PEMEX, MMUS$. Saldo calculado como exportaciones "
                              "menos importaciones.", chica))

    historia.append(Paragraph("Límites del análisis", h2))
    for texto in [
        "Solo cubre enero a septiembre de 2026 (9 meses). No hay años completos para comparar estacionalidad "
        "ni variación interanual; el reporte anterior incluía un perfil estacional que no se incluye aquí.",
        "Una asociación entre precios y comercio no demuestra causalidad. Volumen, producto y condiciones de "
        "compra o venta también influyen en el saldo.",
        "Brent y WTI son referencias internacionales. El precio de exportación de PEMEX es un promedio de crudos "
        "y no es un precio realizado por una instalación específica.",
        "Las cifras son nacionales de PEMEX. No deben atribuirse a Ciudad del Carmen sin verificar su cobertura.",
    ]:
        historia.append(Paragraph(f"• {texto}", normal))

    historia.append(Paragraph("Fuentes y método", h2))
    for texto in [
        f"PEMEX, Base de Datos Institucional (BDI). INDI09, precio promedio de exportación de petróleo crudo "
        f"(USD/b), e INDI10, valor del comercio exterior de hidrocarburos y derivados (MMUS$). Mensual. "
        f"Consulta: {CONSULTA}.",
        "FRED, Federal Reserve Bank of St. Louis. MCOILBRENTEU y MCOILWTICO (EIA, precios spot mensuales en USD/b). "
        "DEXMXUS (tipo de cambio diario, promedio mensual calculado ignorando días sin dato). Consulta: "
        f"{CONSULTA}.",
        "Los CSV de FRED y el script que genera este documento están en la carpeta reporte_2026_datos.",
    ]:
        historia.append(Paragraph(f"• {texto}", normal))

    doc = SimpleDocTemplate(str(SALIDA), pagesize=letter,
                            leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                            title="Escenario petrolero enero-septiembre 2026", author="Mtro. Cristóbal Hernández")
    doc.build(historia)
    print(f"PDF generado: {SALIDA}")


if __name__ == "__main__":
    construir()
