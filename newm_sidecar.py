import json
import time
import uuid
import hmac
import hashlib
import base64
import requests
import sys

guac_server = "http://localhost:8080/guacamole"
secret = "guacsecret"
protocol = "vnc"
ip_address = "localhost"
port = 5900
timestamp = int(round(time.time()*1000))

# Create signature
message = "%d%s%s%d" % (timestamp, protocol, ip_address, port) # username + passwd
signature = base64.b64encode(
    hmac.new(
        secret.encode("ascii"),
        message.encode("ascii"),
        hashlib.sha256
    ).digest()
)


# Create UUID for connection ID
conn_id = str(uuid.uuid4())
base64_conn_id = base64.b64encode(("%s\0c\0hmac" % conn_id).encode("ascii"))

# Build the POST request
# Additional parameters from Guacamole docs can be added with "guac." prefix
request_string = ('timestamp=' + str(timestamp)
                  + '&guac.port=' + str(port)
                  # + '&guac.username=' + username
                  # + '&guac.password=' + passwd
                  + '&guac.protocol=' + protocol
                  + '&signature=' + signature.decode("ascii")
                  + '&guac.hostname=' + ip_address
                  + '&id=' + conn_id)

# Send request to Guacamole backend and record the result
response = requests.post(guac_server + '/api/tokens', data=request_string)

if response.status_code != 200:
    raise Exception("Guacamole server responded with %d." % response.status_code)

# Extract token and build URL
token = json.loads(response.content)['authToken']
print("%s/#/client/%s?token=%s" %
      (guac_server, base64_conn_id.decode("ascii"), token))
