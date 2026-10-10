# Registro de uso de IA — TP2 Compresión de audio con wavelets

Herramienta: Claude (Claude Code, app de escritorio). Modelos: Claude Sonnet 5.5 y, desde la pregunta 6, Claude Opus 5.5.

Preguntas completas, en orden y sin editar. Cuando la pregunta incluía texto pegado (un error o código), va a continuación tal como se pegó.

---

## Parte 1 — Tres audios, al microscopio

### Carga de los audios (antes de arrancar la Parte 1)

**1.**

```text
Me podes generar una celda de python que convierta los archivos .m4a de la carpeta audios/ a .wav mono para copiar en un notebook
```

**2.** (se pegó el error que dio la celda)

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

**3.**

```text
lee TPs\TPs-Labo_DSP\TP2\TP2_compresion_audio.ipynb
```

**4.**

```text
los archivos .wav ya existen. deje la celda comentada para el profesor. quiero que vayamos de a poco. principalmente voy a necesitar ayuda con el código y planeo hacer preguntas puntuales para los analisis. antes de arrancar parte 1: que representa el nivel J?
```

**5.** (con el notebook de la clase 8 adjunto)

```text
@"C:\Users\glouz\Documents\ITBA\5to_Ano\2Q\Labo_DSP\notebooks\08_wavelets.ipynb"
okay, arranquemos con el codigo. cuando pide una daubechis usa db4. adjunto el notebook de la C8 para el grafico de niveles
```

**6.**

```text
es muy raro el resultado. decime si lo estoy interpretando mal, pero parece que DCT le gana al resto! en la percusiva (caso tipico de Haar) gana bior4.4 y db4, que está pasando?
```

**7.** (sin texto: se adjuntó una captura del gráfico «percusivo: error al retener M»)

**8.**

```text
dame una celda de codigo para el paso 2, ayudame a visualizar los distintos J en una sola imagen. Y evidenciar los problemas de J chico o grande que indica la consigna.
```

**9.** (se pegó el tramo de código a modificar)

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

**10.**

```text
dame la celda de la figura de niveles del percusivo
```

**11.**

```text
que hace que un audio sea sparse? como puede uno esperar que algo sea o no sparse
```

**12.**

```text
que significa "donde viven los coeficientes"? veo que estan alineados a los impactos y casi nulos en el silencio, pero no enteindo bien la pregunta
```

**13.**

```text
listo. la parte 1 done. te parece que falta algo? pegale una leida
```

**14.**

```text
corregí los comentarios y agregá los pies de foto directametne en el archivo. ya me ocupé del resto de las cosas
```

**15.**

```text
crea el archivo de memoria de ia separado por partes y pone lo que te fui preguntando en parte 1
```

---

## Parte 2 — La curva tasa–distorsión

---

## Parte 3 — Elegí, y defendela

---

## Parte 4 — El test de escucha

---

## Parte 5 — El mismo acto: denoising

---

## Extensiones


## Referencias 

## Cita de autores
Para los audios recite el poema 20 de pablo neruda de Veinte poemas de amor y una canción desesperada (1924).  y la cancion she's electric de oasis, interpretada en pinao por mi, citame esas dos cossas asi lo pego