# -*- coding:utf-8 -*-

from core.plugins_manager import PluginsManager 

import textwrap
import smtplib
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
import time
from datetime import datetime
import getpass

class MailNotificator:

	def __init__(self, conf):
		self._smpt = conf.get('smtp')
		self._smtp_port = conf.get('smtp_port')
		self._sender = conf.get('sender')
		self._receiver = conf.get('receiver')
		print("Introduzca la contraseña del sender: " + self._sender)
		self._sender_password = getpass.getpass()
		self._dhost = conf.get('dhost', '')
		self._content_type = conf.get('content_type', '')
		self._path = conf.get('path', '')
		self._content_length = conf.get('content_length',None)
		# Nos conectamos al servidor SMTP	
		self._serverSMTP = smtplib.SMTP(self._smpt,self._smtp_port)
		self._serverSMTP.ehlo()
		self._serverSMTP.starttls()
		self._serverSMTP.ehlo()
		self._serverSMTP.login(self._sender,self._sender_password)

	def __del__(self):
		if self._serverSMTP:
			self._serverSMTP.close()
	
	def log_stream(self, http_stream):
		if (self._dhost_condition(http_stream) and
		    self._content_type_condition(http_stream) and
		    self._path_condition(http_stream) and
		    self._content_length_condition(http_stream) ):
			self._send_mail(http_stream)
	
	def _dhost_condition(self, http_stream):
		if self._dhost is None:
			res = True
		else:
			res = self._dhost in http_stream.get_dhost()
		return res
	
	def _content_type_condition(self, http_stream):
		if self._content_type is None:
			res = True
		else:
			res = self._content_type in str(http_stream.get_response_header('Content-Type'))
		return res
	
	def _path_condition(self, http_stream):
		if self._path is None:
			res = True
		else:
			res = self._path in http_stream.get_path()
		return res
	
	def _content_length_condition(self, http_stream):
		if self._content_length is None:
			res = True
		else:
			res = (int(http_stream.get_response_header('Content-Length')) >= self._content_length)
		return res
	
	def _send_mail(self, http_stream):
		# Configuracion del mensaje y lo enviamos
		msg =  MIMEMultipart()
		msg['From']=self._sender
		msg['To']=self._receiver
		msg['Subject']="Conexión crítica advertida"
		msg.attach(MIMEText("Se ha detectado una comunicación crítica.\n"))
		msg.attach(MIMEText("A continuación se lista la información del acceso:\n"))
		msg.attach(MIMEText('url: ' + http_stream.get_url()))
		msg.attach(MIMEText('path: ' + http_stream.get_path()))
		msg.attach(MIMEText('method: ' + http_stream.get_method()))
		msg.attach(MIMEText('dhost: ' + http_stream.get_dhost()))
		msg.attach(MIMEText('dport: ' + str(http_stream.get_dport())))
		msg.attach(MIMEText('shost: ' + http_stream.get_shost()))
		msg.attach(MIMEText('sport: ' + str(http_stream.get_sport())))
		msg.attach(MIMEText('http_version: ' +  ".".join(map(str, http_stream.get_http_version()))))
		msg.attach(MIMEText('status_code: ' + str(http_stream.get_status_code())))
		msg.attach(MIMEText('ctime: ' + datetime.now().ctime()))
		msg.attach(MIMEText('content_type: ' + str(http_stream.get_response_header('Content-Type'))))
		msg.attach(MIMEText('content_length: ' + str(http_stream.get_response_header('Content-Length'))))
		msg.attach(MIMEText("\n"))
		self._serverSMTP.sendmail(self._sender,self._receiver,msg.as_string())
	
	@classmethod
	def help(cls):
		return textwrap.dedent('''\
		MailNotificator: manda un mail por cada conexión que cumple con los criterios pasados por parámetro
		Params:
			- smtp				dirección del servidor smtp
			- smtp_port			puerto de conexión del servidor smtp
			- sender			dirección de mail desde la cual se envía el email
			- senderPassword	contraseña del sender del mail
			- receiver			dirección de mail al cual se enviará el email
			- host				parte del host al que se intento realizar la conexión (default: '')
			- content_type		contenido descargado (default: '')
			- path				parte del path al que se intentó acceder (default: '')
			- content_length	tamaño mínimo del contenido al que se intentó acceder (default: None)
		Data sended in the mail:
			- url				request url (TEXT)
			- path              request path (TEXT)
			- method            request method (TEXT)
			- dhost             destination host (TEXT)
			- dport             destination port (TEXT)
			- shost             source host (TEXT)
			- sport             source port (TEXT)
			- http_version		http_version (TEXT)
			- status_code       response status code (INTEGER)
			- ctime             date of the request (DATE)
			- content_type      response content type (TEXT)
			- content_length    response length (INTEGER)
		''')

PluginsManager.register(MailNotificator, 'MailNotificator');
