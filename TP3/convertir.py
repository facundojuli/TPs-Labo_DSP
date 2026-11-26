"""Genera dataset_doa.npz para el TP3.

El dataset LOCATA (tarea 2, dev.zip) no se pudo descargar: la descarga desde Zenodo queda
trabada en 0 bytes. Como permite la consigna, la escena se arma con el generador sintético
de cátedra, imitando lo que hubiera sido el dato real:

- el subarreglo de 8 cm del arreglo DICIT (M = 5 micrófonos),
- trabajando a 2 kHz, donde d/λ = 0,08 · 2000 / 343 ≈ 0,466 (menor que λ/2: sin réplicas),
- tres fuentes incorreladas fijas (como los parlantes de la tarea 2), dos de ellas más
  cerca entre sí que el Rayleigh de la apertura, y ruido blanco de potencia 1,
- K = 300 snapshots, del orden de lo que dan ~3 s de STFT con ventana de 1024 y salto de 512.

La verdad se guarda aparte (clave `verdad`), para compararla recién después de estimar.

Uso: python convertir.py   → escribe dataset_doa.npz junto a este archivo.
"""
from pathlib import Path

import numpy as np

D_METROS = 0.08          # espaciado del subarreglo de 8 cm
F_TRABAJO = 2000.0       # Hz
C_SONIDO = 343.0         # m/s
M = 5
K = 300
THETAS = [-35.0, 10.0, 25.0]     # grados, medidos desde la normal al arreglo
SNRS_DB = [10.0, 5.0, 5.0]       # por fuente, contra ruido de potencia 1
SEMILLA = 2543


def steering(theta_deg, M, d):
    """Mismo vector de dirección que la notebook: θ > 0 del lado del primer sensor."""
    return np.exp(-2j * np.pi * np.arange(M) * d * np.sin(np.deg2rad(theta_deg)))


def generar_ula(thetas, snrs_db, M, d, K, semilla):
    """El generador sintético de cátedra: fuentes incorreladas + ruido blanco."""
    rng = np.random.default_rng(semilla)
    X = np.sqrt(0.5) * (rng.standard_normal((M, K)) + 1j * rng.standard_normal((M, K)))
    for theta, snr_db in zip(thetas, snrs_db):
        pot = 10 ** (snr_db / 10)
        s = np.sqrt(pot / 2) * (rng.standard_normal(K) + 1j * rng.standard_normal(K))
        X += np.outer(steering(theta, M, d), s)
    return X


if __name__ == "__main__":
    d_lambda = D_METROS * F_TRABAJO / C_SONIDO
    X = generar_ula(THETAS, SNRS_DB, M, d_lambda, K, SEMILLA)
    descripcion = (
        f"Escena sintética (generador de cátedra, semilla {SEMILLA}) en lugar de LOCATA, "
        f"que no se pudo descargar. Imita el subarreglo DICIT de {D_METROS * 100:.0f} cm "
        f"(M = {M}) a f = {F_TRABAJO:.0f} Hz: d/λ = {d_lambda:.3f}. "
        f"{len(THETAS)} fuentes incorreladas, ruido blanco, K = {K} snapshots."
    )
    destino = Path(__file__).with_name("dataset_doa.npz")
    np.savez(destino, X=X, d=d_lambda, descripcion=descripcion,
             verdad=np.array(THETAS), snrs_db=np.array(SNRS_DB))
    print(descripcion)
    print(f"guardado en {destino}  —  X de {X.shape[0]}×{X.shape[1]}")
