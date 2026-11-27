"""Genera dataset_doa.npz para el TP3, a partir de LOCATA (tarea 2, conjunto de desarrollo).

Datos: LOCATA Challenge, dev.zip (Zenodo, record 3630471), tarea 2 (varios parlantes fijos,
arreglo fijo), grabación 1, arreglo DICIT. Se lee directamente del zip, sin extraerlo: solo
hacen falta el audio del arreglo, las posiciones y las etiquetas de actividad de voz.

Elecciones, con su regla:

- Subarreglo de 8 cm (micrófonos 4, 5, 7, 10, 11, M = 5): a ~2 kHz da d ≈ λ/2 (sin réplicas
  de grating) y su campo lejano, 2L²/λ ≈ 1,2 m con L = 32 cm, queda por debajo de la
  distancia a los parlantes (~1,4 y ~1,5 m). Los de 16 y 32 cm resuelven mejor, pero piden
  frecuencias más bajas y su campo lejano (2,4 m y más) ya no se cumple en esta sala.
- Frecuencia de trabajo: el bin de la STFT más cercano a 2 kHz.
- STFT con ventana Hann de 1024 muestras (21 ms, bins de 46,9 Hz) y salto de 512. El tiempo
  que tarda la onda en cruzar el subarreglo (L/c ≈ 0,9 ms) es mucho menor que la inversa del
  ancho del bin (~21 ms): la hipótesis de banda angosta se sostiene.
- Snapshots: solo las ventanas en las que los dos parlantes están activos según sus VAD.
- Grabación 1 y no 3: en los tramos con un solo parlante activo, el retardo entre los
  micrófonos 4 y 11 (y entre 1 y 14) medido con GCC-PHAT coincide con el que predicen las
  posiciones en la grabación 1 (−25 contra −24,4 muestras), pero en la grabación 3 sale con
  la magnitud correcta y el signo opuesto: su verdad geométrica no se pudo validar.

La verdad (sin θ = û·ê, con ê del último sensor al primero y û del centro del subarreglo a
cada parlante) se guarda aparte, en la clave `verdad`, para compararla recién después de
estimar.

Si el zip no está, `python convertir.py --sintetico` arma la escena con el generador de
cátedra, que fue el plan B mientras la descarga no andaba.

Uso: python convertir.py [ruta/a/dev.zip]   → escribe dataset_doa.npz junto a este archivo.
"""
import io
import sys
import zipfile
from pathlib import Path

import numpy as np
from scipy.io import wavfile
from scipy.signal import stft

GRABACION = 1
PARLANTES = [3, 4]                    # los parlantes de la grabación 1
MICROFONOS = [4, 5, 7, 10, 11]        # subarreglo de 8 cm, en el orden de la consigna
D_METROS = 0.08
F_OBJETIVO = 2000.0                   # Hz; se usa el bin más cercano
LARGO, SALTO = 1024, 512              # muestras
C_SONIDO = 343.0                      # m/s


def snapshots_stft(x, fs, f_trabajo, largo, salto):
    """x: M×N real, un sensor por fila, en el orden del subarreglo (el de la consigna).
    Devuelve los snapshots del bin más cercano a f_trabajo, su frecuencia y el instante
    (en muestras) del centro de cada ventana."""
    f, t, Z = stft(x, fs=fs, nperseg=largo, noverlap=largo - salto, axis=1)
    b = np.argmin(np.abs(f - f_trabajo))
    return Z[:, b, :], f[b], np.round(t * fs).astype(int)


def leer_tabla(z, nombre):
    """Archivo de texto de LOCATA: encabezado con nombres de columna, separado por tabs."""
    lineas = z.read(nombre).decode().splitlines()
    encabezado = lineas[0].split("\t")
    datos = np.array([[float(v) for v in l.split("\t")] for l in lineas[1:]])
    return encabezado, datos


def leer_vad(z, nombre):
    return np.array(z.read(nombre).decode().split()[1:], dtype=int)


def verdad_geometrica(z, base, microfonos, parlantes):
    """θ de cada parlante respecto de la normal al subarreglo: sin θ = û·ê."""
    enc, arreglo = leer_tabla(z, base + "position_array_dicit.txt")
    pos = np.array([arreglo[0, enc.index(f"mic{k}_x"):enc.index(f"mic{k}_x") + 3] for k in microfonos])
    e = (pos[0] - pos[-1]) / np.linalg.norm(pos[0] - pos[-1])
    centro = pos.mean(axis=0)
    thetas, distancias = [], []
    for s in parlantes:
        enc_s, fuente = leer_tabla(z, base + f"position_source_loudspeaker{s}.txt")
        p = fuente[0, enc_s.index("x"):enc_s.index("x") + 3]
        u = (p - centro) / np.linalg.norm(p - centro)
        thetas.append(np.rad2deg(np.arcsin(u @ e)))
        distancias.append(np.linalg.norm(p - centro))
    return np.array(thetas), np.array(distancias)


def desde_locata(ruta_zip):
    z = zipfile.ZipFile(ruta_zip)
    base = f"dev/task2/recording{GRABACION}/dicit/"

    fs, audio = wavfile.read(io.BytesIO(z.read(base + "audio_array_dicit.wav")))
    x = audio[:, [k - 1 for k in MICROFONOS]].T          # canal k−1 = micrófono k

    X_todo, f, centros = snapshots_stft(x, fs, F_OBJETIVO, LARGO, SALTO)
    vads = [leer_vad(z, base + f"VAD_dicit_loudspeaker{s}.txt") for s in PARLANTES]
    activos = np.logical_and.reduce(vads)
    dentro = centros < len(activos)
    elegidos = np.zeros(len(centros), dtype=bool)
    elegidos[dentro] = activos[centros[dentro]].astype(bool)
    X = X_todo[:, elegidos]

    d_lambda = D_METROS * f / C_SONIDO
    verdad, distancias = verdad_geometrica(z, base, MICROFONOS, PARLANTES)
    descripcion = (
        f"LOCATA (Löllmann et al., 2018), tarea 2, grabación {GRABACION}, arreglo DICIT, "
        f"subarreglo de {D_METROS * 100:.0f} cm (micrófonos {MICROFONOS}). "
        f"f = {f:.1f} Hz (bin de {fs / LARGO:.1f} Hz), d/λ = {d_lambda:.3f}. "
        f"STFT Hann de {LARGO} muestras con salto de {SALTO}; "
        f"{X.shape[1]} de {X_todo.shape[1]} ventanas, las que tienen activos los parlantes {PARLANTES}."
    )
    extras = dict(fs=fs, largo=LARGO, salto=SALTO, grabacion=GRABACION,
                  microfonos=np.array(MICROFONOS), parlantes=np.array(PARLANTES),
                  distancias=distancias, ventanas_totales=X_todo.shape[1])
    return X, d_lambda, f, descripcion, verdad, extras


def desde_sintetico():
    """Plan B: la escena con el generador de cátedra, imitando al subarreglo de 8 cm."""
    rng = np.random.default_rng(2543)
    M, K, f = len(MICROFONOS), 300, F_OBJETIVO
    d_lambda = D_METROS * f / C_SONIDO
    thetas, snrs_db = [-35.0, 10.0, 25.0], [10.0, 5.0, 5.0]
    X = np.sqrt(0.5) * (rng.standard_normal((M, K)) + 1j * rng.standard_normal((M, K)))
    for theta, snr_db in zip(thetas, snrs_db):
        s = np.sqrt(10 ** (snr_db / 10) / 2) * (rng.standard_normal(K) + 1j * rng.standard_normal(K))
        X += np.outer(np.exp(-2j * np.pi * np.arange(M) * d_lambda * np.sin(np.deg2rad(theta))), s)
    descripcion = (f"Escena sintética (generador de cátedra, semilla 2543) que imita el subarreglo "
                   f"DICIT de 8 cm a {f:.0f} Hz: d/λ = {d_lambda:.3f}, 3 fuentes, K = {K}.")
    return X, d_lambda, f, descripcion, np.array(thetas), dict(snrs_db=np.array(snrs_db))


if __name__ == "__main__":
    aqui = Path(__file__).parent
    if "--sintetico" in sys.argv:
        X, d_lambda, f, descripcion, verdad, extras = desde_sintetico()
    else:
        argumentos = [a for a in sys.argv[1:] if not a.startswith("--")]
        ruta_zip = Path(argumentos[0]) if argumentos else aqui / "dev.zip"
        X, d_lambda, f, descripcion, verdad, extras = desde_locata(ruta_zip)

    destino = aqui / "dataset_doa.npz"
    np.savez(destino, X=X, d=d_lambda, descripcion=descripcion,
             f=f, d_metros=D_METROS, c=C_SONIDO, verdad=verdad, **extras)
    print(descripcion)
    print(f"guardado en {destino}  —  X de {X.shape[0]}×{X.shape[1]}")
