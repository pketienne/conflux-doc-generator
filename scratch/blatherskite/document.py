from lxml import etree
from lxml.builder import E

class Document:
	def __init__(self):
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
