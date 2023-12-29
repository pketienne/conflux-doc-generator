# Document Generator Script

This script's purpose is to generate reports from data originating in Retool.

The data source can be either REST API POST requests from a Retool application or local sample data simulating a REST API POST request.

The output of the script is a single XHTML file with accompanying CSS for style.

The output can be delivered via one of the following channels:

- Displayed in the local python console.
- Written as a file to the local filesystem.
- Delivered back to Retool within the API response.
- Saved as a remote file within an AWS S3 bucket.

Each mode of delivery can be independently enabled or disabled as desired.

## Production

The production workflow behaves as follows:

- A Retool application button click triggers a REST API POST query.
- The POST query hits an AWS API Gateway.
- The API Gateway triggers an AWS Lambda function.
- The Lambda function then:
	- Detects the document type (e.g.: "estimate", "invoice").
	- Combines default and document type specific templates.
	- Populates templates with delivered data.
	- Generate a single XHTML+CSS document.
	- Saves the document to an S3 bucket.
	- Delivers a API response to the Retool application.

## Environment

The script utilizes a python library called `lxml`. This library must be compiled on an operating system compatible with the containers used by the Amazon Lambda service

To use the lxml library on AWS Lambda, the library must be compiled on an
Amazon native operating system, then uploaded as a layer to the Lambda
function in question.

## Resources

- Source code: `https://github.com/pketienne/conflux-doc-generator`
