# srcds_exporter
A exports that gets data from game servers using a2s_info queries.
My reason for making this is all of the other ones I could find used source rcon and I don't want to see the stats command being ran over and over.

This is a flask app so it can be ran behind many things. I would recommend not exposing this to the internet and instead run it on a secure closed off network. Same with anything else monitoring related really.

Supported Games:
    - Anything that supports a2s queries. I tested this with gmod but it should work with many games.

## How to install
```
git clone https://github.com/synkstar/srcds_exporter.git
cd srcds_exporter
pip3 install -r requirements.txt
python3 main.py
```

## Methods of running.

If you are running this in production for stability it is recommended to run flask apps using a WSGI server. But for testing running it directly works.

## How to query with Prometheus:
Adjust the following config to your specifications. This one assumes you are going to use pterodactyl aswell. 
```
  - job_name: 'srcds'

    static_configs:
      - targets: ["<serverip>:<serverport>:<pterodactyladdress>:<protocol http or https>:<pterodactyl apikey>:<pterodactyl server id>"]

    relabel_configs:
      - source_labels: [__address__]
        regex: "(.+):.+:.+:.+:.+:.+"
        replacement: "$1"
        target_label: __param_ip
      - source_labels: [__address__]
        regex: ".+:(.+):.+:.+:.+:.+"
        replacement: "$1"
        target_label: __param_port
      - source_labels: [__address__]
        regex: ".+:.+:(.+):.+:.+:.+"
        replacement: "$1"
        target_label: __param_pterodactylhost
      - source_labels: [__address__]
        regex: ".+:.+:.+:(.+):.+:.+"
        replacement: "$1"
        target_label: __param_proto
      - source_labels: [__address__]
        regex: ".+:.+:.+:.+:(.+):.+"
        replacement: "$1"
        target_label: __param_apikey
      - source_labels: [__address__]
        regex: ".+:.+:.+:.+:.+:(.+)"
        replacement: "$1"
        target_label: __param_serverid
      - source_labels: [__param_target]
        target_label: instance
      - target_label: __address__
        replacement: <ip>:<port> # Real exporter's IP:Port

```
And if your not using pterodactyl change pterodactyl = 1 in main.py to 0 or erase the code you are not using.
```
  - job_name: 'srcds'

    static_configs:
      - targets: ["<serverip>:<serverport>]

    relabel_configs:
      - source_labels: [__address__]
        regex: "(.+):.+"
        replacement: "$1"
        target_label: __param_ip
      - source_labels: [__address__]
        regex: ".+:(.+)"
        replacement: "$1"
        target_label: __param_port
      - target_label: __address__
        replacement: <ip>:<port> # Real exporter's IP:Port

```

## What can you do with this data ?
You could put it all into a grafana dashboard and have it display stats for a large server network if you wanted or a single server. All you would need to do for multiple servers is put them all into the targets.