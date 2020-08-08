import json

with open('keys.json', 'r') as f:
    loaded_keys = json.load(f)

site_settings = {
    'debug': True,
    'autoreload': True,
    'cookie_secret': loaded_keys["COOKIE_SECRET"],
}