import requests

BASE_URL = "https://g3cyberspace3.sharepoint.com/sites/Demosite/"
FOLDER_PATH = "/sites/Demosite/Shared Documents/Evidence"

COOKIES = {
    "FedAuth": "77u/PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz48U1A+VjE0LDBoLmZ8bWVtYmVyc2hpcHwxMDAzMjAwNTI5YWNlMWU3QGxpdmUuY29tLDAjLmZ8bWVtYmVyc2hpcHxrZWVydGhpeWF0QGczY3liZXJzcGFjZS5jb20sMTM0MDk5OTYyNTgwMDAwMDAwLDEzNDA0MjIwMjM3MDAwMDAwMCwxMzQxMDY5NDk4MTg5NDc1MjUsNDkuMjAwLjQzLjE0NiwzLDc2N2FmNGZkLTI5Y2ItNGY2ZS05NTM5LTgwMjBiM2FlM2Q0ZSwsMDBiOGY3YTktOTJiMC1kNTdjLTg2ZTAtNjJkZWU2NTVmZWI0LGM4MzZlM2ExLTYwY2YtNjAwMC0zOGE2LTY0NmQwZmZiNGE0MyxjODM2ZTNhMS02MGNmLTYwMDAtMzhhNi02NDZkMGZmYjRhNDMsLDAsMTM0MTAzNDkzODE4NzMyNjg3LDEzNDEwNTIyMTgxODczMjY4NywsLGV5SjRiWE5mWTJNaU9pSmJYQ0pEVURGY0lsMGlMQ0o0YlhOZmMzTnRJam9pTVNJc0luQnlaV1psY25KbFpGOTFjMlZ5Ym1GdFpTSTZJbXRsWlhKMGFHbDVZWFJBUnpORFdVSkZVbE5RUVVORkxrTlBUU0lzSW5WMGFTSTZJblZKZUZaZlRtZzNNakJ4Y3pKWFNrNXVUMVZVUVZFaUxDSmhkWFJvWDNScGJXVWlPaUl4TXpRd09UazVOakkxT0RBd01EQXdNREFpZlE9PSwyNjUwNDY3NzQzOTk5OTk5OTk5LDEzNDEwMjYyOTgxMDAwMDAwMCw1YTFkYzg5Ni01NGE4LTQ3ZDQtOTUzYS02ZjY1MTIzZTNhNGYsLCwsLCwxMTUyOTIxNTA0NjA2ODQ2OTc2LCwxOTcxNDMsZUg4RHFfeC1XR1dOXzBJMEc3TEU4d1lWREZNLCxYUEprZDZleEh5RG80SXdqNFlCSGdYck4zUEhXMkhyMDRRTU94MVI4RnE0cTlLQUhCVEYrYmtOWnBIZWJzTVhxUCtUZFRlS2MwMDY3R2RlTkNIdWRhSnkxRS9KU2tJeEYrbjJpaVpwV29xOThVcGxISi9DWnpJRVFKVHNRYXRkZG9QR0o2Tmd3cllRdXpueUFuanpQcVdKdGlrUHB6Mk1EVk8xOE1Ha2NzN2dLUjhPa1pybmJuT3k5MWgyS1puR2xkeEpyQ25yVUJGZEx5ZDZpcHdESTR1c3VORXEyNERsMjd4OVQzV1Brd2Zlc3c2Vjc1Y3FjdkdlM3VDRjB3am9od3NoaXlKYU1tREYvWjdudzBwZElZK25uSm5MZkZNbVdwUzBpM0ltQ1g1di9FZUVKZG15R0NueU1jUkZTbm4yWTRubmIzWElIK2RGV0g3RndIa1VCeUE9PTwvU1A+",
    "rtFA": "pHqyzRClC24OsiryBh8nsWOxFFVvxL2ufI7CbnZcR1UmNzY3YWY0ZmQtMjljYi00ZjZlLTk1MzktODAyMGIzYWUzZDRlIzEzNDEwMjYyOTgxOTEwMzI5OCNjODM2ZTNhMS04MGNkLTYwMDAtMzhhNi02M2E1YmZlZGZiMTQja2VlcnRoaXlhdCU0MEczQ1lCRVJTUEFDRS5DT00jMTk3MTQzIy1ndDVNenhvajJVYktuaVZuQnBUM19xRHhzTSMtZ3Q1TXp4b2oyVWJLbmlWbkJwVDNfcUR4c02UvYZiGpVTuKcOpWvspDAEJ0NFDeL7c40Cev6isATO+cKIsMonc1NJhDD7S5PrZcf/mOBZLHq6YcF7gEHEKgfUw3hPSFZsbvkOkXRnJWB9k60E2tKb4PswQXZ2+H6UGqGaHcAClR5Hqr+sk19j/vYf/nWgnYwUjSYbtUBfySIQh+WFixVJuJ+lkzMCRpfzVqTxXAXpba57tpAIY5bafziGvTVVQ6tmZztIgRNojZgmSHhzPoJooAwjQgZrQHrqXq7GvXZBfDnQ1wCPR4q+Cdd8yVDP+RgVYhHVgrlto8GI3dWoZJNHkSEMIskTrrtSerwNAtfRNPF0NLA2Xo2XZSni2gAAAA=="
}

url = (
    f"{BASE_URL}_api/Web/"
    f"GetFolderByServerRelativePath(decodedurl='{FOLDER_PATH}')/Files"
)

headers = {
    "Accept": "application/json;odata=verbose",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://g3cyberspace3.sharepoint.com/sites/Demosite/",
    "X-Requested-With": "XMLHttpRequest"
}

r = requests.get(url, headers=headers, cookies=COOKIES)

print("HTTP Status:", r.status_code)

if r.status_code != 200:
    print("❌ Error response:")
    print(r.text[:1000])
    exit()

files = r.json()["d"]["results"]

print("\n📂 Files inside Evidence folder:\n")
for f in files:
    print("•", f["Name"])
