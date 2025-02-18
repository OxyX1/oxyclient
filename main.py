from flask import Flask, request, Response, send_from_directory
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, quote

app = Flask(__name__, static_folder='dist')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')
    return send_from_directory(app.static_folder, 'style.css')

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return "Missing 'url' parameter", 400

    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) '
                       'Chrome/115.0.0.0 Safari/537.36'),
        'Referer': target_url
    }

    try:
        remote_response = requests.get(target_url, headers=headers)
    except Exception as e:
        return f"Error fetching {target_url}: {e}", 500

    content_type = remote_response.headers.get('Content-Type', '')

    if 'text/html' in content_type:
        soup = BeautifulSoup(remote_response.text, 'html.parser')

        # Rewrite all anchor tags to point back to your proxy
        for tag in soup.find_all('a', href=True):
            new_href = urljoin(target_url, tag['href'])
            tag['href'] = f"/proxy?url={quote(new_href, safe='')}"

        # Rewrite all form actions to point back to your proxy
        for form in soup.find_all('form', action=True):
            form['action'] = f"/proxy?url={quote(urljoin(target_url, form['action']), safe='')}"

        modified_html = str(soup)
        return Response(modified_html, headers={'Content-Type': content_type})
    
    return Response(remote_response.content, headers={'Content-Type': content_type})

if __name__ == '__main__':
    app.run(debug=True)
