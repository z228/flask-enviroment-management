from json import load

with open(r'apps\productApp\user.json', 'r',encoding='utf-8') as users:
    user = load(users)
    print(list(user))