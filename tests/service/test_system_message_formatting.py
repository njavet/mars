import pytest

# project imports
from mars.service.parsing import parse_system_message


def test_tabs_whitespaces():
    sm = '  This\tis a  bad formatted system message.\n'
    psm = parse_system_message(sm)
    assert psm == 'This is a bad formatted system message.'


def test_multiple_newlines():
    sm = 'This \n\n\n  message \n\n uses \n\n\n\ntoo many newlines.\n'
    psm = parse_system_message(sm)
    expected = 'This\n\nmessage\n\nuses\n\ntoo many newlines.'
    assert psm == expected


def test_bullet_point_list():
    sm = """
    Do the following:\n* format\n* test\n* repeat\nLater you should\n
    do something else.\n
    """
    psm = parse_system_message(sm)
    expected = 'Do the following:\n* format\n* test\n* repeat\nLater you should do something else.'
    assert psm == expected
