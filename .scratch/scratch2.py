from lxml import etree
from lxml.builder import E
from events import invoice, estimate

# Document
class Document:

	@classmethod
	def create(cls, event):
		body = event['body']
		type = body['document'].capitalize()
		body.pop('document', None)
		klass = globals()[type]
		return klass(body)


	@property
	def template_html(self):
		return (
			E.html(
				E.head(
					E.title("McGraw D&B Invoice"),
					# E.style(self.style()),
				),
				E.body(
					E.div(), # MDB Logo
					E.table(
						E.tr(
							E.td('Contrator:'),
							E.td('McGraw Design & Build'),
							E.td('Invoice #:'),
							E.td('INVOICE-#'),
							E.td('Client:'),
							E.td('CLIENT-NAME'),
						),
						E.tr(
							E.td('Address:'),
							E.td('CONTRACTOR-ADDRESS'),
							E.td('Invoice Date:'),
							E.td('INVOICE-DATE'),
							E.td('Address:'),
							E.td('CLIENT-ADDRESS'),
						),
						E.tr(
							E.td('Email:'),
							E.td('CONTRACTOR-EMAIL'),
							E.td('Invoice Subject'),
							E.td('INVOICE-SUBJECT'),
							E.td('Email:'),
							E.td('CLIENT-EMAIL'),
						),
						E.tr(
							E.td('Phone:'),
							E.td('CONTRACTOR-PHONE'),
							E.td(),
							E.td(),
							E.td('Phone:'),
							E.td('CLIENT-PHONE'),
						),
					)
				)
			)
		)

	@property
	def template_style(self):
		style = ''''''

	def combine(self, template1, template2):
		return template1.find('.//body').append(template2)

	def to_file(self, html):
		with open(f"./{self.__class__.__name__.lower()}.html",'wb') as f:
			f.write(etree.tostring(
				self.html(self.template), xml_declaration=True, pretty_print=True,
				encoding='utf-8', doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
			))
		f.close()

	def to_string(self):
		etree.tostring(self)

# Invoice
class Invoice(Document):
	def __init__(self, body):
		super().__init__(body)

	@property	
	def template_html(self):
			return (
				E.table(
					E.tr(
						E.th('Materials'),
					),
					E.tr(
						E.th('Description'),
						E.th('Quantity'),
						E.th('Cost'),
						E.th('Total'),
					),
					E.tr('na', id='materials'),
					E.tr(
						E.th('Labor'),
					),
					E.tr(
						E.th('Description'),
						E.th('Quantity'),
						E.th('Cost'),
						E.th('Total'),
					),
					E.tr('na', id='labor'),
				)
			)

	@property
	def template_style(self):
		style = ''''''

# Estimate
class Estimate(Document):
	def __init__(self, body):
		super().__init__(body)

	@property
	def template(self):
		return (
			E.table(
				E.tr(
					E.th("column1"),
					E.th("column2"),
					E.th("column3"),
				),
			),
		)

# AWS Trigger
def lambda_handler(event, context):
	url = 'https://mdb-conflux.s3.us-east-2.amazonaws.com/sample.html'
	doc = Document.create(event)
	r = {
		'statusCode': 200,
		'doc': doc.to_string(),
		'headers': { 'Content-Type': 'text/html' },
	}
	return r

# AWS Trigger - old
def lambda_handler_old(event, context):
	document_type = event['body']['document'].capitalize()
	document_class = globals()[document_type]
	event['body'].pop('document', None)
	document_instance = document_class(event['body'])
	document_instance.to_file()
	body = etree.tostring(document_instance.html())
	r = {
		'statusCode': 200,
		'body': body,
		'headers': { 'Content-Type': 'text/html' },
	}
	return r

# lambda_handler(event, None)

b = ''

