from flask import Flask, render_template_string
from lxml import etree

app = Flask(__name__)

# Route to serve the XML data as a web page
@app.route('/')
def home():
    # Load XML data
    xml_file = 'dist/gui/data.xml'
    xslt_file = 'dist/gui/style.xsl'
    
    # Parse XML and XSLT files
    xml_tree = etree.parse(xml_file)
    xslt_tree = etree.parse(xslt_file)
    
    # Perform the transformation
    transform = etree.XSLT(xslt_tree)
    result_tree = transform(xml_tree)
    
    # Return the transformed HTML as a response
    return render_template_string(str(result_tree))

if __name__ == '__main__':
    app.run(debug=True)
