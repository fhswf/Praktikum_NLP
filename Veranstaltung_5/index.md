<a href="https://www.ki.fh-swf.de/jupyterhub/hub/user-redirect/git-pull?profile=nlp-environment&repo=https%3A%2F%2Fgithub.com%2Ffhswf%2FPraktikum_NLP.git&urlpath=lab%2Ftree%2FPraktikum_NLP.git%2FVeranstaltung_5%2Findex.md&branch=main&profile=nlp-environment" style=""><img src="https://www.ki.fh-swf.de/cluster_badge.svg" style="height: 32px" alt="Open in FH Cluster"></a>
# Chatbot für „Alltagsaufgaben“

In diesem Praktikum wollen wir einen Chatbot mit 
[Rasa](htps://rasa.com) entwickeln. 
Rasa ist ein Open-Source-Framework für die Entwicklung von Chatbots, das durchaus mit kommerziellen Lösungen mithalten kann. 
Ein besonderes Merkmal ist, dass Rasa auch die Dialoge mittels Machine Learning trainiert.

In unserem Chatbot wollen wir uns auf die Beantwortung von Fragen zu folgenden Themengebieten konzentrieren:
- Fragen nach der aktuellen Uhrzeit
- Fragen nach der Uhrzeit in verschiedenen Städten
- Fragen nach dem Wetter
- Witze erzählen

## Installation von Rasa
Installieren Sie Rasa mit folgendem Befehl:
```bash
pip install rasa 
```

## Erstellen eines neuen Projekts
Erstellen Sie ein neues Projekt mit folgendem Befehl:
```bash
rasa init --no-prompt
```
Dieser Befehl erstellt ein neues Projekt mit dem Namen `rasa-bot` und legt die folgenden Dateien an:
- `actions.py`: Hier werden die Aktionen definiert, die der Chatbot ausführen kann.
- `config.yml`: Hier werden die Konfigurationen für den Chatbot definiert.
- `credentials.yml`: Hier werden die Zugangsdaten für die Verbindung zu anderen Diensten definiert.
- `data/nlu.yml`: Hier werden die Trainingsdaten für das NLU-Modell definiert.
- `data/rules.yml`: Hier werden die Trainingsdaten für das Core-Modell definiert.
- `data/stories.yml`: Hier werden die Trainingsdaten für das Core-Modell definiert.
- `domain.yml`: Hier werden die Domänen-Definitionen für den Chatbot definiert.
- `endpoints.yml`: Hier werden die Endpunkte für die Verbindung zu anderen Diensten definiert.

## Definition der Intents und Actions
Fügen Sie Ihrem Projekt passende Intents und Actions für die oben genannten Themengebiete hinzu. Editieren Sie dazu die Datei `domain.yml`.

Sie brauchen die Actions noch nicht zu implementieren, sondern nur die Methodenköpfe in der Datei `actions.py` zu definieren.

## Konfiguration der Entity-Erkennung mit Spacy
Konfigurieren Sie die Entity-Erkennung mit Spacy. Editieren Sie dazu die Datei `config.yml`.

```yaml
language: en
pipeline:
  - name: SpacyNLP
    model: en_core_web_sm
  - name: SpacyTokenizer
  - name: SpacyFeaturizer
    pooling: mean
  - name: SpacyEntityExtractor
    dimensions: ["PERSON", "GPE"]
  - name: LexicalSyntacticFeaturizer
  - name: CountVectorsFeaturizer
  - name: CountVectorsFeaturizer
    analyzer: char_wb
    min_ngram: 1
    max_ngram: 4
  - name: DIETClassifier
    epochs: 100
```

## Erfassung von Trainingsdaten für Intents und Stories
Fügen Sie Ihrem Projekt Trainingsdaten für die oben genannten Themengebiete hinzu. Es sollten mindestens 10 Trainingsbeispiele pro Intent vorhanden sein und mindestens 2 Stories.

## Training der Modelle
Trainieren Sie den Chatbot mit folgendem Befehl:
```bash
rasa train
```

## Testen des Chatbots
Testen Sie den Chatbot mit folgendem Befehl:
```bash
rasa shell
```
Führen Sie einen Dialog mit dem Chatbot und überprüfen Sie, ob die Intents und Entities korrekt erkannt werden.

Die Actions werden noch nicht ausgeführt, da diese noch nicht implementiert sind.

## Implementierung der Actions
Implementieren Sie die Actions, die Sie in der Datei `domain.yml` definiert haben. Editieren Sie dazu die Datei `actions.py`.

### Action für die aktuelle Uhrzeit
Implementieren Sie eine Action, die die aktuelle Uhrzeit zurückgibt. Verwenden Sie dazu die Python-Bibliothek `datetime`.

### Action für die Uhrzeit in verschiedenen Städten
Implementieren Sie eine Action, die die Uhrzeit in verschiedenen Städten zurückgibt. Verwenden Sie dazu die Python-Bibliothek `pytz`.

### Action für das Wetter
Implementieren Sie eine Action, die das Wetter zurückgibt. Verwenden Sie dazu die Python-Bibliothek `pyowm`.
Sie können wahlweise einen eigenen API-Key für OpenWeatherMap verwenden oder den folgenden API-Key verwenden:
```text
70cc3025706fcdbd8a7631b8104b8340
```

### Action für Witze
Für die Action für Witze können Sie die folgende Joke API verwenden:
```text 
https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw,religious,political,racist,sexist,explicit&type=single
```

