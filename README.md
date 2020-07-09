# inC
Implementación de la obra **In C**, de Terry Riley, con el entorno de programación FoxDot

Parseamos la información de la partitura de Riley escrita en notación ABC, con ayuda del paquete
[PyABC - Python package for parsing and analyzing ABC music notation] de Luke Campagnola, y la importamos
en nuestro programa principal, `inC.py`, con el cuál generamos, dados unos parámetros variables a placer del usuario,
una versión posible de la obra.

## Set-up
Una vez puesto en marcha el tándem [FoxDot/SuperCollider], colocar en el directorio de trabajo los siguiente ficheros:
+`pyabc.py` del paquete de Campagnola.
+`inC.abc` con la partitura original trascrita a notación ABC.
+`abcparser.py`
+`inC.py`

Abrir _SuperCollider_ y linkearlo con _FoxDot_ para escuchar sus mensajes con la orden `FoxDot.start`.

Abrir el archivo `inC.py` con _FoxDot_, y ejecutar los tres bloques de código:
+`_0_parámetros` donde se puede modificar algunos elementos de la versión de **In C** como la instrumentación o el _tempo_.
+`_1_constantes y funciones` para importar la información del parser.
+`_2_normas y PLAY` para que empiece a sonar nuestra versión personalizada con _FoxDot_ de **In C**.



[PyABC - Python package for parsing and analyzing ABC music notation]: https://github.com/campagnola/pyabc
[FoxDot/SuperCollider]: https://foxdot.org/installation/
