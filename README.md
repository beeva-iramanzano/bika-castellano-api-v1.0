Bika Castellano v1.0
========================

Api que extrae informacion (personas, empresas, fechas,...) de un texto en castellano.
La api está compuesta por 5 webservices REST, a los que se puede invocar tanto con 'Get' como con 'Post'. El texto en lenguaje natural, se pasa con el nombre 'text'. La respuesta de estos servicios está en formato Json. 


Puesta en marcha
----------------
Para levantar el servicio es necesario:
- tener instalada la version 3.0 de Puthon o superior
- tener instalada la versión 3.1 de freeling o superior
- arrancar freeling: analyze -f es.cfg --outf tagged --server --port 50006
- ejecutar el script 'entidades.py': python3 entidades.py


Servicios
---------

- Extracción de fechas

Webservice que extrae las fechas que contiene un texto en lenguaje natural. Utiliza expresiones regulares. Extrae fechas del tipo:

1) Nombres de meses >> ‘month’

2) Nombres de días de la semana >> ‘weekday’

3) Fechas con el formato: YYYY-mm-dd , YYYY/mm/dd, dd-mm-YYYY  o  dd/mm/YYYY >> ‘birthDate’

4) Años YYYY >> ‘year’
   
 
      URL: http://ip:5000/fechas, Methods: GET, POST

      RESPUESTA: "dates_list": [{ "weekday": "Lunes"}, {"weekday": "Domingo" }, {"birthDate": "26/06/72"}, {"birthDate": "21/03/75"}]



- Extracción de direcciones de correo

Webservice que extrae las direcciones de correo electrónico que contiene un texto en lenguaje natural. Utiliza expresiones regulares.

      URL: http://ip:5000/correos

      RESPUESTA: "emails_list": [{"email": "jdclark@email.com."}]



- Extracción de número de teléfono

Webservice que extrae los número de teléfono que contiene un texto en lenguaje natural. Utiliza expresiones regulares.

      URL: http://ip:5000/telefonos

      RESPUESTA: "phones_list": [{"telephone": "213555776"}, { "telephone": "666777897" }, { "telephone": "912345678"}]
   


- Extracción de entidades

Webservice que extrae las entidades que contiene un texto en lenguaje natural.Utiliza los módulos de Freeling NER (Named Entity Recognition) y NEC (Named Entity Clasification). Extrae:

1) Personas: Nombre + Apellido >> ‘name’

2) Localizaciones >> ‘addressLocality’
  
3) Organizaciones  >> ‘affiliation’


      URL: http://ip:5000/entidades, Methods: GET, POST
      RESPUESTA: 

   "entities_list": [{
       "name": "John Clark"
   }, {
       "addressLocality": "Madrid"
   }, {
       "addressLocality": "España"
   }, {
       "addressLocality": "Linares"
   }, {
       "addressLocality": "España"
   }, {
       "name": "Morgan Clark"
   }, {
       "affiliation": "BBVA"
   }, {
       "affiliation": "ERICSSON"
   }, {
       "affiliation": "GE"
   }]



- Extracción completa

Webservice que extrae las entidades, fechas, direcciones de correo electrónico y números de teléfono que contiene un texto en lenguaje natura.

      URL: http://ip:5000/bikaCastellano
      RESPUESTA: {"phones_list": [{"telephone": "213555776"}, {"telephone": "666555888"}, {"telephone": "915552222"}], "emails_list": [{"email":"jdclark@email.com."}], "entities_list": [{"name": "John_Clark"},  {"addressLocality": "Madrid"}, {"addressLocality": "España"}, {"addressLocality": "Linares"}, {"addressLocality": "España"}, {"name": "Morgan_Clark"}, {"affiliation": "BBVA"}, {"affiliation": "Ericson"}, {"affiliation": "GE"}], "dates_list": [{"weekday": "Lunes"}, {"weekday": "Domingo"}, {"birthDate": "26/06/72"}, {"birthDate": "21/03/75"}]}


