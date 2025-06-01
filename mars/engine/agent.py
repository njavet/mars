import re
import json
from difflib import get_close_matches

# project imports
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.schema.eval import Message
from mars.engine.prompts.medical import justifier_prompt


class Agent:
    def __init__(self, llm: OllamaLLM, messages: list[Message]):
        self.llm = llm
        self.messages = messages
        self.text = messages[1].content
        self.sections = self.extract_sections()

    def extract_sections(self) -> dict[str, str]:
        sections = {}
        for section in self.text.split('\n\n'):
            m = re.match(r'##(?: [^\n]+){1,3}\n', section + '\n')
            tlen = len(m.group(0))
            sections[m.group(0).strip()[3:]] = section[tlen:]
        return sections

    def generate_res(self) -> str:
        res = self.llm.chat(self.messages)
        try:
            dix = json.loads(res)
        except json.decoder.JSONDecodeError:
            print('llm did not return a JSON object')
            return res
        completes = {}
        justified = {}
        for section, score in dix.items():
            if score == 1:
                completes[section] = 1
            else:
                content = self.extract_section_content(section)
                print('content', content)
                justification = self.justify_missing_section(content)
                justified[section] = justification
        completes_text = '\n'.join([k + ':' + str(v) for k, v in completes.items()])
        just_text = '\n'.join([k + ':' + j for k, j in justified.items()])
        return '\n\n'.join([completes_text, just_text])


    def extract_section_content(self, section: str) -> str:
        best_match = get_close_matches(section, self.sections.keys(), n=1, cutoff=0.6)
        if not best_match:
            print(f'no best match found for section: {section}')
            return ''

        correct_header = best_match[0]
        try:
            content = self.sections[correct_header]
        except KeyError:
            content = ''
        return content

    def justify_missing_section(self, content: str) -> str:
        """
        Use another LLM to justify why the section is incomplete.
        """

        messages = [Message(role='system', content=justifier_prompt),
                    Message(role='user', content=content)]

        self.llm.params['temperature'] = 0.7
        res = self.llm.chat(messages)
        return res
