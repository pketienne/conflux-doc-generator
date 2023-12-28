from lxml import etree
from lxml.builder import E
from events import estimate, invoice


# Document
class Document:
	xpath = './/body'

	def __init__(self, event):
		self.status_code = event['statusCode']
		self.json_body = event['body']
		self.tree = Document.xml()

	@classmethod
	def create(cls, event):
		return globals()[event['body']['document'].capitalize()](event)

	@classmethod
	def xml(cls):
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
	
	def to_string(self):
		print(etree.tostring(self.tree))


# Invoice
class Invoice(Document):
	def __init__(self, event):
		super().__init__(event)
		self.tree.find(self.xpath).append(self.xml())
		self.to_string()

	@classmethod
	def xml(cls):
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

	@classmethod
	def css(cls):
		return ''


# Estimate
class Estimate(Document):
	def __init__(self, event):
		super().__init__(event)
		self.tree.find(self.xpath).append(self.xml())
		self.to_string()

	@classmethod
	def xml(cls):
		return (
			E.table(
				E.tr(
					E.th("column1"),
					E.th("column2"),
					E.th("column3"),
				),
			)
		)

	@classmethod
	def css(cls):
		return ''


# AWS Trigger
def lambda_handler(event, context):
	r = {
		'statusCode': 200,
		'doc': invoice,
		'headers': { 'Content-Type': 'text/html' },
	}
	return r

def non_lambda_handler(event):
	doc = Document.create(event)

non_lambda_handler(invoice)
