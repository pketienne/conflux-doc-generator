from lxml import etree # For representing and manimpulating XML trees
from lxml.builder import E # For building XML trees
from events import estimate, invoice # Sample REST API data

#
# Document Generator Script
#

# Creates an HTML file (with CSS) to represent different kinds of documents
# originating from Retool (such as "Invoice", "Estimate", or other as of yet
# unspecifed reports.

# The script can output to:
# - The python console
# - A local file
# - A REST API response
# - An AWS S3 bucket file

# The script uses a parent `Document` class which can be subclassed for
# different kinds of report types (e.g.: "Estimate", "Invoice", etc)
# Implementing a new report would just require creating a new Document subclass
# and writing the appopriate document specific code (e.g.: the `xml()`, `css()``
# and `populate()` methods.


# The Document Class
class Document:
	xpath = './/body' # Location for appending document specific XML data

	# TODO: Implement handling of status codes
	def __init__(self, event):
		self.status_code = event['statusCode'] # In case of non-200 result
		self.json_body = event['body'] # The Retool specific data
		self.tree = Document.xml() # Populate the initial tree

	# This is a utility method, only used to generate the specific document
	# subclass, determined by the value of the "document" property within the
	# API call.
	@classmethod
	def create(cls, event):
		return globals()[event['body']['document'].capitalize()](event)

	# This is the core XML data, common to every document type.
	# TODO: Add CSS to the XML document's "style" property.
	@classmethod
	def xml(cls):
		return (
			E.html(
				E.head(
					E.title("McGraw D&B Invoice"),
					E.style(cls.css()), # Inserts CSS instructions
				),
				E.body(
					E.div(), # Use for the MDB Logo
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

	# These are the core CSS instructions, common to every document type.
	@classmethod
	def css(cls):
		return ''

	# A quick method for printing an Etree object to the console as a string.
	def to_string(self):
		print(etree.tostring(self.tree))


# The Invoice Class: A subclass of Document
class Invoice(Document):
	def __init__(self, event):
		super().__init__(event) # Call the parent class object initializer.

		# Append this class' xml template to the XML tree represention to the end of
		# the specified XML xpath location.
		self.tree.find(self.xpath).append(self.xml())

		# Evaluate the result via the console.
		self.to_string()

	# This is the document specific xml template.
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

	# These are the document specific CSS instructions.
	@classmethod
	def css(cls):
		return ''


# The Estimate Class: A subclass of Document
# This works the same as "Invoice" subclass above.
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


# The AWS Trigger
# This method is required by AWS Lambda.
# The "event" is the data from the API call.
# The "context" is (roughly) the internal Lambda environment (not used).
def lambda_handler(event, context):
	return {
		'statusCode': 200,
		# The line below creates a subclass of `Document` from the "document"
		# "property" of the API requests' JSON body.
		'doc': Document.create(event),
		'headers': { 'Content-Type': 'text/html' },
	}

# Non-AWS Trigger
# These must be commented out while in use by AWS Lambda.
# Document.create(estimate)
# Document.create(invoice)
