from lxml import etree # For representing and manimpulating XML trees
from lxml.builder import E # For building XML trees
# from events import estimate, invoice # Sample REST API data


# The Document Class
class Document:
	xpath = './/body' # Location for appending document specific XML data
	channels = { "console": True, "local": True, "retool": True, "s3": False }

	# TODO: Implement handling of status codes
	def __init__(self, event):
		# self.status_code = event['statusCode'] # In case of non-200 result
		# self.json_body = event['body'] # The Retool specific data
		self.tree = Document.xml() # Populate the initial tree
		self.report = '' # string representation of the etree object
		self.response = { # Core of API response, will have properties appended
			'statusCode': 200,
			'headers': { 'Content-Type': 'text/html' },
		}

	# This is a utility method, only used to generate the specific document
	# subclass, determined by the value of the "document" property within the
	# API call.
	@classmethod
	def create(cls, event):
		return globals()[event['document'].capitalize()](event)

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

	def generate(self):
		self.compile() # Combine templates from parent and child classes
		self.populate() # Populate compiled template with received data
		self.render() # Render the etree object to a string
		self.deliver() # Deliver the output to the appropriate channel

	def compile(self):
		# Append this class' xml template to the XML tree represention to the end of
		# the specified XML xpath location.
		self.tree.find(self.xpath).append(self.xml())

	def populate(self):
		'' # Requires subclass override

	# Render the output through the enabled channels.
	def render(self):
		self.report = etree.tostring(
			self.tree,
			xml_declaration=True,
			pretty_print=True,
			encoding='utf-8',
			doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
		)

	def deliver(self):
		if Document.channels['console']:
			self.to_string()
		if Document.channels['local']:
			self.to_file()
		if Document.channels['retool']:
			self.to_retool()
		if Document.channels['s3']:
			self.to_s3()

	def to_string(self):
		print(self.report.decode())

	def to_file(self):
		with open(f"./html/{self.__class__.__name__.lower()}.html", 'wb') as f:
			f.write(self.report)

	def to_retool(self):
		self.response['body'] = self.report.decode()

	def to_s3(self):
		# TODO: Save to S3 bucket using Report ID as file name, return file URL.
		# self.report.decode() => S3 bucket
		url = 'https://amazon.s3/bucket/file.html'
		self.response['url'] = url


# The Invoice Class: A subclass of Document
class Invoice(Document):
	def __init__(self, event):
		super().__init__(event) # Call the parent class object initializer.
		self.generate() # Execute the document generation

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

	# This method uses the json body data to add data into the xml tree.
	def populate(self):
		'' # TODO: Implement Me!


# The Estimate Class: A subclass of Document
# This works the same as "Invoice" subclass above.
class Estimate(Document):
	def __init__(self, event):
		super().__init__(event)
		self.generate()

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

	def populate(self):
		'' # TODO: Implement Me!


# The AWS Trigger
# This method is required by AWS Lambda.
# The "event" is the data from the API call.
# The "context" is (roughly) the internal Lambda environment (not used).
def lambda_handler(event, context):
	return Document.create(event).response
	# return event

# Non-AWS Trigger
def generate():
	documents = [estimate, invoice] # Add others as available
	for d in documents: # Loop through document samples
		Document.create(d) # Generate a document per type

# This must be commented out while in use by AWS Lambda.
# generate()
