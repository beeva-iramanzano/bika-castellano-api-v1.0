Bika Castellano v1.0
========================

Api que extrae informacion (personas, empresas, fechas,...) de un texto en castellano.
La api está compuesta por 5 webservices REST, a los que se puede invocar tanto con 'Get' como con 'Post'. La respuesta de estos servicios está en formato Json. 


Servicios
---------

. Extracción de fechas:  webservice que extrae las fechas que contiene un texto en lenguaje natural. Utiliza expresiones regulares. Extrae fechas del tipo:
1) Nombres de meses >> ‘month’
2) Nombres de días de la semana >> ‘weekday’
3) Fechas con el formato: YYYY-mm-dd , YYYY/mm/dd, dd-mm-YYYY  o  dd/mm/YYYY >> ‘birthDate’
4) años YYYY >> ‘year’

http://ip:5000/fechas


. Extracción de direcciones de correo: webservice que extrae las direcciones de correo electrónico que contiene un texto en lenguaje natural.

http://ip:5000/correos


. Extracción de número de teléfono: webservice que extrae los número de teléfono que contiene un texto en lenguaje natural. Utiliza expresiones regulares.

http://ip:5000/telefonos

. Extracción de entidades: webservice que extrae las entidades que contiene un texto en lenguaje natural. Utiliza los módulos de freeling NER (Named Entity Recognition) y NEC (Named Entity Clasification). Extrae:
1) Personas: Nombre + Apellido >> ‘name’
2) Localizaciones >> ‘addressLocality’
3) Organizaciones  >> ‘affiliation’

http://ip:5000/entidades


. Extracción completa: webservice que extrae las entidades, fechas, direcciones de correo electrónico y números de teléfono que contiene un texto en lenguaje natural.

http://ip:5000/bikaCastellano


Puesta en marcha
----------------
Para levantar el servicio es necesario:
- tener instalada la version 3.0 de Puthon o superior
- tener instalada la versión 3.1 de freeling o superior
- arrancar freeling: analyze -f es.cfg --outf tagged --server --port 50006
- ejecutar el script 'entidades.py': python3 entidades.py
