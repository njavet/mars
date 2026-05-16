import re
import json
from rich.console import Console

# project imports
from mars.engine.parsing import parse_text_to_llm_input
from mars.core.prompts import diagnosis_specialist
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.schema.eval import Message


class Agent:
    def __init__(self, llm: OllamaLLM, messages: list[Message]):
        self.console = Console()
        self.llm = llm
        self.messages = messages
        self.text = messages[1].content
        self.sections = self.extract_sections()

    def extract_sections(self) -> dict[str, str]:
        sections = {}
        for section in self.text.split('\n\n'):
            m = re.match(r'##(?: [^\n]+){1,3}\n', section.strip() + '\n')
            tlen = len(m.group(0))
            sections[m.group(0).strip()[3:]] = section[tlen:]
        return sections

    def sections_to_text(self):
        tt = []
        for key, value in self.sections.items():
            tt.append('## {}\n{}'.format(key, value))
        return '\n\n'.join(tt)

    @staticmethod
    def get_tool():
        return [{"type": "function",
                 "function": {
                     "name": "analyze_diagnosis",
                     "description": "analyze the diagnosis section",
                     "parameters": {
                         "type": "object",
                         "properties": {
                             "text": {
                                 "type": "string",
                                 "description": "The content of the diagnosis section",
                             },
                         },
                         "required": ["text"]
                     }
                 }}]

    @staticmethod
    def analyze_diagnosis(text: str) -> str:
        print('I GOT CALLED FOR', text)
        messages = [Message(role='system', content=parse_text_to_llm_input(diagnosis_specialist)),
                    Message(role='user', content=text)]
        llm = OllamaLLM('llama3.1:8b', 'http://localhost:11434')
        res = llm.chat(messages)
        return res

    def generate_res(self) -> str:
        tool_called = self.llm.chat_with_tools(self.messages, tools=self.get_tool())
        if tool_called:
            diag = self.sections['Diagnosen']
            res = json.loads(self.analyze_diagnosis(diag))
            self.sections.pop('Diagnosen')
            self.messages[1].content = self.sections_to_text()
            res.update(json.loads(self.llm.chat(self.messages)))
            res = json.dumps(res)
        else:
            res = self.llm.chat(self.messages)
        return res


