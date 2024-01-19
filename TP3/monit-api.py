from flask import Flask
from flasgger import Swagger
from monit import Calls

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/status")
def status():
    """
    The status endpoint
    ---
    responses:
      200:
        description: Status OK
    """
    return {"status": "ok"}

@app.route("/run/check")
def requestCheck():
    """
    The check request endpoint
    ---
    responses:
      200:
        description: Check request
    """
    return Calls.requestCheck()

@app.route("/get/report/latest")
def requestLast():
    """
    The latest report endpoint
    ---
    responses:
      200:
        description: Latest report
    """
    return Calls.requestLast()

@app.route("/get/report/avg/<int:hours>")
def requestAvg(hours):
    """
    The average report endpoint
    ---
    parameters:
      - name: hours
        in: path
        type: integer
        required: true
        description: The number of hours
    responses:
      200:
        description: Average report
    """
    return Calls.requestAvg(hours)

@app.errorhandler(404)
def page_not_found(e):
    return {"error": "404"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)