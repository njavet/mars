# project imports
from mars.engine.prompts import prompts, medical
from mars.schema.res import SystemMessage


def load_system_messages():
    lst = []
    for name in dir(medical):
        if not name.startswith('_'):
            text = getattr(medical, name)
            sm = SystemMessage(key=name,
                               text=text)
            lst.append(sm)
    for name in dir(prompts):
        if not name.startswith('_'):
            text = getattr(prompts, name)
            sm = SystemMessage(key=name,
                               text=text)
            lst.append(sm)
    return lst
