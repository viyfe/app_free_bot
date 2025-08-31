import requests

def push_to_telegram(app, bot_token, chat_id):
    text = f"【精品限免】{app.title}\n{app.desc}\n链接: {app.link}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": False,
    }
    resp = requests.post(url, data=data)
    return resp.ok