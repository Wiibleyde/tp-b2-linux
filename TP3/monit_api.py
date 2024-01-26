#!/usr/bin/python3

"""Monit API

This script allows to run the Monit API.

This script requires that `flask` and `flasgger` be installed within the Python
environment you are running this script in.    
"""

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
def request_check():
    """
    The check request endpoint
    ---
    responses:
      200:
        description: Check request
    """
    Calls.request_check()
    return {"status": "ok"}


@app.route("/reports", methods=["GET"])
def request_reports():
    """
    The reports endpoint
    ---
    responses:
      200:
        description: Reports
    """
    reports = Calls.request_reports()
    if reports is None:
        return {"error": "No report found"}, 404
    return reports


@app.route("/reports/latest", methods=["GET"])
def request_last():
    """
    The latest report endpoint
    ---
    responses:
      200:
        description: Latest report
    """
    last = Calls.request_last()
    if last is None:
        return {"error": "No report found"}, 404
    return last


@app.route("/reports/<string:id_wanted>", methods=["GET"])
def request_report(id_wanted):
    """
    The report endpoint
    ---
    parameters:
      - name: id_wanted
        in: path
        type: string
        required: true
        description: The report ID
    responses:
      200:
        description: Report
    """
    report = Calls.request_report(id_wanted)
    if report is None:
        return {"error": "No report found"}, 404
    return report


@app.route("/reports/avg/<int:hours>", methods=["GET"])
def request_avg(hours):
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
    avg = Calls.request_avg(hours)
    if avg is None:
        return {"error": "No report found"}, 404
    return avg


@app.errorhandler(404)
def page_not_found(e):
    """Error 404

    Args:
        e (string): Error message

    Returns:
        json: Error message
    """
    return {"error": "404","message":e}, 404


@app.errorhandler(500)
def internal_server_error(e):
    """Error 500

    Args:
        e (string): Error message

    Returns:
        json: Error message
    """
    return {"error": "500","message":e}, 500


@app.errorhandler(405)
def method_not_allowed(e):
    """Error 405

    Args:
        e (string): Error message

    Returns:
        json: Error message
    """
    return {"error": "405","message":e}, 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
