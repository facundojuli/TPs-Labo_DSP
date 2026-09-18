# Diagnóstico de falla en rodamiento por análisis vibracional

**Trabajo Práctico de Cursada — Laboratorio de Procesamiento de Señales (ITBA)**
Louzao Gonzalo (63010) · Facundo Juli (63379)

Detección e identificación de una falla localizada en el rodamiento de un ventilador
industrial a partir de señales de vibración, con un flujo **empírico**: el elemento
fallado se determina desde la señal y no desde una fórmula con geometría supuesta.

## Resultado

Falla localizada en la **pista interna (BPFI)** del rodamiento del lado acople del
ventilador 2 (canal `M2-C1`).

| Evidencia | Valor |
|---|---|
| Pico dominante del espectro de envolvente | 173.22 Hz = **10.396 × f_r** |
| Armónicos detectados (>3 dB sobre el fondo local) | 4 de 4 |
| Bandas laterales a ±f_r (>3 dB) | 7 de 8 |
| BPFI teórico (reporte SKF) | 10.826 × f_r → error **−3.97 %** (deslizamiento) |
| Relación pico/fondo a 173 Hz | 20.6 dB, contra 1.3–1.4 dB en los canales sanos |

## Datos

Carpeta `datos/`. CSV exportados por el sistema de monitoreo de planta:
separador `;`, coma decimal, primera columna `Tiempo` en segundos, una columna por canal.

| Archivo | Contenido | f_s | Duración | Rol |
|---|---|---|---|---|
| `med2_acel_wf.csv` | aceleración, 2 canales | 24 kHz | 271 s | **caso de estudio**: C1 = lado acople (falla), C2 = lado libre del mismo ventilador |
| `med1_acel_wf.csv` | aceleración, 2 canales | 24 kHz | 364 s | otro ventilador, aparentemente sano: referencia externa |
| `ruido_sensor_acel.csv` | aceleración, 1 canal | 24 kHz | 122 s | sensor sin máquina: piso de ruido |
| `med*_vel_wf.csv` | velocidad [mm/s] | 3 kHz | — | estimación empírica de f_r (pico 1×) |
| `med*_env_wf.csv` | envolvente [gE] | 3 kHz | — | envolvente del software de mantenimiento: validación cruzada |

Las señales de velocidad y envolvente ya vienen procesadas por el software comercial.
**No** se usan como entrada del análisis: la velocidad sólo sirve para medir f_r, y la
envolvente del equipo se usa al final del paso 6 para verificar que nuestra cadena de
demodulación llega al mismo resultado (coinciden exactamente: 173.22 Hz).

Condiciones de operación: f_r medida = **16.663 Hz** (999.8 rpm), del pico 1× del espectro
de velocidad.

## Rodamiento

**SKF 22230 CCK/W33** — rodillos a rótula, doble hilera, d=150 mm, D=270 mm, B=73 mm.

El catálogo no publica la geometría interna. Del reporte `SKF_Bearing_calculation_report-1_260916_125317.pdf`
(a 995 rpm) se despejan los coeficientes adimensionales, y de las identidades de
consistencia `BPFO + BPFI = Z·f_r` y `BPFO = Z·FTF` se deduce **Z = 19** elementos
rodantes por hilera (ambas dan 19.00, discrepancia 1.2e-3).

| | × f_r | Hz @ 16.663 Hz |
|---|---|---|
| FTF | 0.4303 | 7.17 |
| BSF | 3.4629 | 57.70 |
| 2×BSF | 6.9258 | 115.40 |
| BPFO | 8.1746 | 136.21 |
| **BPFI** | **10.8258** | **180.39** |

> El rango publicado "BPFI ≈ 5–8 × f_r" corresponde a rodamientos de bolas con Z ≈ 8–12.
> Con Z = 19 el BPFI cae en 10.83 × f_r, fuera de ese rango. La ventana de búsqueda
> empírica del notebook llega hasta 15 × f_r por ese motivo.

## Contenido

```
TP Cursada/
├── TP_diagnostico_rodamiento.ipynb    # el análisis completo
├── datos/                             # CSV de las mediciones
├── SKF_Bearing_calculation_report-1_260916_125317.pdf
├── TP_LDSP_Propuestas.pdf             # propuesta inicial (Propuesta B)
└── Presentacion_TP_LDSP.pdf/.pptx
```

## Cómo correrlo

```bash
pip install numpy scipy matplotlib pandas PyWavelets
```

Abrir `TP_diagnostico_rodamiento.ipynb` y hacer **Restart & Run All**. Tarda ~45 s y
genera 22 figuras. El notebook se entrega sin salidas embebidas: hay que ejecutarlo
para ver los gráficos.

Todos los parámetros están en la primera celda de código. Los que conviene tocar:

| Parámetro | Default | Qué hace |
|---|---|---|
| `T_ANALISIS` | `60.0` | segundos de registro a procesar. Verificado a 20, 60 y 120 s: mismo veredicto, el pico se mueve como máximo un bin espectral |
| `NPERSEG_ENV` | `2**16` | ventana de Welch del espectro de envolvente (Δf = 0.366 Hz) |
| `T_VENTANA` | `1.0` | ventana para los indicadores por segmento |
| `K_SIGMA` | `3.0` | margen del umbral de alarma, en σ de la población de referencia |

## Estructura del análisis

| Paso | Contenido |
|---|---|
| 1 | Carga y control de calidad: f_s, saturación, offset, estacionariedad |
| 2 | Caracterización del piso de ruido: Welch con promedio robusto, autocorrelación |
| 3 | Indicadores temporales: RMS, factor de cresta, kurtosis, asimetría |
| 4 | Estimación espectral: periodograma vs. Welch, ventanas, modelo AR (Yule-Walker) |
| 5 | Selección automática de la banda de demodulación: kurtograma rápido (Antoni) |
| 6 | Análisis de envolvente: Hilbert, espectro, armónicos y bandas laterales |
| 7 | Identificación empírica de la falla y contraste con el reporte del fabricante |
| 8 | Tiempo-frecuencia: STFT y wavelet de Morlet |
| 9 | Vector de indicadores de salud y umbral de alarma |
| 10 | Tabla resumen y veredicto automático |

## Resumen de resultados

| Canal | RMS [g] | Kurtosis | Banda kurtograma | R_BPFI [dB] | Veredicto |
|---|---|---|---|---|---|
| M2-C1 | 1.684 | **+1.098** | 1500–3000 Hz | **+3.64** | **FALLA** |
| M2-C2 | 3.469 | −0.006 | 750–1125 Hz | +0.20 | OK |
| M1-C1 | 2.924 | −0.015 | 8250–9000 Hz | −0.10 | OK |
| M1-C2 | 1.375 | +0.577 | 8000–12000 Hz | +0.07 | OK |
| RUIDO | 0.0024 | +9.757 | — | +0.29 | MEDICIÓN NO VÁLIDA |

## Notas metodológicas

Cuatro cosas que los datos mostraron y que conviene tener presentes:

- **El nivel global de vibración señala el canal equivocado.** El canal sano M2-C2 tiene
  el doble de RMS que el fallado (3.47 vs 1.68 g). La detección exige mirar la *forma* de
  la señal (kurtosis), no su energía.

- **Un máximo de kurtosis espectral no es un diagnóstico.** Los canales sanos M1-C1 y
  M1-C2 alcanzan SK de 4.5 y 7.5, mayores que el 1.97 del canal fallado. Peor: aplicado al
  registro de ruido, el kurtograma da SK ≈ 244 producido por un único *glitch* en una
  banda sin señal. El kurtograma dice *dónde mirar*; el espectro de envolvente dice
  *qué hay*.

- **Un indicador espectral de falla debe normalizarse por el fondo local.** La energía
  absoluta de la envolvente en f_BPFI no separa nada (índice de Fisher J ≈ 0.2): mide el
  nivel de vibración del canal. La relación pico/fondo da J ≈ 5.3, con 88 % de detección
  y 0 % de falsas alarmas sobre la referencia.

- **La tolerancia de búsqueda debe absorber el deslizamiento.** El pico real está 7.3 Hz
  por debajo del BPFI teórico. Un detector que busque el valor teórico con ±3 % no lo
  encuentra y declara el equipo sano. Mínimo ±5 %.

## Limitaciones

- Una sola medición por estado y sin histórico: no hay forma de estimar la tasa de falsas
  alarmas del umbral ni la tendencia de la falla. El umbral μ + 3σ es un prototipo
  metodológico, no una calibración industrial.
- Los canales "sanos" son otro punto del mismo equipo y dos de otro ventilador, no el
  mismo punto en estado sano.
- Z = 19 se dedujo de las identidades de consistencia sobre el reporte SKF; no se dispone
  de la geometría interna de fábrica. El paso 7 deja la celda de revalidación preparada.
- No se estimó severidad ni vida remanente: requieren seguimiento en el tiempo.
