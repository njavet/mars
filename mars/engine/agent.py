import re
import json
from difflib import get_close_matches

# project imports
from mars.engine.llm.ollama_llm import OllamaLLM
from mars.schema.eval import Message


class Agent:
    def __init__(self, llm: OllamaLLM, messages: list[Message]):
        self.llm = llm
        self.messages = messages
        self.text = messages[1].content
        self.sections = self.extract_sections()

    def extract_sections(self) -> dict[str, str]:
        sections = {}
        for section in self.text.split('\n\n'):
            try:
                m = re.match(r'##(?: [^\n]+){1,3}\n', section + '\n')
                tlen = len(m.group(0))
                sections[m.group(0).strip()[3:]] = section[tlen:]
            except AttributeError:
                print("FAIL", section)
        return sections

    def generate_res(self) -> str:
        res = self.llm.chat(self.messages)
        try:
            dix = json.loads(res)
        except json.decoder.JSONDecodeError:
            print('llm did not return a JSON object')
            return res

        ref_res = {}
        for section, score in dix.items():
            print('section:', section)
            content = self.extract_section_content(section)
            print('content', content)
            new_ans = self.reflect(section, content, score)
            ref_res[section] = new_ans
        just_text = '\n'.join([k + ':' + j for k, j in ref_res.items()])
        return just_text

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

    def reflect(self, section: str, content: str, complete: int):
        if complete == 1:
            as_msg = f'{section}, with this content: {content} is complete'
        else:
            as_msg = f'{section}, with this content: {content} is incomplete'

        messages = [Message(role='system', content=justifier_prompt),
                    Message(role='assistant', content=as_msg),
                    Message(role='user', content='Do you agree?')]
        res = self.llm.chat(messages)
        return res
