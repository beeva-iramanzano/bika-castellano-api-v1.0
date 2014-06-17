Bika Castellano v1.0
========================

Api que extrae informacion (personas, empresas, fechas,...) de un texto en castellano.
La api está compuesta por 5 webservices REST, a los que se puede invocar tanto con 'Get' como con 'Post'. La respuesta de estos servicios está en formato Json. 


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
4) años YYYY >> ‘year’

URL: http://ip:5000/fechas
Methods: GET, POST
Response: JSON array

 "dates_list": [{
       "weekday": "Lunes"
   	   }, {
       "weekday": "Domingo"
   }, {
       "birthDate": "26/06/72"
   }, {
       "birthDate": "21/03/75"
   }]

- Extracción de direcciones de correo

Webservice que extrae las direcciones de correo electrónico que contiene un texto en lenguaje natural. Utiliza expresiones regulares.

URL: http://ip:5000/correos
Methods: GET, POST
Response: JSON array

 "emails_list": [{
       "email": "jdclark@email.com."
   }]

- Extracción de número de teléfono
Webservice que extrae los número de teléfono que contiene un texto en lenguaje natural. Utiliza expresiones regulares.

URL: http://ip:5000/telefonos
Methods: GET, POST
Response: JSON array

"phones_list": [{
       "telephone": "213555776"
   }, {
       "telephone": "666777897"
   }, {
       "telephone": "912345678"
   }]

- Extracción de entidades
Webservice que extrae las entidades que contiene un texto en lenguaje natural.Utiliza los módulos de Freeling NER (Named Entity Recognition) y NEC (Named Entity Clasification). Extrae:
1) Personas: Nombre + Apellido >> ‘name’
2) Localizaciones >> ‘addressLocality’
3) Organizaciones  >> ‘affiliation’


URL: http://ip:5000/entidades
Methods: GET, POST
Response: JSON array

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
Methods: POST, GET

POST
Request
Headers


Body


Request Url: http://ip:5000/bikaCastellano
Request Method: POST
Status Code: 200
Params: {
   "callback": "jQuery11654254656562545656",
   "text": "\"Mi nombre es John Clark y tengo 28 años. Soy abogado. Naci el 26/06/1972 en Madrid, España. Vivo en la calle Orujo,4, 23700, Linares, España. En caso de emergencia, Lunes o Domingo, por favor contacta con mi mujer Morgan Clark, ella nacio el 21/03/1975. Puedes contactar conmigo por email en jdclark@email.com. Mi número de teléfono es el 213 555 776 y el número de casa es el 666555888 y 91 555 22 22. Trabajo en BBVA, Ericson y GE.\""
}

Response
Headers
Status Code: 200
Access-Control-Allow-Origin: *
Date: Mon, 16 Dec 2013 16:17:43 GMT
Server: Werkzeug/0.9.4 Python/3.3.3
Content-Length: 822
Content-Type: application/json
Body
{
   "address_list": [],
   "dates_list": [{
       "weekday": "Lunes"
    }, {
       "weekday": "Domingo"
    }, {
       "birthDate": "26/06/72"
   }, {
       "birthDate": "21/03/75"
   }],
   "emails_list": [{
       "email": "jdclark@email.com."
   }],
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
   }],
   "phones_list": [{
       "telephone": "213555776"
   }, {
       "telephone": "666777897"
   }, {
       "telephone": "912345678"
   }]
}

GET
Request
Headers

Body


Request Url: http://ip:5000/bikaCastellano
Request Method: GET
Status Code: 200
Params: {
   "callback": "jQuery11654254656562545656",
   "text": "\"Mi nombre es John Clark y tengo 28 años. Soy abogado. Naci el 26/06/1972 en Madrid, España. Vivo en la calle Orujo,4, 23700, Linares, España. En caso de emergencia, Lunes o Domingo, por favor contacta con mi mujer Morgan Clark, ella nacio el 21/03/1975. Puedes contactar conmigo por email en jdclark@email.com. Mi número de teléfono es el 213 555 776 y el número de casa es el 666555888 y 91 555 22 22. Trabajo en BBVA, Ericson y GE..\""
}

Response
Headers
Status Code: 200
Date: Mon, 16 Dec 2013 16:09:02 GMT
Server: Werkzeug/0.9.4 Python/3.3.3
Content-Length: 551
Content-Type: text/html; charset=utf-8
Body
jQuery11654254656562545656({"entities_list": [{"name": "John Clark"}, {"addressLocality": "Madrid"}, {"addressLocality": "España"}, {"addressLocality": "Linares"}, {"addressLocality": "España"}, {"name": "Morgan Clark"}, {"affiliation": "BBVA"}, {"affiliation": "ERICSSON"}, {"affiliation": "GE"}], "address_list": [], "dates_list": [{"weekday": "Lunes"}, {"weekday": "Domingo"}, {"birthDate": "26/06/72"}, {"birthDate": "21/03/75"}], "phones_list": [{"telephone": "213555776"}, {"telephone": "666777897"}, {"telephone": "912345678"}], "emails_list": [{"email": "jdclark@email.com."}]});

