bika-castellano-api-v1.0
========================

Api que extrae información (personas, empresas, fechas,...) de un texto en castellano.
La api está compuesta por 5 webservices REST, a los que se puede invocar tanto con 'Get' como con 'Post'. La respuesta de estos servicios está en formato Json. 


SERVICIOS
---------

. Extracción de fechas: Webservices que a partir de un texto en lenguaje natural, extrae las fechas que contiene. Utiliza expresiones regulares. Extrae fechas del tipo:
1) Nombres de meses >> ‘month’
2) Nombres de días de la semana >> ‘weekday’
3) Fechas con el formato: YYYY-mm-dd , YYYY/mm/dd, dd-mm-YYYY  o  dd/mm/YYYY >> ‘birthDate’
4) años YYYY >> ‘year’
http://ip:5000/fechas


. Extracción de direcciones de correo: Webservices que a partir de un texto en lenguaje natural, extrae las direcciones de correo que contiene. Utiliza expresiones regulares.

http://ip:5000/correos


. Extracción de número de teléfono: Webservices que a partir de un texto en lenguaje natural, extrae los número de teléfono que contiene. Utiliza expresiones regulares. 

http://ip:5000/telefonos

. Extracción de entidades: Webservices que a partir de un texto en lenguaje natural, extrae las entidades que contiene. Utiliza Freeling NER (Named Entity Recognition) y NEC (Named Entity Clasification). Extrae:
1) Personas: Nombre + Apellido >> ‘name’
2) Localizaciones >> ‘addressLocality’
3) Organizaciones  >> ‘affiliation’

http://ip:5000/entidades


. Extracción completa: Webservices que a  partir de un texto en lenguaje natural,  extrae las entidades, fechas, direcciones de correo electrónico y números de teléfono que contiene.

http://ip:5000/bikaCastellano


PUESTA EN MARCHA
----------------
Para levantar el servicio es necesario:
- arrancar freeling: analyze -f es.cfg --outf tagged --server --port 50006-
- ejecutar el script 'entidades.py': python3 entidades.py
