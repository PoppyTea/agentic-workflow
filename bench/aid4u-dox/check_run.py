"""Czy przebieg zakończył się poprawnie? Wypisuje ok / fail:<powód>.

Czyta OSTATNIĄ linię `"type":"result"` i patrzy na pola statusu. Nie wolno szukać
"429" ani "rate limit" jako podciągu w transkrypcie: agent czyta pliki repo, które
opisują throttle i kody HTTP, więc te napisy występują tam legalnie.
"""
import json
import sys

path = sys.argv[1]
result = None
try:
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            if d.get("type") == "result":
                result = d
except OSError as exc:
    print(f"fail:brak-transkryptu ({exc})")
    raise SystemExit(1)

if result is None:
    print("fail:brak-linii-result")
    raise SystemExit(1)
if result.get("is_error"):
    print(f"fail:is_error subtype={result.get('subtype')} api={result.get('api_error_status')}")
    raise SystemExit(1)
if result.get("subtype") != "success":
    print(f"fail:subtype={result.get('subtype')}")
    raise SystemExit(1)
if result.get("api_error_status"):
    print(f"fail:api_error_status={result['api_error_status']}")
    raise SystemExit(1)
print(f"ok turns={result.get('num_turns')} cost={result.get('total_cost_usd')}")
