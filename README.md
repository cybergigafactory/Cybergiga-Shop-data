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
Auf der Box: `python3 /workspace/GrokBot/webseiten/shop/build_produkte.py` (Token aus der Umgebungsvariable `PRINTIFY_API_TOKEN`, nur lesende API-Aufrufe). Das Skript prüft jeden Store-Link selbst und setzt `visible` nur bei HTTP 200 (`link_status` 0 = keine Antwort). Danach Datei hierher kopieren und nach Freigabe pushen. Niemals Tokens committen.

**Archiv (30.10.2026):** 15 alte Kinderprodukte, deren Store-Links 404 lieferten, stehen jetzt in `produkte-archiv.json` statt in `produkte.json`. Der Generator überspringt sie. In Printify bleiben sie unverändert (nichts gelöscht).
