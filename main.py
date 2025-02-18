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

        # Rewrite all anchor tags to point back to the proxy
        for tag in soup.find_all('a', href=True):
            new_href = urljoin(target_url, tag['href'])
            tag['href'] = f"/proxy?url={quote(new_href, safe='')}"

        # Rewrite all form actions to point back to the proxy
        for form in soup.find_all('form', action=True):
            form['action'] = f"/proxy?url={quote(urljoin(target_url, form['action']), safe='')}"

        # Inject JavaScript for better navigation interception
        script = f"""
        <script>
        (function() {{
            function rewriteLink(url) {{
                return "/proxy?url=" + encodeURIComponent(url);
            }}

            function fixLinks() {{
                document.querySelectorAll("a").forEach(el => {{
                    if (el.href.startsWith("http")) {{
                        el.href = rewriteLink(el.href);
                    }}
                }});
            }}

            document.addEventListener("click", function(event) {{
                let el = event.target.closest("a");
                if (el && el.href.startsWith("http")) {{
                    event.preventDefault();
                    window.open(rewriteLink(el.href), "_blank"); // Open in new tab inside proxy
                }}
            }});

            // Override JavaScript-based navigation (pushState, replaceState)
            const originalPushState = history.pushState;
            const originalReplaceState = history.replaceState;

            function interceptNavigation(method, ...args) {{
                if (typeof args[2] === "string" && args[2].startsWith("http")) {{
                    args[2] = rewriteLink(args[2]);
                }}
                return method.apply(history, args);
            }}

            history.pushState = function(...args) {{ return interceptNavigation(originalPushState, ...args); }};
            history.replaceState = function(...args) {{ return interceptNavigation(originalReplaceState, ...args); }};

            // Override window.location.href
            Object.defineProperty(window.location, "href", {{
                set: function(url) {{
                    window.location.assign(rewriteLink(url));
                }}
            }});

            // Block direct `window.open()` calls and redirect them through proxy
            const originalWindowOpen = window.open;
            window.open = function(url, target, features) {{
                if (url.startsWith("http")) {{
                    return originalWindowOpen.call(window, rewriteLink(url), target || "_blank", features);
                }}
                return originalWindowOpen.call(window, url, target, features);
            }};

            // Intercept fetch requests to ensure they go through proxy
            const originalFetch = window.fetch;
            window.fetch = function(resource, init) {{
                if (typeof resource === "string" && resource.startsWith("http")) {{
                    resource = rewriteLink(resource);
                }}
                return originalFetch.call(this, resource, init);
            }};

            // Intercept XMLHttpRequest to ensure proxy usage
            const originalXHR = window.XMLHttpRequest;
            window.XMLHttpRequest = function() {{
                const xhr = new originalXHR();
                const open = xhr.open;
                xhr.open = function(method, url, ...args) {{
                    if (url.startsWith("http")) {{
                        url = rewriteLink(url);
                    }}
                    return open.call(this, method, url, ...args);
                }};
                return xhr;
            }};

            // Handle dynamically added elements
            const observer = new MutationObserver(fixLinks);
            observer.observe(document.body, {{ childList: true, subtree: true }});

            fixLinks();
        }})();
        </script>
        """

        # Ensure `soup.body` exists before inserting the script
        script_soup = BeautifulSoup(script, "html.parser")
        if soup.body:
            soup.body.append(script_soup)
        else:
            soup.append(script_soup)  # If no <body>, inject script into <html>

        modified_html = str(soup)
        return Response(modified_html, headers={'Content-Type': content_type})

    return Response(remote_response.content, headers={'Content-Type': content_type})

if __name__ == '__main__':
    app.run(debug=True)
