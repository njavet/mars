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


def test_single_non_semantic_newlines():
    sm = 'This \n  message\nuses \n\t\n\ntoo many newlines.\n'
    psm = parse_system_message(sm)
    expected = 'This message uses\n\ntoo many newlines.'
    assert psm == expected


def test_bullet_point_list():
    sm = 'Do:\n\n* format\n* test\n* repeat\n\nLater you should\ndo.\n'
    psm = parse_system_message(sm)
    expected = 'Do:\n\n* format\n* test\n* repeat\n\nLater you should do.'
    assert psm == expected


def test_trailing_bullet_point_list():
    sm0 = 'Do:\n\n* format\n* test\n* repeat\n'
    sm1 = 'Do:\n\n* format\n* test\n* repeat\n\n'
    sm2 = 'Do:\n\n* format\n* test\n* repeat'

    psm0 = parse_system_message(sm0)
    psm1 = parse_system_message(sm1)
    psm2 = parse_system_message(sm2)
    expected = 'Do:\n\n* format\n* test\n* repeat'
    assert psm0 == expected
    assert psm1 == expected
    assert psm2 == expected
