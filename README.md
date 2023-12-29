# Document Generator Script

Creates an HTML file (with CSS) to represent different kinds of documents
originating from Retool (such as "Invoice", "Estimate", or other as of yet
unspecifed reports.

The script can render it's output to:

- The python console
- A local file
- A REST API response
- An AWS S3 bucket file

The script uses a parent `Document` class which can be subclassed for
different kinds of report types (e.g.: "Estimate", "Invoice", etc)
Implementing a new report would just require creating a new Document subclass
and writing the appopriate document specific code (e.g.: the `xml()`, `css()`
and `populate()` methods.

## Environment

To use the lxml library on AWS Lambda, the library must be compiled on an
Amazon native operating system, then uploaded as a layer to the Lambda
function in question.

## Resources

- Source code: `https://github.com/pketienne/conflux-doc-generator`
