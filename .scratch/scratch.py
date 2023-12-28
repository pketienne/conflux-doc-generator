from lxml import etree
from lxml.builder import E

xmlns='http://www.w3.org/1999/xhtml'

def klass(*args):
	return {"class":' '.join(args)}

def html():


	E.html(
		E.head(
			E.title("McGraw D&B Invoice"),
			E.style(style()),
		),
		E.body(
			E.div('MDB Logo'),
			E.div('PROJECT_NAME'),
			E.div('Invoice #00512'),
			E.div('Created: January 1st, 2024'),
			E.div('Due: February 1st, 2024'),
			E.div('McGraw Design & Build'),
			E.div('service@mcgrawdesignbuild.com'),
			E.div('www.mcgrawdesignbuild.com'),
			E.div('448 W 31st Street'),
			E.div('Indianapolis, IN 46208'),
			E.div('(317) 782-5271'),
			E.div('CLIENT_NAME'),
			E.div('CLIENT_EMAIL'),
			E.div('CLIENT_CONTACT'),
			E.div('CLIENT_ADDRESS'),
			E.div('McGraw Design & Build'),
			E.table(
				E.tr(
					E.th('Material Expenses'),
					E.th('Quantity'),
					E.th('Cost'),
					E.th('Total'),
				),
				E.tr(
					E.td('Framing Lumber'),
					E.td(''),
					E.td(''),
					E.td('$1,682.30'),
				),
				E.tr(
					E.th('Labor Costs'),
					E.th('Quantity'),
					E.th('Cost'),
					E.th('Total'),
				),
				E.tr(
					E.td('Delivered lumber package'),
					E.td('4.5'),
					E.td('35.796'),
					E.td('161.082'),
				),
			),
		)
	)
)

with open('./estimate.html', 'wb') as f:
    f.write(etree.tostring(
         html, xml_declaration=True, pretty_print=True, encoding='utf-8', doctype='<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'))

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': html,
        'headers': {
          'Content-Type': 'text/html',
        }
    }

# lxml library examples
'''
			E.h1("Hello!", klass("title")),
html = etree.Element(etree.QName(xmlns, 'html'), )
html.append(etree.Element('head'))
html.append(etree.Element('body'))
head = head.append(etree.Element('title'))
body.append(etree.Element('ol'))
'''

def style():
     return '''
			.invoice-box {
				max-width: 800px;
				margin: auto;
				padding: 30px;
				border: 1px solid #eee;
				box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
				font-size: 16px;
				line-height: 24px;
				font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
				color: #555;
			}
			.invoice-box table {
				width: 100%;
				line-height: inherit;
				text-align: left;
			}
			.invoice-box table td {
				padding: 5px;
				vertical-align: top;
			}
			.invoice-box table tr td:nth-child(2) {
				text-align: right;
			}
			.invoice-box table tr.top table td {
				padding-bottom: 20px;
			}
			.invoice-box table tr.top table td.title {
				font-size: 45px;
				line-height: 45px;
				color: #333;
			}
			.invoice-box table tr.information table td {
				padding-bottom: 40px;
			}
			.invoice-box table tr.heading td {
				background: #eee;
				border-bottom: 1px solid #ddd;
				font-weight: bold;
			}
			.invoice-box table tr.details td {
				padding-bottom: 20px;
			}
			.invoice-box table tr.item td {
				border-bottom: 1px solid #eee;
			}
			.invoice-box table tr.item.last td {
				border-bottom: none;
			}
			.invoice-box table tr.total td:nth-child(2) {
				border-top: 2px solid #eee;
				font-weight: bold;
			}
			@media only screen and (max-width: 600px) {
				.invoice-box table tr.top table td {
					width: 100%;
					display: block;
					text-align: center;
				}
				.invoice-box table tr.information table td {
					width: 100%;
					display: block;
					text-align: center;
				}
			}
			/** RTL **/
			.invoice-box.rtl {
				direction: rtl;
				font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
			}
			.invoice-box.rtl table {
				text-align: right;
			}
			.invoice-box.rtl table tr td:nth-child(2) {
				text-align: left;
			}
		'''

