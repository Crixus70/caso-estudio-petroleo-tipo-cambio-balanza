# Precio del petróleo, tipo de cambio y balanza comercial: impacto económico, comercial y social en Ciudad del Carmen

Caso de estudio didáctico de análisis de datos aplicado a una pregunta económica real: ¿cómo se relacionan el precio del petróleo, el tipo de cambio y el comercio exterior con la actividad económica de una región petrolera?

> **Estado:** en desarrollo. El tipo de cambio USD/MXN está planeado como variable principal, pero la serie aún no está integrada al análisis. Las secciones de hallazgos se completarán cuando el análisis esté validado.

## Pregunta de negocio

Para una región con actividad petrolera, como Ciudad del Carmen, un cambio en el precio del crudo o en el tipo de cambio puede afectar:

- **Económico:** ingresos, costos en pesos de bienes importados y capacidad de inversión.
- **Comercial:** exportaciones, importaciones, contratos con proveedores y márgenes.
- **Social:** empleo, ingresos de hogares y servicios locales.

Este caso busca responder primero la parte económica y comercial, con datos públicos. Los efectos sociales se presentan como hipótesis que requieren datos adicionales.

## Fuentes públicas

| Fuente | Qué aporta | Condiciones de uso |
|---|---|---|
| U.S. Energy Information Administration (EIA) | Precios de referencia Brent y WTI | Dominio público; citar la fuente con fecha |
| PEMEX, Base de Datos Institucional (BDI) | Mezcla mexicana y comercio de crudo | Revisar condiciones de uso y fechas de validación |
| INEGI | Comercio exterior | Uso libre citando la fuente |
| Banco de México (SIE) | Tipo de cambio USD/MXN (pendiente) | Reproducción permitida citando la fuente y el sitio |

Cada fuente se documenta con unidad, periodicidad, cobertura geográfica, fecha de actualización y limitaciones.

## Enfoque metodológico

1. **Integración:** alinear series diarias de precios con series mensuales de comercio.
2. **Limpieza:** verificar unidades, fechas faltantes y cambios de base.
3. **Agregación:** convertir precios diarios a promedio mensual para compararlos con el comercio.
4. **Exploración:** revisar tendencias y asociaciones temporales.
5. **Comunicación:** resumir hallazgos con sus límites.

## Cifras verificadas (julio 2026)

Consultadas el 2026-11-08. Solo se incluyen cifras contrastadas con la fuente indicada.

| Variable | Valor | Fuente | Nota |
|---|---|---|---|
| Brent, promedio mensual (USD/barril) | 83.76 | FRED, serie MCOILBRENTEU (EIA) | Coincide con la cifra previa |
| WTI, promedio mensual (USD/barril) | 80.46 | FRED, serie DCOILWTICO (EIA) | Promedio de 22 días hábiles |
| USD/MXN, promedio mensual | 17.46 | FRED, serie DEXMXUS (Reserva Federal) | Promedio de 22 días hábiles |
| Exportaciones de hidrocarburos (MMUS$) | 1,547.174 | PEMEX BDI, Valor del comercio exterior | Cifra previa: 1,531.3 |
| Importaciones de hidrocarburos (MMUS$) | 2,391.693 | PEMEX BDI, Valor del comercio exterior | Cifra previa: 2,211.8 |
| Exportaciones netas (MMUS$) | −844.518 | PEMEX BDI, Valor del comercio exterior | Cifra previa: −680.5 |
| Mezcla mexicana (USD/barril) | Pendiente | PEMEX BDI | Se retira la cifra previa (74.66) hasta verificarla |

**Discrepancia:** las cifras de PEMEX del análisis previo no coinciden con el BDI. La causa (versión de datos, categoría o error) no está confirmada. Se usan las cifras del BDI.

Las series del BDI cubren 2026 de enero a septiembre. El análisis previo afirmaba que la serie terminaba en julio; eso no aplica a esta variable.

## Limitaciones

- Una asociación temporal **no demuestra causalidad**.
- Los precios de Brent y WTI son referencias; no representan el precio realizado por PEMEX.
- Las cifras nacionales no deben atribuirse a Ciudad del Carmen sin verificar su cobertura.
- Este repositorio usa **datos sintéticos** para probar el flujo. No representan precios ni operaciones reales.

## Código ilustrativo

La carpeta [`fragmentos/`](fragmentos/) contiene ejemplos cortos del enfoque, con datos sintéticos. No es el pipeline completo del análisis.

## Autor del análisis

Cristóbal Antonio Hernández Juárez · [Perfil de GitHub](https://github.com/Crixus70)
