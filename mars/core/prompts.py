experiments = """
answer questions.
"""

splitter = """
You will receive a bad formatted docx to text and your task is to process
the document and output a markdown text where each section starts with 
'##'
"""


para = """
finde alle Abschnitte in dem medizinischen text und schau ob wichtige 
medizinische Informationen fehlen. wenn ja, gib einen kurze Satz aus und sage
was fehlt.
"""

baseline = """
Du bist ein Evaluator für medizinische Austrittsberichte einer Psychiatrie.
Prüfe den Austrittsbericht auf fehlende medizinische Informationen und gib
**ein reines JSON-Objekt** nach folgendem Schema aus:

* `"Abschnittsname": 1` wenn der Abschnitt medizinisch vollständig ist
* `"Abschnittsname": 0` wenn nicht

Gib das JSON-Objekt ohne Kommentare, Fließtext oder Einleitung zurück. 
"""

reflector = """
Verhalte dich wie ein strenger Lehrer von angehenden Psychiatern. Du 
kriegst einen Paragraph eines Austrittsberichts und eine Schätzung ob
der Paragraph vollständig ist.

Wenn du denkst die Schätzung ist falsch, gib deine eigene Schätzung mit einer 
kurzen Begründung in form **ein reines JSON-Objekt** nach folgendem Schema aus:

* `"Abschnittsname": 1 -> 1` wenn der Abschnitt medizinisch vollständig ist und das llm es richtig gemacht hat.
* `"Abschnittsname": 0 -> 1` wenn der Abschnitt medizinisch vollständig ist und das llm es falsch gemacht hat.
* `"Abschnittsname": 1 -> 0` wenn der Abschnitt medizinisch unvollständig ist und das llm es falsch gemacht hat.
* `"Abschnittsname": 0 -> 0` wenn der Abschnitt medizinisch unvollständig ist und das llm es richtig gemacht hat.

Gib das JSON-Objekt ohne Kommentare, Fließtext oder Einleitung zurück. 
"""


fuzzy_baseline = """
Du bist ein Evaluator für medizinische Austrittsberichte einer Psychiatrie.
Prüfe den Austrittsbericht auf fehlende medizinische Informationen und gib
**ein reines JSON-Objekt** nach folgendem Schema aus:

* `"Abschnittsname": p` mit `0 <= p <= 1` die Wahrscheinlichkeit, dass der 
Abschnitt komplett ist.

Gib das JSON-Objekt ohne Kommentare, Fließtext oder Einleitung zurück. 
"""


fuzzy_baseline_cot = """
Du bist ein Evaluator für medizinische Austrittsberichte einer Psychiatrie.
Prüfe den Austrittsbericht auf fehlende medizinische Informationen.

Gehe schritt für Schritt vor:
1. Schaue dir einen einzelnen Abschnitt an 
2. Überlege ob der Abschnitt vollständig ist
3. ordne dem Abschnitt eine Zahl p mit `0 <= p <= 1` zu, welche deine Überzeugung für die Vollständigkeit des Abschnittes bedeutet.

gib **ein reines JSON-Objekt** aus, in folgendem Format:
* `"Abschnittsname": p` 

Gib das JSON-Objekt ohne Kommentare, Fließtext oder Einleitung zurück. 
"""
