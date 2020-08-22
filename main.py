from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
import json
import subprocess

app = FastAPI() 


def print_alarm_noise(alarm_file_name):
    print_alarm = subprocess.run(["lpr", alarm_file_name])
    print("The exit code was: %d" % print_alarm.returncode)


def write_to_file(alarm):
    alarm_file_name = "alarm.txt"
    with open(alarm_file_name, "w") as text_file:
        text_file.write("Alarm Status: {}\n".format(alarm['status']))
        text_file.write("\n")
        text_file.write("Alarm Summary: {}\n".format(alarm['commonAnnotations']['summary']))
        text_file.write("\n")
        text_file.write("Severity is:  {}\n".format(alarm['commonLabels']['severity']))
        text_file.write("\n")
        text_file.write("Host:  {}\n".format(alarm['commonLabels']['instance']))
    print_alarm_noise(alarm_file_name)


def validate_prom_alarm(alarm):
    if alarm['receiver'] == "on-call-printing":
      return True
    return False


@app.get("/")
async def root():
    return {"message": "Goliath Online!"}


@app.post("/api/incoming_alerts")
async def incoming_alerts(request: Request):
    body = await request.body()
    alarm_json = json.loads(body)
    if validate_prom_alarm(alarm_json):
        write_to_file(alarm_json)
        return {"message": "Alert received!"}
    else:
        return {"message": "This is not a Prometheus Alarm!"}
