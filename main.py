import valve.source.a2s 
from flask import Flask, request
from jinja2 import Template
import requests
import json
app = Flask(__name__)


@app.route('/')
def index():
    return("nerd") #Don't ask

@app.route('/metrics')
def metrics():
    pterodactyl = 1

    if pterodactyl == 1: 
        if not request.args.get("apikey") or not request.args.get("serverid") or not request.args.get("pterodactylhost") or not request.args.get("proto"):
            return("Missing paramater")
        
        apikey = request.args.get("apikey")
        serverid = request.args.get("serverid")
        pterodactylhost = request.args.get("pterodactylhost")
        proto = request.args.get("proto")
        
        if proto != "http" and proto != "https":
            return("Invalid argument")

    if not request.args.get("ip") or not request.args.get("port"):
        return("Missing paramater")
    
    ip = request.args.get("ip")
    port = int(request.args.get("port"))
    SERVER_ADDRESS = ip,port

    try:
        with valve.source.a2s.ServerQuerier(SERVER_ADDRESS) as server:
            info = server.info()
        
        server_dict = {
            "target": "%s:%s" % (ip, port),
            "players": info["player_count"],
            "max_players": info["max_players"],
            "bots": info["bot_count"]
        }


        if pterodactyl == 1:
            headers = {"Authorization": "Bearer " + apikey}
            pt = requests.get( proto + "://" + pterodactylhost + "/api/client/servers/" + serverid + "/resources", headers = headers)
            pterodactyl = pt.json()
            server_dict["cpu"] = pterodactyl["attributes"]["resources"]["cpu_absolute"]
            server_dict["memory"] = pterodactyl["attributes"]["resources"]["memory_bytes"]
            server_dict["storage"] = pterodactyl["attributes"]["resources"]["disk_bytes"]

    except: 
        return f'# HELP srcds_up is the gameserver reachable # TYPE srcds_up gauge srcds_up{{server="{ip}:{port}"}} 0'
    
    return template.render(**server_dict)

with open("response.j2", "r") as f:
    t = f.read()
    template = Template(t, trim_blocks=True, lstrip_blocks=True,)
if __name__ == "__main__":
    app.run("0.0.0.0",8080) 