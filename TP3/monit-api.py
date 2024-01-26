#!/usr/bin/python3
from flask import Flask
from flasgger import Swagger
from monit import Calls

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/status", methods=["GET"])
def status():
    """
    The status endpoint
    ---
    responses:
      200:
        description: Status OK
    """
    return {"status": "ok"}


@app.route("/run/check", methods=["GET"])
def requestCheck():
    """
    The check request endpoint
    ---
    responses:
      200:
        description: Check request
    """
    Calls.requestCheck()
    return {"status": "ok"}


@app.route("/reports", methods=["GET"])
def requestReports():
    """
    The reports endpoint
    ---
    responses:
      200:
        description: Reports
    """
    reports = Calls.requestReports()
    if reports is None:
        return {"error": "No report found"}, 404
    return reports


@app.route("/reports/latest", methods=["GET"])
def requestLast():
    """
    The latest report endpoint
    ---
    responses:
      200:
        description: Latest report
    """
    last = Calls.requestLast()
    if last is None:
        return {"error": "No report found"}, 404
    return last


@app.route("/reports/<string:id>", methods=["GET"])
def requestReport(id):
    """
    The report endpoint
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The report ID
    responses:
      200:
        description: Report
    """
    report = Calls.requestReport(id)
    if report is None:
        return {"error": "No report found"}, 404
    return report


@app.route("/reports/avg/<int:hours>", methods=["GET"])
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
    avg = Calls.requestAvg(hours)
    if avg is None:
        return {"error": "No report found"}, 404
    return avg


@app.errorhandler(404)
def page_not_found(e):
    return {"error": "404"}, 404


@app.errorhandler(500)
def internal_server_error(e):
    return {"error": "500"}, 500


@app.errorhandler(405)
def method_not_allowed(e):
    return {"error": "405"}, 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
