# Registro de uso de IA — TP2 Compresión de audio con wavelets

Herramientas: Claude (Claude Code y aplicación de escritorio) y ChatGPT. Modelos indicados en los registros originales: Claude Sonnet 5.5, Claude Opus 5.5 y GPT-6.

Se presentan las consultas completas tal como figuran en los dos registros proporcionados, conservando el texto y el código pegados. Se integraron por parte del TP y por etapa del análisis, manteniendo el orden de los mensajes dentro de cada fuente. La numeración original tenía saltos; aquí se renumera consecutivamente sin inventar consultas ausentes. Al no haber marcas temporales compartidas entre las dos fuentes, la intercalación entre Claude y ChatGPT sigue la progresión del trabajo, no una cronología horaria verificable.

---


## Parte 1 — Tres audios, al microscopio

### Preparación y carga de audios

**1.** *Claude*

```text
Me podes generar una celda de python que convierta los archivos .m4a de la carpeta audios/ a .wav mono para copiar en un notebook
```

**2.** *Claude* (se pegó el error que dio la celda)

```text
---------------------------------------------------------------------------
FileNotFoundError                         Traceback (most recent call last)
Cell In[3], line 8
      6 for m4a in sorted(audios_dir.glob("*.m4a")):
      7     wav = m4a.with_suffix(".wav")
----> 8     audio = AudioSegment.from_file(m4a, format="m4a").set_channels(1)  # mono
      9     audio.export(wav, format="wav")
     10     print(f"{m4a.name} -> {wav.name}  ({audio.frame_rate} Hz, mono)")

File c:\Users\glouz\AppData\Local\Programs\Python\Python313\Lib\site-packages\pydub\audio_segment.py:728, in AudioSegment.from_file(cls, file, format, codec, parameters, start_second, duration, **kwargs)
    726     info = None
    727 else:
--> 728     info = mediainfo_json(orig_file, read_ahead_limit=read_ahead_limit)
    729 if info:
    730     audio_streams = [x for x in info['streams']
    731                      if x['codec_type'] == 'audio']

File c:\Users\glouz\AppData\Local\Programs\Python\Python313\Lib\site-packages\pydub\utils.py:274, in mediainfo_json(filepath, read_ahead_limit)
    271         file.close()
    273 command = [prober, '-of', 'json'] + command_args
--> 274 res = Popen(command, stdin=stdin_parameter, stdout=PIPE, stderr=PIPE)
    275 output, stderr = res.communicate(input=stdin_data)
    276 output = output.decode("utf-8", 'ignore')

File c:\Users\glouz\AppData\Local\Programs\Python\Python313\Lib\subprocess.py:1036, in Popen.__init__(self, args, bufsize, executable, stdin, stdout, stderr, preexec_fn, close_fds, shell, cwd, env, universal_newlines, startupinfo, creationflags, restore_signals, start_new_session, pass_fds, user, group, extra_groups, encoding, errors, text, umask, pipesize, process_group)
   1032         if self.text_mode:
   1033             self.stderr = io.TextIOWrapper(self.stderr,
   1034                     encoding=encoding, errors=errors)
-> 1036     self._execute_child(args, executable, preexec_fn, close_fds,
   1037                         pass_fds, cwd, env,
   1038                         startupinfo, creationflags, shell,
   1039                         p2cread, p2cwrite,
   1040                         c2pread, c2pwrite,
   1041                         errread, errwrite,
   1042                         restore_signals,
   1043                         gid, gids, uid, umask,
   1044                         start_new_session, process_group)
   1045 except:
   1046     # Cleanup if the child failed starting.
   1047     for f in filter(None, (self.stdin, self.stdout, self.stderr)):

File c:\Users\glouz\AppData\Local\Programs\Python\Python313\Lib\subprocess.py:1548, in Popen._execute_child(self, args, executable, preexec_fn, close_fds, pass_fds, cwd, env, startupinfo, creationflags, shell, p2cread, p2cwrite, c2pread, c2pwrite, errread, errwrite, unused_restore_signals, unused_gid, unused_gids, unused_uid, unused_umask, unused_start_new_session, unused_process_group)
   1546 # Start the process
   1547 try:
-> 1548     hp, ht, pid, tid = _winapi.CreateProcess(executable, args,
   1549                              # no special security
   1550                              None, None,
   1551                              int(not close_fds),
   1552                              creationflags,
   1553                              env,
   1554                              cwd,
   1555                              startupinfo)
   1556 finally:
   1557     # Child is launched. Close the parent's copy of those pipe
   1558     # handles that only the child should have open.  You need
   (...)   1561     # pipe will not close when the child process exits and the
   1562     # ReadFile will hang.
   1563     self._close_pipe_fds(p2cread, p2cwrite,
   1564                          c2pread, c2pwrite,
   1565                          errread, errwrite)

FileNotFoundError: [WinError 2] El sistema no puede encontrar el archivo especificado
```

### Parte 1


### Análisis de sparsity y elección del nivel J

**3.** *Claude*

```text
lee TPs\TPs-Labo_DSP\TP2\TP2_compresion_audio.ipynb
```

**4.** *Claude*

```text
los archivos .wav ya existen. deje la celda comentada para el profesor. quiero que vayamos de a poco. principalmente voy a necesitar ayuda con el código y planeo hacer preguntas puntuales para los analisis. antes de arrancar parte 1: que representa el nivel J?
```

**5.** *Claude* (con el notebook de la clase 8 adjunto)

```text
@"C:\Users\glouz\Documents\ITBA\5to_Ano\2Q\Labo_DSP\notebooks\08_wavelets.ipynb"
okay, arranquemos con el codigo. cuando pide una daubechis usa db4. adjunto el notebook de la C8 para el grafico de niveles
```

**6.** *Claude*

```text
es muy raro el resultado. decime si lo estoy interpretando mal, pero parece que DCT le gana al resto! en la percusiva (caso tipico de Haar) gana bior4.4 y db4, que está pasando?
```

**7.** *Claude* (sin texto: se adjuntó una captura del gráfico «percusivo: error al retener M»)



**8.** *Claude*

```text
dame una celda de codigo para el paso 2, ayudame a visualizar los distintos J en una sola imagen. Y evidenciar los problemas de J chico o grande que indica la consigna.
```

**9.** *Claude* (se pegó el tramo de código a modificar)

```text
dame este tramo de codigo pero que muestre tres señales en vez de dos, agregué un valor a J_comparar. 

# Figura 2: la curva de error para los dos J, un panel por audio
fig, axes = plt.subplots(1, 3, figsize=(11, 3.8), sharey=True)
for ax, (nombre, (x, _)) in zip(axes, señales.items()):
    for j, estilo in zip(J_COMPARAR, ["--", "-"]):
        c, error = curvas_sparsity(coeficientes(x, FAM_J, nivel=j))
        ax.loglog(np.arange(1, len(c) + 1) / len(c) * 100, error, estilo, lw=1.4, label=f"$J={j}$")
    ax.set_title(nombre)
    ax.set_xlabel("% de coeficientes retenidos")
    ax.set_xlim(0.1, 100)
    ax.set_ylim(1e-4, 1)
    ax.legend()
axes[0].set_ylabel("error relativo")
fig.suptitle(f"Mismo audio, misma familia ({FAM_J}), dos niveles de descomposición")
plt.tight_layout()
plt.show()
```

**10.** *Claude*

```text
dame la celda de la figura de niveles del percusivo
```

**11.** *Claude*

```text
que hace que un audio sea sparse? como puede uno esperar que algo sea o no sparse
```

**12.** *Claude*

```text
que significa "donde viven los coeficientes"? veo que estan alineados a los impactos y casi nulos en el silencio, pero no enteindo bien la pregunta
```

**13.** *Claude*

```text
corregí los comentarios y agregá los pies de foto directametne en el archivo. 
```


### Registro de consultas de la Parte 1

**14.** *Claude*

```text
crea el archivo de memoria de ia separado por partes y pone lo que te fui preguntando en parte 1
```

---


---


## Parte 2 — La curva tasa–distorsión

### Comparación entre SNR global y local del ataque percusivo

**15.** *ChatGPT*

````text
hacelas todas las transformadas en el mismo grafico
````

**16.** *ChatGPT* (Se adjuntó una captura de error al ejecutar esta celda.)

````text
# 3. Graficar todas las transformadas en un único gráfico

porcentajes = np.array(FRACCIONES) * 100

fig, ax = plt.subplots(figsize=(11, 5.5))

colores = {
    "haar": "tab:blue",
    "db4": "tab:orange",
    "bior4.4": "tab:green",
    "dct": "tab:red"
}

for familia in FAMILIAS:

    snr_global = resultados_snr["percusivo"].loc[familia].to_numpy(dtype=float)
    snr_local = resultados_ataque[familia]

    ax.plot(
        porcentajes, snr_global,
        "o-", color=colores[familia],
        linewidth=1.8, markersize=4,
        label=f"{familia} — global"
    )

    ax.plot(
        porcentajes, snr_local,
        "s--", color=colores[familia],
        linewidth=1.8, markersize=4,
        label=f"{familia} — ataque"
    )

ax.set_xscale("log")
ax.set_xticks([1, 2, 3, 5, 7, 10, 25, 50])
ax.set_xticklabels(["1", "2", "3", "5", "7", "10", "25", "50"])

ax.set_xlabel("Coeficientes retenidos (%)")
ax.set_ylabel("SNR de reconstrucción (dB)")
ax.set_title("Audio percusivo — SNR global vs. SNR local en un ataque")

ax.grid(True, which="both", alpha=0.3)
ax.legend(ncol=2, fontsize=9)

plt.tight_layout()
plt.show()
````

**17.** *ChatGPT*

````text
hace una cosa mejor, vamos por partes, hace el grafico solo de la localizada, las 4 familias en un grafico
````

**18.** *ChatGPT*

````text
buenisimo, funciono bien en est acelda. # Parte 2 — SNR local en un ataque percusivo

x, fs = señales["percusivo"]

# Buscar el pico de un golpe cerca del segundo 2
inicio_busqueda = int(1.5 * fs)
fin_busqueda = int(2.5 * fs)

pico = inicio_busqueda + np.argmax(
    np.abs(x[inicio_busqueda:fin_busqueda])
)

# Ventana: 10 ms antes y 90 ms después del pico
inicio = max(0, pico - int(0.010 * fs))
fin = min(len(x), pico + int(0.090 * fs))

print(f"Ataque seleccionado: {pico/fs:.3f} s")
print(f"Ventana analizada: {inicio/fs:.3f} a {fin/fs:.3f} s")

# Calcular SNR local para cada familia y porcentaje
resultados_ataque = {}

for familia in FAMILIAS:
    snr_locales = []

    for fraccion in FRACCIONES:
        xr = comprimir(x, familia, fraccion)
        snr_local = snr_db(x[inicio:fin], xr[inicio:fin])
        snr_locales.append(snr_local)

    resultados_ataque[familia] = snr_locales

# Graficar las cuatro familias
porcentajes = np.array(FRACCIONES) * 100

fig, ax = plt.subplots(figsize=(10, 5))

for familia in FAMILIAS:
    ax.plot(
        porcentajes,
        resultados_ataque[familia],
        marker="o",
        linewidth=1.8,
        label=familia
    )

ax.set_xscale("log")
ax.set_xticks([1, 2, 3, 5, 7, 10, 25, 50])
ax.set_xticklabels(["1", "2", "3", "5", "7", "10", "25", "50"])

ax.set_xlabel("Coeficientes retenidos (%)")
ax.set_ylabel("SNR local (dB)")
ax.set_title("Audio percusivo — SNR local en un ataque")
ax.grid(True, which="both", alpha=0.3)
ax.legend(title="Transformada")

plt.tight_layout()
plt.show()



pero mejor ahora agregale las curvas de la snr global en el mismo grafico asi pueden compararse, con otro estilo de linea.
````

**19.** *ChatGPT* (Sin texto: se adjuntó una captura del gráfico de SNR global vs. SNR local.)

````text
le podemos agregar un punto a la curva de la local? en 15%
````

**20.** *ChatGPT* (Sin texto: se adjuntó una captura del gráfico luego de agregar el 15 %.)



**21.** *ChatGPT*

````text
ok. lo de la dct parece esperable pq no localiza en el tiempo.  te consulto esta bien mi raoznamiento onda d q al analizar mas tiempo como q la energia del golpe se distribuye en tiempos donde no hay señal entonces como q se promedia todo y la amplitud promedio es menor y eso t hace valorar una peor snr adaptadaa ahi? no se, cual seria la explic pasame asi la pongo en el .md.
````

**22.** *ChatGPT*

````text
ok, y estaria bueno destacar  q ahora se peude ver una rodillita entre 10 y 15 o bueno region donde cae
````

**23.** *ChatGPT*

````text
agregame una "nota: se agrego medicion al 15% para visualizar mejor la caida
````

**24.** *ChatGPT* (Se adjuntó una captura de la consigna de la Parte 2.)

````text
La SNR local de las wavelets resulta mayor que la global, especialmente al conservar más coeficientes. Esto se debe a que la energía de la señal percusiva se concentra en los golpes, mientras que el error de reconstrucción también puede aparecer en los intervalos de baja amplitud entre ellos. Al calcular la SNR global, estos errores adicionales reducen la relación entre la energía de la señal y la del error. En cambio, al analizar únicamente el ataque, obtenemos una SNR mayor. Por otro lado, la DCT presenta valores globales y locales similares, lo cual es esperable porque sus funciones base no están localizadas temporalmente y representan peor los transitorios. Además, al analizar la SNR local se distingue con mayor claridad una especie de rodilla alrededor del 10–15 % de coeficientes retenidos, especialmente en las wavelets. Por debajo de esa región, la pérdida de SNR se vuelve más pronunciada, lo que sugiere que estamos comenzando a descartar coeficientes importantes para reconstruir fielmente el ataque.
 reforumulala asi responde eso
````


### Revisión de figuras y análisis de la rodilla

**25.** *Claude*

```text
primera tarea: agregá pies de foto en los graficos que no lo tienen basandote en el analisis de los markdowns, y quiero que agregues en la curva tasa distorsion puntos por encima de 50% para ver la rodilla que intuyo esta mas arriba
```

---


---


## Parte 3 — Elegí, y defendela

### Criterios de selección y metodología de escucha

**26.** *ChatGPT*

````text
bueno, vamos a ir con la parte 3 q pide esto Parte 3 — Elegí, y defendela

> **A partir de C9 · 29/09**

Esta parte casi no tiene código, y es la que más pesa.

Para cada uno de tus tres audios, elegí **una familia y una fracción** para dos usos distintos: (a) *transparencia* — que no se note—, y (b) *la máxima compresión que tolerarías* para mandar ese audio por un canal malo. Son seis decisiones, y cada una se defiende con la curva de la parte 2 **y** con tu escucha.

**Qué hay que responder.**

- Para cada decisión: qué medición la sostiene, y qué escuchaste que el número no decía.
- ¿En qué contenido la SNR y tu oído estuvieron más en desacuerdo? ¿Por qué ahí?
- ¿Hay alguna elección donde familias distintas empatan en SNR pero no en escucha? Ésa es la más valiosa: documentala con los dos audios guardados.

> Las elecciones pueden diferir de las de otro grupo y estar las dos bien. Lo que se corrige es el argumento: una elección defendida con una medición y una escucha documentada vale; la misma elección defendida con «sonaba bien», no.

en q me tengo q basar para decidir? entiendo q para elegir la familia elijo en cada caso la q predomina: tonal DCT y para las otras 2 bio4 .4 auqnue por otro lado capaz no suena como dice la snr, capaz lo mejor sea primero elegir la fraccion y ahi comparar los audios?
````

**27.** *ChatGPT*

````text
ok y como lo encaro? o sea primero vamos con el tonal ponele.  se me ocurre probar la dct al 50 y al 10 e ir probando, hasta encontrar el minimo transparente. una vez hecho esto, lo comparo con otra familia cercana como db4 o bio4.4 para ver si efectivamente dct era mejor
````


### Audio tonal — Transparencia y máxima compresión

**28.** *ChatGPT*

````text
bueno perfecto, vamos con el codigo del tonal, primero transparencia y despues maxima compresion. vamos a hacer celda individual para cada audio. haceme la parte de la celda q comprime el tonal a un 50 con un dct
````

**29.** *ChatGPT*

````text
que tengo q tocar para cambiar el prcentaje ? asi no te reprompteo cada 2 por 3
````

**30.** *ChatGPT*

````text
# Parte 3 — Audio tonal: DCT con 50 % de coeficientes

from IPython.display import Audio, display

x, fs = señales["tonal"]

# Comprimir y reconstruir conservando el 50 % de los coeficientes
xr = comprimir(x, "dct", 0.50)

print(f"SNR: {snr_db(x, xr):.2f} dB")

print("Original:")
display(Audio(x, rate=fs, normalize=False))

print("DCT — 50 %:")
display(Audio(xr, rate=fs, normalize=False))
 tuneala asi lo toco mas facil
````

**31.** *ChatGPT*

````text
\--------------------------------------------------------------------------- ValueError                                Traceback (most recent call last) Cell In[14], line 22      18 print("\nOriginal:")      19 display(Audio(x, rate=fs, normalize=**False**))      20       21 print(f"\n{familia} — {porcentaje}%:") ---> 22 display(Audio(xr, rate=fs, normalize=**False**))  ValueError: Audio data must be between -1 and 1 when normalize=False. ´puse 25 y tira eso
````

**32.** *ChatGPT*

````text
no. tenes q normalizar para no clipear. normalizalo en misma escala auditiva evitando el cliping
````

**33.** *ChatGPT*

````text
en el 10% ya siento la diferencia ponele pero porque eleimino el ruido de fondo, la señal sigue quedando joya, agregale a esta celda para que calcule en el medio la del 20% asi la contrasto con 15 y la original para mostrar q 20 es la respuesta del transparente
````

**34.** *ChatGPT*

````text
# Parte 3 — Audio tonal: máxima compresión tolerable

porcentaje = 1  # Cambiar acá para probar otros porcentajes

xr_max = comprimir(x, familia, porcentaje / 100)

# Usar la misma escala que en la comparación anterior
# Si el nuevo audio supera el rango, ampliar la escala para evitar clipping
escala_max = max(escala, np.max(np.abs(xr_max)) / 0.99)

print(f"DCT — {porcentaje}% | SNR: {snr_db(x, xr_max):.2f} dB")
display(Audio(xr_max / escala_max, rate=fs, normalize=False))

agregale aca que te genere el audio de 0,5 % porque ahi vi y el 1% se puede mandar y el 0,5 ya se pierde, asi muestro todos
````

**35.** *ChatGPT*

````text
agregame la generacion de bior4.4 y de db4 al 1% asi comparo las 3, porq db4 y bior tan empatadas
````

**36.** *ChatGPT*

````text
bueno respondamos en tonces que para tonal elijo dct por esos motivos, de los graficos, y la razon auditiva esa del ruido, tambien agrega ese dato d q aveces menos snr no significa peor audible sino q a veces t limpia ruido y termina siendo mejor, y justifica la auditivilidad diciendo que siendo q es una cancion de piano y se quisiera comprimir, imaginamos un caso donde alguien quiere reconstruir esa cancion por ejemplo para tocarla en su casa oe scribir la partitura, y hasta ese punto se lograba distinguir los acordes y la melodia mientras q con menos % ya las notas se confundian con el ruido
````

**37.** *ChatGPT*

````text
agregale una oracion d q finalmente comparamos este peor casos con las otras dos familias para validar la decision entre familias y efectivamente la diferencia era notorioa
````


### Audio de voz — Transparencia y máxima compresión

**38.** *ChatGPT*

````text
bueno ahora vamos a ver la transparencia de la voz, primero comparemos  bior4.4 la original y un porcentaje arbitrario para q yo pueda ir modificando
````

**39.** *ChatGPT*

````text
# Parte 3 — Audio de voz: prueba de transparencia

from IPython.display import Audio, display

# ===== MODIFICAR SOLO ESTO =====
familia = "bior4.4"
porcentaje = 45
# ===============================

x, fs = señales["voz"]

# Comprimir y reconstruir
xr = comprimir(x, familia, porcentaje / 100)

# SNR de reconstrucción
print(f"Familia: {familia} | Coeficientes retenidos: {porcentaje}%")
print(f"SNR: {snr_db(x, xr):.2f} dB")

# Normalización conjunta para evitar clipping
pico_maximo = max(np.max(np.abs(x)), np.max(np.abs(xr)))
escala = pico_maximo / 0.99 if pico_maximo > 0 else 1.0

print("\nOriginal:")
display(Audio(x / escala, rate=fs, normalize=False))

print(f"\n{familia} — {porcentaje}%:")
display(Audio(xr / escala, rate=fs, normalize=False)) agregale para q ademas muestre con 45% asi comparo 50 con 45 para msotrar q 50 es lo maximo de transparencia pq ya se nota q noes el mismo audio sino
````

**40.** *ChatGPT*

````text
agregame las celdas para comparar maxima compresion ahora que calcule 2 casos asi voy comparando de a 2. arranca con 2 y 10%
````

**41.** *ChatGPT*

````text
perfecto, ahora agregame una partecita de codigo q muestre el 10% de db4, asi los comparo
````

**42.** *ChatGPT*

````text
# Parte 3 — Audio de voz: comparación db4 al 10 %

xr_db4 = comprimir(x, "db4", 0.10)

# Mantener la escala de la comparación anterior, evitando clipping
escala_db4 = max(escala_comp, np.max(np.abs(xr_db4)) / 0.99)

print(f"db4 — 10 % | SNR: {snr_db(x, xr_db4):.2f} dB")
display(Audio(xr_db4 / escala_db4, rate=fs, normalize=False))
 hacemelo parametrizable para cambiar el porcentaje
````

**43.** *ChatGPT*

````text
# Parte 3 — Audio de voz: comparación de transparencia (50 % vs. 45 %)

from IPython.display import Audio, display

x, fs = señales["voz"]
familia = "bior4.4"

# Reconstruir ambas versiones
xr_50 = comprimir(x, familia, 0.50)
xr_45 = comprimir(x, familia, 0.45)

# Normalización conjunta para evitar clipping
pico_maximo = max(
    np.max(np.abs(x)),
    np.max(np.abs(xr_50)),
    np.max(np.abs(xr_45))
)
escala = pico_maximo / 0.99 if pico_maximo > 0 else 1.0

# Escuchar y comparar
print("Original:")
display(Audio(x / escala, rate=fs, normalize=False))
print("Comparación de transparencia")
print(f"\nbior4.4 — 50 % | SNR: {snr_db(x, xr_50):.2f} dB")
display(Audio(xr_50 / escala, rate=fs, normalize=False))

print(f"\nbior4.4 — 45 % | SNR: {snr_db(x, xr_45):.2f} dB")
display(Audio(xr_45 / escala, rate=fs, normalize=False))

print("Comparación de compresión:")
 cambialo para q en vez d 45 genere 40%
````

**44.** *ChatGPT*

````text
bueno la aleeccion de esto fue bior4.4 para 50 y 10 % respectivamente, er ala que mejor snr tenia y al compararla con db4 que estaba ahi cerquita en el 10% vimos diferencias practicamnte nulas en el senoido pero esta presenta mejor relacion señal a ruido. en l 50 llegamos bien ya dps aparece ruido de fondo como cdo frotas una birulana que se percibe q el audio e distinto. aceptamos hasta un 10% porque despues ya las palabras no se entienden por completo y si bien puedan salir por contexto, se prioriza conservar unos pocos coeficientes mas a cambio de poder resolver la palabra perfectamente dado q no siempre todo sale x contexto. armame la respuestita para justificar la eleccion de voz en el .md
````


### Audio percusivo — Transparencia y máxima compresión

**45.** *ChatGPT*

````text
bueno buenisimo ahora vamos con la percusion, repitamos el analisis con bior4.4, haceme una celda que haga la original y estas dos pero que en cada una pueda parametrizar su porcentaje.
````

**46.** *ChatGPT*

````text
# Parte 3 — Audio percusivo: comparación de reconstrucciones

from IPython.display import Audio, display

# ===== MODIFICAR SOLO ESTO =====
familia = "bior4.4"
porcentaje_1 = 20
porcentaje_2 = 15
# ===============================

x, fs = señales["percusivo"]

# Reconstruir ambas versiones
xr_1 = comprimir(x, familia, porcentaje_1 / 100)
xr_2 = comprimir(x, familia, porcentaje_2 / 100)

# Normalización conjunta: misma escala y sin clipping
pico_maximo = max(
    np.max(np.abs(x)),
    np.max(np.abs(xr_1)),
    np.max(np.abs(xr_2))
)
escala = pico_maximo / 0.99 if pico_maximo > 0 else 1.0

# Escuchar y comparar
print("Original:")
display(Audio(x / escala, rate=fs, normalize=False))

print("Comparación de transparencia")
print(f"\n{familia} — {porcentaje_1:g}% | SNR: {snr_db(x, xr_1):.2f} dB")
display(Audio(xr_1 / escala, rate=fs, normalize=False))

print(f"\n{familia} — {porcentaje_2:g}% | SNR: {snr_db(x, xr_2):.2f} dB")
display(Audio(xr_2 / escala, rate=fs, normalize=False))

tengo esto, agregame un pedacito que imprima una sola compresion con db4 en 20% para comparar, q sea paremtrizable su porcentaje
````

**47.** *ChatGPT*

````text
bueno ahora comparemos hasta cuando podriamos comprimir con bior4.4  hacelo parametrizable poneme para probar con 10 y 2%
````

**48.** *ChatGPT*

````text
perfecto el maximo aceptable fue de 5, agregame una compresion parametrizable de db4 en 5%
````

**49.** *ChatGPT*

````text
bueno haceme la celdita markdown que diga q en maxima compresion llegamos hasta 5% con bior4.4, la eleccion fue porque siendo que es un elemento percusivo pensado como golpes, si bien es importante q se vea un ataque con cierta duracion, tambien importa el timbre (no se si timbre es la palabra o color usala vos la palabra correcta) que mantenga del sonido original, por ejemplo si uno lo piensa como el microfoneo de una bateria, esta no solo importa q marque los golpes a tiempo y con un ataque sino que distinga el color de la parte q se golpea para distinguir sus partes (timbre particular) . 
````

**50.** *ChatGPT*

````text
y decile q comparamos con db4 en la maxima compresion y era bastante similar con un snr practicamente identico pero no conservaba tan bien el timbre distorsionandolo, ponelo en una oracion asi agrego
````

**51.** *Claude*

```text
en la escucha de los audios percusivos para mantener transparencia, pude escuchar como un ruido que es como unos "puntitos" de ruido, como si dejaran caer un grano de arena a la vez en el microfono. Similar a lo escuchado en radio am en mi experiencia. Como es el nombre del fenomeno? o como lo explico claramente.
```


### Comparación general de familias y refinamiento del análisis de voz

**52.** *Claude*

```text
quiero que agregues en la parte 3 (codigo), al resto de las familias. lo que tenemos ahora es una eleccion basada en el snr. quiero considerar que puede ser que el snr diga una cosa, pero al escuchar, otra familia sea mas transparente. Mismas fracciones que las y analizadas para cada caso, pero todas las familias. Si es posible, agregá prints para no perderse entre todos los audios del notebook, separando por ejemplo: Titulo: TONAL subtitulo: transparencia subsubtitulo familia x
```

**53.** *Claude*

```text
puedo borrar las celdas viejas de la parte 3 donde hacia audios? si ahora en la que hiciste vos se hacen todos los audios de vuelta y mas prolijamente ordenados
```

**54.** *Claude*

```text
ya lo borré. estoy escuchando y encontré algo: en el audio de voz, la transparencia gana bior, pero en maxima compresion gana DCT. te parece algo esperable? como justificarias? se me ocurre que mantiene la fundamental de la voz y algunos armonicos
```

**55.** *Claude*

```text
pasame la celda de los espectrogramas
```

**56.** *Claude* (con una captura de los espectrogramas de voz: original, bior4.4 y DCT al 7 %)

```text
Se ve que la DCT tiene un piso de ruido blanco, es lo que expliqué en la celda de analisis. que te parece el resto? los baches negros en bior4.4 sostienen el analisis?
```

---


---


## Parte 5 — Denoising

### Escucha de artefactos y análisis del umbral

**57.** *Claude*

```text
uh, se va el ruido pero no es nada transparente. es lo logico no?
```

**58.** *Claude* (con una captura del zoom en los 200 ms más débiles del audio tonal)

```text
por que la original se va a 0 por tramos?
```

**59.** *Claude*

```text
dame un checklist de temas a analizar en la parte 5. por ejemplo: snr de umbral blando no presenta mejoras significativas, mejora umbral duro, coeficientes de f>3kHz mueren todos, conserva frecuencias de energía, etc. inclui todos los temas a cubrir para contestar las preguntas
```

---


---


## Extensiones

### SWT y fundamentación bibliográfica

**60.** *Claude*

```text
explicame como funciona la SWT
```

**61.** *Claude* (con el paper de Wang y Dai, 2018, adjunto)

```text
@"C:\Users\glouz\Downloads\25902510.pdf"
Te paso este pdf porque lo use como bibliografia para el analisis de la parte 5. Ayudame a completar el código de la celda.
```


---


## Documentación del TP y registro de IA

### Registro de los prompts

**62.** *ChatGPT*

````text
haceme un compilado de todos los propmts que te pedi para este tp
````

**63.** *Claude*

```text
actualizá el registro_IA con las preguntas de las partes 2 a 5
```



---
