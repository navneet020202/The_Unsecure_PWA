from flask import Flask, render_template, request, redirect
from markupsafe import escape  # Correct import for escape
import user_management as dbHandler
from urllib.parse import urlparse, urljoin

app = Flask(__name__)

# Function to check if the URL is s afe for redirection
ALLOWED_DOMAINS = ['yourwebsite.com', 'localhost']

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

 #add security headers (Clickjacking Prevention)
@app.after_request
def set_security_headers(response):
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none';"
    return response

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if is_safe_url(url):
            return redirect(url, code=302)
        return "Invalid Redirect", 400  #  Block unsafe redirects

    if request.method == "POST":
        feedback = escape(request.form["feedback"])  #  XSS Protection
        dbHandler.insertFeedback(feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    
    dbHandler.listFeedback()
    return render_template("/success.html", state=True, value="Back")

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if is_safe_url(url):
            return redirect(url, code=302)
        return "Invalid Redirect", 400  #  Block unsafe redirects

    if request.method == "POST":
        username = escape(request.form["username"])  #  XSS Protection
        password = escape(request.form["password"])  #  XSS Protection
        dob = escape(request.form["dob"])  # XSS Protection
        dbHandler.insertUser(username, password, dob)
        return render_template("/index.html")

    return render_template("/signup.html")

@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        if is_safe_url(url):
            return redirect(url, code=302)
        return "Invalid Redirect", 400  #  Block unsafe redirects

    if request.method == "POST":
        username = escape(request.form["username"])  # XSS Protection
        password = escape(request.form["password"])  #  XSS Protection
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        
        return render_template("/index.html")

    return render_template("/index.html")

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(host="0.0.0.0", port=5000)  # Debug mode disabled
