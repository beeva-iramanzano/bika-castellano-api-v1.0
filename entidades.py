#!flask/bin/python
import json
import ast
from flask import Flask, request, url_for, render_template, jsonify, Response
import re
import dateutil
import datetime
import calendar
from dateutil.parser import *
from datetime import *
import os
import subprocess


## Direcorio de instalación del API de python de freeling

app = Flask(__name__)


def extraer_telefonos(text):
  list_phones = []
  text = text.replace(' ', '')
  matchlist = re.findall(r'\d{9}', text)  #|[0-9]{3} [0-9]{3} [0-9]{3}|[0-9]{2} [0-9]{3} [0-9]{2} [0-9]{2}

  for match in matchlist:
    list_phones.append("{'telephone': '"+ str(match) +"'},")

  str_list_phones = ' '.join(list_phones)
  return str_list_phones 

def extraer_correos(text):
  list_emails=[]
  matchlist = re.findall(r"[0-9A-Za-z._-]+\@[0-9A-Za-z._-]+", text)

  for match in matchlist:
    list_emails.append("{'email': '"+match+"'},")

  str_list_emails = ' '.join(list_emails)
  return str_list_emails


def extraer_fechas(text):
  list_dates=[]

  matchlist = re.findall(r'\d{4}-\d{2}-\d{2}|\s\d{4}\s|\d{2}-\d{2}-\d{4}|\d{4}/\d{2}/\d{2}|\d{2}/\d{2}/\d{4}', text)
  months = "Enero" + "|" + "Febrero" + "|" + "Marzo" + "|" +"Abril" + "|" + "Mayo" + "|" + "Junio" + "|" + "Julio" + "|" + "Agosto" + "|" + "Septiempre" + "|" + "Octubre" + "|" + "Noviembre" + "|" + "Diciembre" + "|" + "Diciembre";
  monthsmatches = re.findall("{0}\s\d+\s\-\s{0}\s\d+".format(months), text)

  if monthsmatches: 
    for monthsmatch in monthsmatches:
      list_dates.append("{'month': '" + monthsmatch +"'},")
  
  days = "Lunes" + "|" + "Martes" + "|" + "Miercoles" + "|" + "Jueves"+ "|" + "Viernes" + "|" + "Sabado" + "|" + "Domingo" + "|" + "Domingo";
  daysmatches = re.findall("{0}\s".format(days), text)

  if daysmatches: 
    for daysmatch in daysmatches:
      list_dates.append("{'weekday': '" + daysmatch +"'},")

  for match in matchlist:
    
    if re.match(r'\d{4}-\d{2}-\d{2}', match):
      date = datetime.strptime(match, '%Y-%m-%d')
      list_dates.append("{'birthDate': '"+date.strftime("%d/%m/%y")+"'},")
    else: 
      if re.match(r'\s\d{4}\s', match):
        match = match.strip()
        date = datetime.strptime(match, '%Y')
        list_dates.append("{'year': '"+date.strftime("%Y")+"'},")
      else: 
        if re.match(r'\d{2}-\d{2}-\d{4}', match):
          date = datetime.strptime(match, '%d-%m-%Y')
          list_dates.append("{'birthDate': '"+date.strftime("%d/%m/%y")+"'},")
        else:
           if re.match(r'\d{4}/\d{2}/\d{2}', match):
             date = datetime.strptime(match, '%Y/%m/%d')
             list_dates.append("{'birthDate': '"+date.strftime("%d/%m/%y")+"'},")
           else:
              if re.match(r'\d{2}/\d{2}/\d{4}', match):
                 date = datetime.strptime(match, '%d/%m/%Y')
                 list_dates.append("{'birthDate': '"+date.strftime("%d/%m/%y")+"'},")

  str_list_dates = ''.join(list_dates)
  return str_list_dates


def extraer_entidades(lista_tags):
   ## output results
  entidades = []
  for s in lista_tags :
    ws = s.get_words();
    for w in ws :
      ##Miro cuales de la entidades me interesan
      tag= w.get_tag();
      if tag == 'NP00G00': 
        stringaux = "{'addressLocality':'" + w.get_form() +"'},"
        entidades.append(stringaux) 
      if tag == 'NP00O00':
        stringaux = "{'affiliation': '" + w.get_form() + "'},"
        entidades.append(stringaux) 
      if tag == 'NP00SP0':
        stringaux=str(w.get_form())
        stringaux=stringaux.replace( '_', ' ')
        stringaux = "{'name': '"+stringaux + "'},"
        entidades.append(stringaux) 

  return entidades

def extraer_entidades_aux(lista):
   ## output results
  entidades = []
  for s in lista :
    fin=s.find(' ')
    pal = s[:fin]
    if s.find('NP00G00')>0: 
      stringaux = "{'addressLocality':'" + pal +"'},"
      #print("S: " + pal)
      entidades.append(stringaux) 
    if s.find('NP00O00')>0: 
      stringaux = "{'affiliation': '" + pal + "'},"
      #print("S: " + pal)
      entidades.append(stringaux)
    if s.find('NP00SP0')>0: 
      stringaux = "{'name': '"+pal+"'},"
      #print("S: " + pal)
      entidades.append(stringaux) 

  return entidades

def api_entidades(text, flag_json):

  command= "echo \"" + text + "\" | analyzer_client localhost:50006 "
  respuesta = subprocess.check_output(command, shell=True)
  r= str(respuesta)
  respuesta=respuesta.decode("utf-8")
  pos = str(respuesta).split("\n")

  entidades= extraer_entidades_aux(pos)
  #entidades = extraer_entidades(ls)
  entitiesstring = "[" + ''.join(entidades) + "]"
  entitiesarrayjson = ast.literal_eval(entitiesstring)
  if flag_json:  #json
    resultado = jsonify({'entities_list': entitiesarrayjson})
    #print('Salgo de api_entidades 2 ' + resultado);
  else: #string
    resultado = json.dumps({'entities_list': entitiesarrayjson})
  
  #print('Ultimo' + resultado);
  return resultado

def api_fechas(text, flag_json):


  dates = extraer_fechas(text)
  datesstring = "[" + ''.join(dates) + "]"
  datesarrayjson = ast.literal_eval(datesstring) 
  if flag_json:  #json
    resultado = jsonify({'dates_list': datesarrayjson})
  else: #string
    resultado = json.dumps({'dates_list': datesarrayjson})
  
  return resultado

def api_correos(text, flag_json):
 
  emails = extraer_correos(text)
  emailsstring = "[" + ''.join(emails[:-1]) + "]"
  emailsarrayjson = ast.literal_eval(emailsstring)  

  if flag_json:  #json
    resultado = jsonify({'emails_list': emailsarrayjson})
  else: #string
    resultado = json.dumps({'emails_list': emailsarrayjson})
  
  return resultado

def api_telefonos(text, flag_json):
  
  phones = extraer_telefonos(text)
  phonesstring = "[" + ''.join(phones[:-1]) + "]"
  phonesarrayjson = ast.literal_eval(phonesstring)  

  if flag_json:  #json
    resultado = jsonify({'phones_list': phonesarrayjson})
  else: #string
    resultado = json.dumps({'phones_list': phonesarrayjson})
  
  return resultado

#flag_json = 1 (json) = 0 (string)
def mostrar_entidades(text, flag_json):

  command= "echo \"" + text + "\" | analyzer_client localhost:50005 "
  respuesta = subprocess.check_output(command, shell=True)
  r= str(respuesta)
  respuesta=respuesta.decode("utf-8")
  pos = str(respuesta).split("\n")

  entidades= extraer_entidades_aux(pos)

  entitiesstring = "[" + ''.join(entidades) + "]"
  entitiesarrayjson = ast.literal_eval(entitiesstring)
  dates = extraer_fechas(text)
  datesstring = "[" + ''.join(dates) + "]"
  datesarrayjson = ast.literal_eval(datesstring) 

  emails = extraer_correos(text)
  emailsstring = "[" + ''.join(emails) + "]"
  emailsarrayjson = ast.literal_eval(emailsstring)  
  
  telefonos = extraer_telefonos(text)
  phonesstring = "[" + ''.join(telefonos) + "]"
  phonesarrayjson = ast.literal_eval(phonesstring)  

  address = []
  addressstring = "[" + ''.join(address) + "]"
  addressarrayjson = ast.literal_eval(addressstring)
  
  if flag_json:  #json
    resultado = jsonify({'entities_list': entitiesarrayjson, 'dates_list': datesarrayjson, 'emails_list': emailsarrayjson, 'phones_list': phonesarrayjson, 'address_list': addressarrayjson})
  else: #string
    resultado = json.dumps({'entities_list': entitiesarrayjson, 'dates_list': datesarrayjson, 'emails_list': emailsarrayjson, 'phones_list': phonesarrayjson, 'address_list': addressarrayjson})
  
  return resultado


#---------------------- ROUTES --------------------------
@app.route('/')
def index():
  #return 'BIKA (BEEVA Information & Knowledge Assistant)'
  return render_template('bikacastellano.html')

@app.route('/bikaCastellano', methods=['GET', 'POST'])
def bika():
  #'POST' ya que viene de un formulario
  if request.method == 'POST':
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
      print("\n-------- request POST form['text'] -------")
      print(request.form['text'])
      text = str(request.form['text'])
      response = mostrar_entidades(text, 1) # devuelve json

      #### para evitar CORS ######
      response.headers.add_header('Access-Control-Allow-Origin', '*')
      response.headers['Content-Type'] = 'application/json'
      response.status_code = 200
      print("\n-------- JSON response -------")
      print(response)
      print("\n")

      return response
  #'GET' permite CORS usando JSONP
  if request.method == 'GET':
      print("\n-------- request GET request.args.get('....') -------")
      print("CALLBACK =" + request.args.get('callback'))
      print("TEXT =" + request.args.get('text'))
      idcallback = str(request.args.get('callback'))
      text = str(request.args.get('text'))
      json_string = mostrar_entidades(text, 0) #devuelve string

      respuesta = Response(idcallback + "("+ json_string + ");")
      print("\n-------- JSON response -------")
      print(respuesta)
      print("\n")
      
      return respuesta
  else:
    text = "My name is John Clark and I'm 28. I'm a lawyer. I was born the 1972-06-26 in  Madrid, Spain. I live in calle orujo, 4, 23700, Linares, Spain. In case emergency, Monday and Sunday, please contact with my wife Morgan Clark, she was born on 21/03/1975. You can contact me by e-mail at jdclark@email.com. My phone number is 213 555 776 and home phonenumber is 666777897 and 91 234 56 78. I work at BBVA, ERICSSON and GE."
   # error = 'use POST with a form(text)'
    info = show_the_entities(text)
    error = info.response
    print(info)
    print(info.response)
    return render_template('bika.html', information=error)


@app.route('/entidades', methods=['GET', 'POST'])
def obtener_entities():
  #print('hola');
  #'POST' ya que viene de un formulario
  if request.method == 'POST':
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
      print("\n-------- request POST form['text'] -------")
      print(request.form['text'])
      text = str(request.form['text'])

      response = api_entidades(text, 1) # devuelve json
      print('AQUI')
      #### para evitar CORS ######
      response.headers.add_header('Access-Control-Allow-Origin', '*')
      response.headers['Content-Type'] = 'application/json'
      response.status_code = 200
      print("\n-------- JSON response -------")
      print(response)
      print("\n")

      return response
  #'GET' permite CORS usando JSONP
  if request.method == 'GET':
      print("\n-------- request GET request.args.get('....') -------")
      print("CALLBACK =" + request.args.get('callback'))
      print("TEXT =" + request.args.get('text'))
      idcallback = str(request.args.get('callback'))
      text = str(request.args.get('text'))
      json_string = api_entidades(text, 0) #devuelve string

      respuesta = Response(idcallback + "("+ json_string + ");")
      print("\n-------- JSON response -------")
      print(respuesta)
      print("\n")
      
      return respuesta

@app.route('/fechas', methods=['GET', 'POST'])
def obtener_fechas():
  #'POST' ya que viene de un formulario
  if request.method == 'POST':
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
      print("\n-------- request POST form['text'] -------")
      print(request.form['text'])
      text = str(request.form['text'])
      response = api_fechas(text, 1) # devuelve json

      #### para evitar CORS ######
      response.headers.add_header('Access-Control-Allow-Origin', '*')
      response.headers['Content-Type'] = 'application/json'
      response.status_code = 200
      print("\n-------- JSON response -------")
      print(response)
      print("\n")

      return response
  #'GET' permite CORS usando JSONP
  if request.method == 'GET':
      print("\n-------- request GET request.args.get('....') -------")
      print("CALLBACK =" + request.args.get('callback'))
      print("TEXT =" + request.args.get('text'))
      idcallback = str(request.args.get('callback'))
      text = str(request.args.get('text'))
      json_string = api_fechas(text, 0) #devuelve string

      respuesta = Response(idcallback + "("+ json_string + ");")
      print("\n-------- JSON response -------")
      print(respuesta)
      print("\n")
      
      return respuesta

@app.route('/telefonos', methods=['GET', 'POST'])
def obtener_telefonos():
  #'POST' ya que viene de un formulario
  if request.method == 'POST':
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
      print("\n-------- request POST form['text'] -------")
      print(request.form['text'])
      text = str(request.form['text'])
      response = api_telefonos(text, 1) # devuelve json

      #### para evitar CORS ######
      response.headers.add_header('Access-Control-Allow-Origin', '*')
      response.headers['Content-Type'] = 'application/json'
      response.status_code = 200
      print("\n-------- JSON response -------")
      print(response)
      print("\n")

      return response
  #'GET' permite CORS usando JSONP
  if request.method == 'GET':
      print("\n-------- request GET request.args.get('....') -------")
      print("CALLBACK =" + request.args.get('callback'))
      print("TEXT =" + request.args.get('text'))
      idcallback = str(request.args.get('callback'))
      text = str(request.args.get('text'))
      json_string = api_telefonos(text, 0) #devuelve string

      respuesta = Response(idcallback + "("+ json_string + ");")
      print("\n-------- JSON response -------")
      print(respuesta)
      print("\n")
      
      return respuesta

@app.route('/correos', methods=['GET', 'POST'])
def obtener_correos():
  #'POST' ya que viene de un formulario
  if request.method == 'POST':
    if request.headers['Content-Type'] == 'application/x-www-form-urlencoded':
      print("\n-------- request POST form['text'] -------")
      print(request.form['text'])
      text = str(request.form['text'])
      response = api_correos(text, 1) # devuelve json

      #### para evitar CORS ######
      response.headers.add_header('Access-Control-Allow-Origin', '*')
      response.headers['Content-Type'] = 'application/json'
      response.status_code = 200
      print("\n-------- JSON response -------")
      print(response)
      print("\n")

      return response
  #'GET' permite CORS usando JSONP
  if request.method == 'GET':
      print("\n-------- request GET request.args.get('....') -------")
      print("CALLBACK =" + request.args.get('callback'))
      print("TEXT =" + request.args.get('text'))
      idcallback = str(request.args.get('callback'))
      text = str(request.args.get('text'))
      json_string = api_correos(text, 0) #devuelve string

      respuesta = Response(idcallback + "("+ json_string + ");")
      print("\n-------- JSON response -------")
      print(respuesta)
      print("\n")
      
      return respuesta      
 
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
