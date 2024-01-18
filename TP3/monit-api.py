from flask import Flask

from monit import Calls

app = Flask(__name__)

@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/status")
def status():
    return {"status": "ok"}

@app.get("/requestCheck")
def requestCheck():
    return Calls.requestCheck()

@app.get("/requestLast")
def requestLast():
    return Calls.requestLast()

@app.get("/requestAvg/<int:hours>")
def requestAvg(hours):
    return Calls.requestAvg(hours)

@app.errorhandler(404)
def page_not_found(e):
    return {"error": "404"}, 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



