# Cybergiga Shop: Daten

Nur Produktdaten für die Shop-Seite auf https://cybergigafactory.grok.me/shop. Kein Website-Code.
Ganzer Shop: https://cybergigafactory.printify.me/

## Datei
`produkte.json` ist eine Liste, sortiert wie im Shop (neueste zuerst). Pro Produkt:

| Feld | Typ | Bedeutung |
|---|---|---|
| id | String | Printify-Produkt-ID |
| title | String | Titel |
| image | String | Mockup-Bild-URL |
| price | Zahl | Preis in EUR |
| currency | String | immer "EUR" |
| url | String | Produktseite im Printify Pop-Up Store |
| categories | String[] | Kategorien für den Filter |
| visible | Bool | nur `true` wird angezeigt |
| link_ok | Bool | Produktlink lieferte HTTP 200 |
| link_status | Zahl | zuletzt gemessener HTTP-Code |

Die Seite zeigt nur Produkte mit `visible: true` (das schließt `link_ok: true` ein).

## Raw-URL
https://raw.githubusercontent.com/cybergigafactory/Cybergiga-Shop-data/main/produkte.json

## Neu erzeugen
Auf der Box: `python3 /workspace/GrokBot/shop/build_produkte.py` (Token aus der Umgebungsvariable `PRINTIFY_API_TOKEN`, nur lesende API-Aufrufe). Danach die Links prüfen, Produkte ohne HTTP 200 auf `visible: false` setzen, Datei hierher kopieren und pushen. Niemals Tokens committen.
