from lxml import etree # For representing and manimpulating XML trees
from lxml.builder import E # For building XML trees
from scratch.events import estimate, invoice # Sample REST API data


# The Document Class
class Document:
	xpath = './/body' # Location for appending document specific XML data
	channels = { "console": True, "local": True, "retool": True, "s3": False }

	# TODO: Implement handling of status codes
	def __init__(self, event):
		self.tree = Document.xml() # Populate the initial tree
		self.report = '' # string representation of the etree object
		self.response = { # Core of API response, will have properties appended
			'statusCode': 200,
			'headers': { 'Content-Type': 'text/html' },
		}
		print('ZOMFG')
		self.populate()

	def populate(self):
		print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHH")

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
					E.div("", {"id": "logo"}), # Use for the MDB Logo
					E.h1("Project Details"),
					E.h2("Contractor"),
					E.ul(
						{"id":"contractor"},
						E.li(
							E.span("Name:", {"class": "key"}),
							E.span("McGraw Design & Build", {"class": "value"}),
						),
						E.li(
							E.span("Address:", {"class": "key"}),
							E.span("448 W 31st St Indianapolis, IN 46208", {"class": "value"}),
						),
						E.li(
							E.span("Email:", {"class": "key"}),
							E.span("oliver@mcgrawdesignbuild.com", {"class": "value"}),
						),
						E.li(
							E.span("Phone:", {"class": "key"}),
							E.span("(317) 782-5271", {"class": "value"}),
						),
						E.li(
							E.span("Website:", {"class": "key"}),
							E.span("https://mcgrawdesignbuild.com/", {"class": "value"}),
						),
					),
					E.h2("Client"),
					E.ul(
						{"id":"client"},
						E.li(
							E.span("Name:", {"class": "key"}),
							E.span("", {"class": "value", "id": "client_name"}),
						),
						E.li(
							E.span("Address:", {"class": "key"}),
							E.span("", {"class": "value", "id": "client_address"}),
						),
						E.li(
							E.span("Email:", {"class": "key"}),
							E.span("", {"class": "value", "id": "client_email"}),
						),
						E.li(
							E.span("Phone:", {"class": "key"}),
							E.span("", {"class": "value", "id": "client_phone"}),
						),
					),
				)
			)
		)

	# These are the core CSS instructions, common to every document type.
	@classmethod
	def css(cls):
		return '''
			body { margin: 20px 50px; }
			#logo {
				width: 500px;
				height: 125px;
				background-image: url('../../../Shared/mdb-logo.png');
				margin: auto;
			}
			h1 {
				background-color: #abc;
				padding: 5px 15px;
				border: 1px solid #999;
			}
			h2 {
				margin-left: 35px;
			}
			table {
				margin: auto;
				width: 100%;
				text-align: left;
			}
			table#materials th { background-color: #66d9ff; }
			table#labors th { background-color: #33aacc; }
			table#totals th { background-color: #3388cc; }
			td, th {
				border: 1px solid #000;
				padding: 5px;
			}
			th.quantity { width: 100px; }
			th.cost { width: 100px; }
			th.total { width: 100px; }
			td.grand-total { background-color: #e0e0e0 }
			ul { list-style-type: none; }
			span.key { font-weight: bold; }
		'''

	def generate(self):
		self.compile() # Combine templates from parent and child classes
		self.populate() # Populate compiled template with received data
		self.render() # Render the etree object to a string
		self.deliver() # Deliver the output to the appropriate channel

	def compile(self):
		# Append this class' xml template to the XML tree represention to the end of
		# the specified XML xpath location.
		# self.tree.find(self.xpath).append(self.xml())
		self.tree.find(self.xpath).append(self.xml())
		''

	# def populate(self):
	# 	# attributes = [ 'name', 'address', 'email', 'phone', 'website' ]
	# 	# for a in attributes:

	# 	# self.tree.find('.//body').append(E.div('footherskite'))
	# 	self.tree.find(self.xpath).append(self.xml())
	# 	print('ZZZZZZZZZZZZZZZZZZOOOOOOOOOOMMMMMMMMMMMMMMMMMGGGGGGGGGGGGGGG')
	# 	''
		
	def populate(self):
		print('fffffffffffffffffooooooooooooooo')


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
			E.div(
				E.h2("Invoice"),
				E.ul(
					{"id":"client"},
					E.li(
						E.span("Invoice #:", {"class": "key"}),
						E.span("", {"class": "value"}),
					),
					E.li(
						E.span("Invoice Date:", {"class": "key"}),
						E.span("", {"class": "value"}),
					),
					E.li(
						E.span("Invoice Notes:", {"class": "key"}),
						E.span("", {"class": "value"}),
					),
				),
				E.h1("Costs"),
				E.h2("Materials"),
				E.table(
					{"id": "materials"},
					E.thead(
						E.tr(
							E.th("Description", {"class": "description"}),
							E.th("Quantity", {"class": "quantity"}),
							E.th("Cost", {"class": "cost"}),
							E.th("Total", {"class": "total"}),
						),
					),
					E.tbody(),
				),
				E.h2("Labor"),
				E.table(
					{"id": "labors"},
					E.thead(
						E.tr(
							E.th("Description", {"class": "description"}),
							E.th("Quantity", {"class": "quantity"}),
							E.th("Cost", {"class": "cost"}),
							E.th("Total", {"class": "total"}),
						),
					),
					E.tbody(),
				),
				E.h2("Totals"),
				E.table(
					{"id": "totals"},
					E.thead(
						E.tr(
							E.th("Cost Type", {"class": "category"}),
							E.th("Total", {"class": "total"}),
						),
					),
					E.tbody(
						E.tr(
							E.td("Materials"),
							E.td({"id": "total-materials"}),
						),
						E.tr(
							E.td("Labor"),
							E.td({"id": "total-labors"}),
						),
						E.tr(
							E.td("Grand Total", {"class": "grand-total"}),
							E.td({"id": "grand-total", "class": "grand-total"}),
						),
					),
				),
			)
		)

	# These are the document specific CSS instructions.
	@classmethod
	def css(cls):
		return ''

	# This method uses the json body data to add data into the xml tree.
	def populate(self):
		''


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
		'' #TODO: Implement Me!


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
generate()

