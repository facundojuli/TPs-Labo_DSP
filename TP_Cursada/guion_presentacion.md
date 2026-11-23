# Guion: presentación final del TP

Pensado para unos 20 minutos con las 30 diapositivas. Si les dan menos tiempo, las marcadas con **(saltable)** se pasan con una frase. 

---

## Bloque 1: el problema y los datos ( ~3 min)

**1. Portada**
"Vamos a contar cómo diagnosticamos una falla de rodamiento en un ventilador industrial a partir de su vibración"

**2. Qué buscamos y cómo**
"Un defecto localizado no aparece como una línea en el espectro. Cada vez que un rodillo pasa por el defecto hay un impacto, el impacto hace sonar a la estructura en kHz, y la información de la falla queda en la modulación de esa resonancia. Por eso el método central es demodular: análisis de envolvente. Abajo está el recorrido del notebook, en diez pasos."

**3. Datos y rodamiento**
"Tenemos cuatro canales de aceleración a 24 kHz: los dos lados del ventilador 2, que es el sospechoso, y dos puntos de otro ventilador sano. Además medimos el sensor apoyado en un escritorio, como piso de ruido. El rodamiento es un SKF de rodillos a rótula; del reporte de SKF sacamos el BPFI teórico, 180.4 Hz, y dedujimos 19 rodillos por hilera."

---

## Bloque 2: antes de buscar la falla ( ~3 min)

**4. Carga y control de calidad** (saltable)
"Antes de calcular nada verificamos tres cosas: que no haya saturación, la frecuencia de muestreo real y sacar offset y tendencia."

**5. ¿Se puede promediar?** (saltable)
"Los canales son estacionarios: el RMS por ventana varía menos de 3 %. Eso justifica promediar en 60 s."

**6. Piso de ruido: media o mediana** (saltable)
"El registro de ruido tiene un transitorio a los 28 s que mete hasta 10 dB de sesgo en el promedio común. Por eso usamos la mediana para estimar el piso."

**7. El ruido no es blanco**
"La autocorrelación no es una delta y la PSD cae 21.6 dB hacia alta frecuencia. Igual queda entre 37 y 64 dB por debajo de la señal, así que no limita el análisis."

**8. El RMS señala el canal equivocado**
"Primer resultado importante. El lado libre del ventilador 2 vibra el doble que el lado acople, pero es gaussiano: kurtosis cero. El lado acople vibra menos pero es impulsivo. Si alarmáramos por nivel de vibración, que es lo que mira la norma, señalaríamos el canal sano."

**9. La kurtosis alta es persistente**
"No es una ventana rara: la peor ventana de M2-C1 tiene más kurtosis que la mejor de los canales sanos. En el plano RMS–kurtosis los grupos se separan en vertical, no en horizontal. La falla cambia la forma antes que la energía."

---

## Bloque 3: el espectro y la banda ( ~3 min)

**10. Welch, periodograma y ventanas** (saltable)
"El periodograma no mejora con más datos; Welch cambia resolución por varianza. Las ventanas casi no importan acá porque la señal es de banda ancha."

**11. La falla no aparece en el espectro crudo**
"En el espectro de aceleración solo se ven los armónicos del giro y una resonancia en 3.9 kHz que también tienen los sanos. Nada en BPFI."

**12. Modelo AR** (saltable)
"Probamos también un modelo AR. Resuelve los armónicos del giro con orden alto, pero tampoco ve la falla. No es falta de resolución: la falla es una modulación, hay que demodular."

**13. Kurtograma**
"La parte más subjetiva del método es elegir qué banda demodular. El kurtograma la elige con un criterio: dónde la señal es más impulsiva. Para M2-C1 da 1500 a 3000 Hz, no la banda más energética. Ojo: mide contraste, no energía. Sobre el registro de ruido da un valor 124 veces mayor sin que haya señal; por eso usamos guardas."

---

## Bloque 4: envolvente e identificación ( ~4 min)

**14. Envolvente**
"Filtramos en esa banda y tomamos el módulo de la señal analítica con Hilbert. La portadora es la resonancia y la modulante, el tren de impactos."
*Si preguntan por la portadora:* "Hilbert no necesita portadora para existir; lo que la necesita es interpretar el módulo como envolvente. Por el teorema de Bedrosian, vale si la modulante está por debajo de la portadora. Por eso filtramos primero."

**15. Impactos cada 5.77 ms**
"Antes de cualquier transformada ya se ve: solo M2-C1 tiene picos regulares, cada 5.77 ms."

**16. Espectro de envolvente**
"El pico dominante está en 173.2 Hz, con cuatro armónicos y bandas laterales separadas exactamente la frecuencia de giro."

**17. Control negativo**
"Para descartar un artefacto, procesamos los cuatro canales con exactamente los mismos parámetros. La serie aparece solo en M2-C1: 20.6 dB sobre el fondo, contra 1.3 en los sanos."

**18. Validación con el software de planta** (saltable)
"El software de mantenimiento calcula su propia envolvente con otro algoritmo y da el mismo pico."

---

## Bloque 5: cepstrum ( ~4 min). Lo nuevo desde la entrega intermedia

**19. Cepstrum**
"El espectro de envolvente tiene picos repetidos cada 173 Hz. El cepstrum, la IFFT del logaritmo del espectro, detecta justamente eso: una periodicidad dentro del espectro, que aparece como un pico en 1/173 Hz = 5.77 ms. Aparece solo en M2-C1. Pero crudo no mejora el contraste: el logaritmo le da al ruido el mismo peso que a los pocos armónicos."

**20. Liftrado**
"La mejora vino de filtrar en quefrencia, el liftrado: nos quedamos solo con el pico en 5.77 ms, ponemos el resto en cero y volvemos con la FFT. Queda una ondulación limpia en M2-C1 y casi plana en los sanos. Ventana a ventana, la separación pasa de J 5.25 a 11.9, y la peor ventana con falla queda por encima de la mejor sana."

**21. Quefrencias largas: los dos relojes**
"Siguiendo una sugerencia del profesor, miramos quefrencias largas. Los picos más fuertes no están en 60 ms, la vuelta del eje, sino en 121, 179 y 300 ms. La falla tiene dos relojes: un impacto cada 5.77 ms y una vuelta cada 60 ms. Como en una vuelta caben 10.4 impactos, recién se alinean después de 2, 3 o 5 vueltas. A los 300 ms, 52 impactos y 5 vueltas difieren 0.13 ms. Se predice solo con el cociente de frecuencias. Con ventanas de 4 s, este indicador casi duplica la separación."

---

## Bloque 6: identificación y persistencia ( ~2 min)

**22. Identificación**
"Juntando todo: el pico está en 10.4 veces la frecuencia de giro, un múltiplo no entero, así que no es desbalanceo ni nada sincrónico; tiene armónicos, o sea un tren de impactos; y bandas laterales a ±fr, o sea que la fuente gira con el eje. Eso es pista interna. El BPFI de SKF queda a 4 %, por el deslizamiento de los rodillos. El diagnóstico sale de la señal; el fabricante confirma."

**23. Tiempo-frecuencia**
"En el tiempo-frecuencia cada impacto es una estructura vertical alineada con los 5.77 ms. Usamos Morlet porque su forma se parece a un impacto, porque su módulo ya es la envolvente en cada banda y porque su resolución se adapta: ventanas cortas en kHz."

**24. ¿Es persistente?** (saltable)
"La relación pico/fondo es positiva en las 60 ventanas: es un defecto establecido, no un golpe suelto."

---

## Bloque 7: detección y decisión ( ~4 min)

**25. Indicadores de salud y umbral**
"Para un monitor automático reducimos todo a indicadores por ventana de 1 s: kurtosis en banda, que es genérica, y relación pico/fondo en BPFI, que es específica. El umbral es media más tres sigmas de los canales sanos."

**26. Espacio de indicadores**
"El 85 % de las ventanas de M2-C1 cae en el cuadrante de falla y ninguna sana. Un detalle: la primera versión usaba la energía absoluta y no separaba nada, porque el canal sano vibra más. Un indicador espectral tiene que estar normalizado por el fondo local."

**27. Curvas ROC y DET**
"El umbral es una elección entre falsas alarmas y fallas no detectadas. Con ROC y DET barrimos todos los umbrales. El liftrado y la regla B separan sin errores. k = 3 resulta conservador, pero no lo bajamos porque sería ajustar con los mismos datos. Para medir la falsa alarma fuera de muestra fijamos el umbral con dos canales sanos y evaluamos en el tercero: cero falsas alarmas."

**28. Resumen por canal**
"El veredicto: FALLA en M2-C1, OK en los tres sanos y el ruido como medición no válida."

**29. Dos marcos de decisión**
"La opción A es la original. La B cambia el indicador específico por el liftrado. Dan el mismo veredicto, pero la B pone el 96.7 % de las ventanas con falla en el cuadrante, contra 85 %. Y si el monitor se configura con el BPFI teórico, la B sigue detectando todo y la A baja a 80 %: el margen del liftro absorbe el deslizamiento."

---

## Cierre (~1 min)

**30. Conclusiones**
"Tres ideas para llevarse: la forma de la señal detecta la falla antes que su energía; un indicador tiene que estar normalizado por el fondo; y el cepstrum liftrado aprovecha la periodicidad de los impactos mejor que el espectro. La salvedad honesta: es un solo rodamiento fallado y algunos parámetros se ajustaron con estos datos, así que es prometedor pero no está demostrado en general. El paso siguiente es medir periódicamente para tener tendencia."

---

## Preguntas probables y respuesta corta

- **¿Por qué la banda del kurtograma y no la más energética?** La más energética, 3.9 kHz, también la tienen los sanos: es estructural. El kurtograma busca impulsividad, no energía.
- **¿Por qué 173 Hz y no 180?** Deslizamiento de los rodillos y ángulo de contacto real bajo carga. Es normal un 1 a 2 % y puede llegar a 4 %.
- **¿Cómo saben que es pista interna y no externa?** Por las bandas laterales a ±fr: el defecto gira con el eje y pasa por la zona de carga una vez por vuelta. Una falla en pista externa está fija y no las genera.
- **¿Qué es el liftrado?** Un filtro en el dominio de las quefrencias: multiplicar el cepstrum por una ventana y volver con la FFT.
- **¿Por qué el cepstrum crudo no mejoró?** Porque el logaritmo pesa igual cada bin de ruido que cada armónico, y acá hay pocos armónicos claros.
- **¿Por qué no aparece nada en 60 ms?** Porque 10.4 impactos por vuelta no es entero: en una vuelta las dos periodicidades no se refuerzan. Se refuerzan a 2, 3 y 5 vueltas.
- **¿No están sobreajustando?** En parte sí, y lo decimos: el margen del lifter y las quefrencias largas se eligieron mirando estos datos. Por eso validamos dejando un canal afuera y por eso mantenemos la opción A.
- **¿Qué es el índice J?** Fisher: diferencia de medias al cuadrado sobre la suma de varianzas. Cuánto se separan las dos clases relativo a su dispersión.
- **¿Por qué Morlet?** Se parece a un impacto, su módulo da la envolvente en cada banda y su resolución se adapta a la frecuencia.
