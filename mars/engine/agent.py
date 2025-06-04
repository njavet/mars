import re
import json
import ollama
from difflib import get_close_matches

# project imports
from mars.core.prompts import reflector
from mars.engine.lab4 import planner
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
            m = re.match(r'##(?: [^\n]+){1,3}\n', section + '\n')
            tlen = len(m.group(0))
            sections[m.group(0).strip()[3:]] = section[tlen:]
        return sections

    def generate_res(self) -> str:
        for section_title, section_text in self.sections.items():
            result = analyze_section_en(section_title, section_text)
            print(f'{section_title}: {result}')

        return planner(self.text)


def analyze_section_en(section_title: str, section_text: str) -> dict:
    # This calls Meditron and returns a JSON-like result
    res = ollama.chat(
        model='meditron',
        messages=[{
            'role': 'user',
            'content': f'Is the following medical section complete? Just answer with JSON: '
                       f'{{"complete": 0 or 1, "justification": "..."}},\n\n'
                       f'Section Title: {section_title}\n\nContent:\n{section_text}'
        }],
        options={'temperature': 0.1}
    )
    return res['message']['content']


def deepseek_plan(sections: list[str]) -> str:
    res = ollama.chat(
        model='deepseek-coder',
        messages=[{
            'role': 'user',
            'content': f"""
You are the planner in a multi-agent system. The user has provided a list of section titles 
from a medical report in German. Your job is to create a plan that analyzes each section
by translating it to English and then calling a medical analysis function.

The available tool is:
analyze_section_en(title: str, text: str) → returns a JSON with keys 'complete' (0/1) and 'justification'.

Plan step-by-step how the executor should proceed for each section.

Sections:
{sections}
"""
        }],
        options={'temperature': 0.3}
    )
    return res['message']['content']
