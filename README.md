
# Projekt: Integration von PostgreSQL, APIs, Docker, KI-gestützten Datenanalysen und einem Streamlit-Chatbot

Dieses Projekt wurde entwickelt, um in einem ersten kick off Projekt zu demonstrieren wie eine Implementation eines AI gesteuerten Chat Bots auf einer Datenbank aussehen könnte. Der Fokus liegt auf der Bereitstellung einer skalierbaren, datengetriebenen Lösung, die Daten aus mehreren Quellen verarbeitet, analysiert und benutzerfreundlich über eine interaktive Oberfläche verfügbar macht.

---

## Projektbeschreibung

### Zielsetzung
Das Projekt kombiniert PostgreSQL, APIs, Docker und KI-Modelle, um eine datengetriebene Plattform zu schaffen. Ein interaktiver Chatbot, implementiert mit Streamlit, ermöglicht Benutzern, über natürliche Sprachbefehle Datenbankabfragen durchzuführen. Die Abfragen werden automatisch generiert und über eine Flask-API ausgeführt.

---

### Kernbestandteile

#### 1. **PostgreSQL-Datenbank**:
- Speicherung strukturierter Daten mit optimierten Tabellen und Relationen.
- Nutzung effizienter SQL-Abfragen zur Datenanalyse und -manipulation.
- Die Daten sind generiert und spiegeln keine reelen Personen oder Prozesse wieder

#### 2. **Flask-API**:
Die API übernimmt die Kommunikation zwischen dem Streamlit-Chatbot und der Datenbank:
- **Eingehende Anfragen**: Natürliche Sprachbefehle werden entgegengenommen.
- **SQL-Generierung**: Ein KI-Modell erstellt dynamisch passende SQL-Abfragen.
- **Datenbankausführung**: Die generierten Abfragen werden in der PostgreSQL-Datenbank ausgeführt.
- **Antwortformatierung**: Ergebnisse werden als JSON-Objekte zurückgegeben.

_Code-Auszug der API_:
```python
@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get("question")
    sql_query = generate_sql_query(question)
    result = execute_sql_query(sql_query)
    return jsonify({"sql_query": sql_query, "result": result})
```

#### 3. **Streamlit-Chatbot**:
Ein interaktiver Chatbot ermöglicht Benutzern, Datenbankabfragen auf intuitive Weise zu stellen:
- **Chat-Funktion**: Benutzer geben Fragen ein, die an die API weitergeleitet werden.
- **Anzeige von Ergebnissen**: SQL-Abfragen und die zugehörigen Ergebnisse werden angezeigt.
- **Fehlerbehandlung**: Fehlermeldungen werden benutzerfreundlich dargestellt.

_Code-Auszug des Streamlit-Chatbots_:
```python
def write_answer(data):
    st.subheader("Generated SQL Query:")
    st.markdown(f"```sql\n{data['sql_query']}\n```")
    st.subheader("Query Result:")
    st.table(pd.DataFrame(data['result']))
```

#### 4. **SQL-Generator**:
Ein KI-Modell erstellt dynamisch SQL-Abfragen aus natürlichen Sprachbefehlen:
- **Transformers-Modell**: Das Modell nutzt vortrainierte Architektur wie `AutoModelForCausalLM`.
- **Textgenerierung**: Basierend auf dem Eingabeprompt wird eine SQL-Abfrage erstellt.
- **Anpassung und Feinjustierung**: Die Abfrage wird auf die spezifische Datenbankstruktur abgestimmt.

_Code-Auszug des SQL-Generators_:
```python
def generate_sql_query(question: str) -> str:
    prompt = generate_prompt(question)
    generated_query = pipeline("text-generation", model=model)(prompt)[0]["generated_text"]
    return generated_query.split(";")[0] + ";"
```

#### 5. **Docker**:
- **Containerisierung**: Die Datenbank und die API laufen in Docker Containern
- **Orchestrierung**: Mit Docker-Compose werden API, Datenbank und Chatbot orchestriert.

---

## Ergebnisse

### Erreichte Ziele
- **Skalierbare Dateninfrastruktur**: PostgreSQL speichert und verarbeitet strukturierte Daten effizient.
- **Dynamische SQL-Generierung**: Das KI-Modell erstellt funktionsfähige SQL-Abfragen.
- **Benutzerfreundlichkeit**: Der Streamlit-Chatbot ermöglicht intuitive Interaktionen.
- **Plattformunabhängigkeit**: Die Anwendung kann mit Docker einfach bereitgestellt werden.

### Herausforderungen
- Die KI-generierten SQL-Abfragen sind noch nicht vollständig zufriedenstellend und erfordern weitere Optimierung.
- Komplexere Datenbankoperationen müssen noch integriert werden.

---

## Nächste Schritte

1. **Verbesserung des KI-Modells**:
   - Anpassung der Prompt-Generierung und Optimierung der Hyperparameter.
   - Integration erweiterter Sprachverarbeitung für präzisere Ergebnisse.

2. **Erweiterung des Chatbots**:
   - Verbesserte Benutzerführung und Integration zusätzlicher Features.
   - Erweiterung der Unterstützung für komplexere Abfragen.

3. **Performance-Optimierung**:
   - Optimierung der API- und Datenbankzugriffszeiten.
   - Implementierung von Caching-Mechanismen für wiederholte Abfragen.

4. **Visualisierung**:
   - Entwicklung von Dashboards zur Darstellung von Analyseergebnissen.

---

## Installation und Nutzung

### Voraussetzungen
- **Software**:
  - Python 3.9+
  - PostgreSQL
  - Docker & Docker-Compose
- **Python-Bibliotheken**:
  - Flask, Streamlit, Transformers, SQLAlchemy, pandas


