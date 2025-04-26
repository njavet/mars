1 Instruction hierarchy and context “dilution”

    System > Developer > User > Assistant is the fixed order the model obeys.

    Anything you put inside the single real system message is absolute law.

    Every extra sentence in that system block competes with your RAG insert (“{docs}”) and with the user’s question (“{query}”).

So:

### system ###
### RAG documents ###
Here you have documents from a RAG system. Answer based on this.
{docs}
### user query ###
{query}

is minimal: the model sees one instruction (“answer from these docs”) plus the docs and the query. Nothing else distracts it.

When you bolt on more paragraphs—especially ones that talk about sexism, offensive language, policy, etc.—you are:

    Eating tokens → less room for your actual documents.

    Possibly contradicting yourself (“Answer from these docs” and “Never produce sexist content” and “Tone must be funny”…). The model now has to reconcile them.

    Accidentally flagging policy triggers (words like sexist, offensive, harassment are themselves cues for the safety classifier).

Because system-level text has the highest priority, a single line like “If any content could be offensive, you must refuse” will override the “answer from docs” request—even if you never meant it that way.:wq
