# Cambotmanager
## Benutzeranleitung
### Setup
Wenn das ganze bereits auf dem Raspberry installiert und aufgesetzt sein so brauchen sie Lediglich die Schritte 6 und 7 zu befolgen.  Ansonsten wird unten erklärt wie sie das Projekt auf dem Raspberry zum laufen kriegen. 
#### Raspberry Pi
Auf dem Raspberry pi muss ein Reverse Proxy so wie der Cambotmanager dienst installiert, Konfiguriert und gestartet sein. 
##### Reverse Proxy
Um den Reverse Proxy zu installieren halten sie sich an die Anleitung von [NGINX Proxy Manager](https://nginxproxymanager.com/guide/).

Nachdem sie alles Installiert und sich angemeldet haben, sollten sie sich auf dem Dashboard des Proxy Managers befinden. 
Hier klicken sie auf "Access List" und dann auf "Add Access List"
**Details**
hier setzen sie einen Namen z.B. "Cambot Access" akktivierne sie "Satisfy Any"
![enter image description here](https://raw.githubusercontent.com/Red8Bee/Cambotmanager-IPA-Maurice-Meier/main/images/ProxyManager%20AccessDetails.png)
**Authorization**
Hier können sie Benutzer erstellen welche auf die API und das UI zugreiffen dürfen.
![enter image description here](https://raw.githubusercontent.com/Red8Bee/Cambotmanager-IPA-Maurice-Meier/main/images/ProxyManager%20AccessAuth.png)
**Access**
Hier werden die autorisierten IP Adressen aufgelistet.
![enter image description here](https://raw.githubusercontent.com/Red8Bee/Cambotmanager-IPA-Maurice-Meier/main/images/ProxyManager%20AccessAcess.png)

Danach erstellen sie einen Proxy Host. mit folgenden Angaben.
Domain Names: cambot
IP: IP des Raspberry Pi's
Forward Port: 5000
Access List: die gerade erstellte liste auswählen.
![enter image description here](https://raw.githubusercontent.com/Red8Bee/Cambotmanager-IPA-Maurice-Meier/main/images/Proxymanager%20proxyhost.png)


Nach dem sie den Domain Namen zusammen mit der IP im Hostfile des Pcs überwelchen sie zugreiffen wollen. Nach dem sie den Cambotmanager aufgesetzt und gestartet haben können sie über ``cambot/`` das UI aufrufen. 

##### Cambotmanager
1. Git Repository  Herunterladen.
Laden sie den Code von Github herunter und speichern sie den Ordner "cambotmanager" unter "/home/pi"
2. Alle Komponenten installieren
Führen sie diese beiden Befehle aus
``sudo apt update``
``sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools`` 
3. Virtuelles Python environment erstellen
``sudo apt install python3-venv``
``cd ~/cambotmanager``
``python3 -m venv myprojectenv``
``python3 -m venv myprojectenv``
``source myprojectenv/bin/activate``
4. Flask aufsetzen
``pip install wheel``
``pip install uwsgi flask``
``sudo ufw allow 5000``
5. WSGI Entry Point erstellen 
``nano ~/cambotmanager/wsgi.py``
Kopieren sie folgendes in dieses Document
```
from app import app

if __name__ == "__main__":
    app.run()
```
6. start uWSGI
``uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app``
7. Testen
Der Cambotmanager sollte nun über die IP des Raspberry erreichbar sein.  Öffnen sie ``http://your_raspberry_ip:5000``

### Startup
Um den Cambot zu starten müssen sie folgendes machen. 

 1. Starten sie den Raspberry. 
 2. in der Console des Raspberrys starten sie das Virtuelle Environment cambotenv
 ```
 cd cambotmanager
 source cambotenv/bin/activate
 ```
 3. führen sie folgenden Befehl aus
 ``uwsgi --socket 0.0.0.0:5000 --protocol=http --enable-threads -w wsgi:app``


### Rechtssystem
Die Sicherheit der Applikation wird vom Reverse Proxy gestellt. Er wurde so konfiguriert, dass nur aufrufe von Autorisierten IP-Adressen oder mit einem Benutzer und Passwort möglich sind.
Standard mässig werden alle IPs blockiert und der Zugriff ist nur mit dem Benutzer und Passwort möglich. Will man nun zum Beispiel mit dem Cambotprocesser darauf zu greifen so kann die IP des PCs auf welchem dieser dienst läuft autorisiert werden.
#### Erstellen von neuen Benutzer/Autorisieren von IP's
Um einen Benutzer zu erstellen oder eine IP zu autorisieren öffnen sie den Proxy Manager. Dazu öffnen sie ``http://your_raspberry_ip:81`` und melden sie sich an. 
Unter dem Abschnitt "Access Lists" bearbeiten sie die Liste mit dem Namen "Cambot Access" 
Dort können sie im Abschnitt "Authorization" neue Benutzer erstellen oder unter "Access" IPs freischalten.

### Probleme
Sollte beim erstellen von Snapshots ein Problem beim Roboter auftauchen z.B. das Erreichen eines Endschalters so setzt er sich in seine Home position zurück und das Momentane Item wird abgebrochen. Sollte dies nicht funktionieren so kann der Roboter über das UI ebenso in die Home position zurück versetzen. 
## Benutzerdokumentation
### Aufbau des Cambotmanagers
#### Models
Um die Daten einfacher handhaben zu können wurden Models geschrieben, um diese abstrakt darzustellen. Sie sind nach den Schemas auf Swagger realisiert. Der Aufbau sieht wie folgt aus:
#### Manager
Die Aufgabe des Managers ist es die Daten aus den Models aufzuarbeiten, Zips zu erstellen und diese an die IPA weiterzugeben. Hier wird auch das Inventar gespeichert.
#### Storage-Handler
Der Storage-Handler überwacht den Speicherplatz und sorgt falls nötig für Ordnung. Hier sollen regelmässig alle Items mit dem Status «scheduled_delete» gelöscht werden.
#### Cambot-Handler
Der Cambot-Handler steuert den Roboter und die Cammera an und macht so die Snapshots. Er hohl sich ein Item aus dem Inventar und führt die dazu gehörende Config aus. Es kann immer nur 1. Item gleichzeitig mit Snapchats befüllt werden.

### Workflow 
Hier wird der Workflow vom erstellen eines Items bis hin zum Download des generierten Zip's Dargestellt.
![enter image description here](https://raw.githubusercontent.com/Red8Bee/Cambotmanager-IPA-Maurice-Meier/main/images/Workflow.png)
