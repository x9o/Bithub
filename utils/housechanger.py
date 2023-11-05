import requests

def hypesquadchanger(house, token):
   
    
    validityTest = requests.get('https://discordapp.com/api/v6/users/@me', headers={'Authorization': token, 'Content-Type': 'application/json'})
    if validityTest.status_code != 200:
        holder = "❌ Invalid token."
        return holder
    else:
        headers = {'Authorization': token, 'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.305 Chrome/69.0.3497.128 Electron/4.0.8 Safari/537.36'}
        if house == "bravery": payload = {'house_id': 1}
        elif house == "brilliance": payload = {'house_id': 2}
        elif house == "balance": payload = {'house_id': 3}
        else:
            holder = "❌ Invalid house."
            return holder
        r = requests.post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload, timeout=10)
        if r.status_code == 204:
          holder = f"✅ Sucessfully changed user's house to {house}"
          return holder
        else:
            holder = "❌ Error. Please try again."
            return holder
     
          
