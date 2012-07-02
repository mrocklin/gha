import re
from gha.log.regexes import *

commit_message = """
commit 8a840cc3fd6b8c0f8172d359215ec5f7c02e3bb6
Author: Matthew Rocklin <mrocklin@gmail.com>
Date:   Mon Jul 2 09:14:15 2012 -0500

    added repositories note to README

    and did some other things

M       gha/repositories/README.md
A       new-README.md
"""

def matches(prog, s):
    """ Returns true if prog (a regex) matches the string s """
    return prog.search(s) is not None

def test_matches():
    prog = re.compile('hello')
    assert matches(prog, "hello world")
    assert not matches(prog, "'ello world")

def test_email_regex():
    prog = re.compile(email_regex)
    assert matches(prog, 'Joe_Schmoe1323@gmail.com')
    assert matches(prog, 'fhsh__234@sfhs.uk.co')
    assert not matches(prog, 'hello world')
    assert not matches(prog, 'matt@gmail')

def test_email():
    prog = re.compile(email)
    assert prog.search(commit_message).groupdict() == {'email':
            "mrocklin@gmail.com"}

def test_fullcommit():
    prog = re.compile(fullcommit)
    assert matches(prog, "a2a7ab4f2e7b6596aca0d7ca31def819d876b3f9")
    assert not matches(prog, "8b9ba6f")

def test_commit():
    prog = re.compile(commit)
    assert matches(prog, "commit 1b2d36f16c6ad9adfca672a3efde25fa20d8247b")
    assert not matches(prog, "1b2d36f16c6ad9adfca672a3efde25fa20d8247b")
    assert prog.search(commit_message).groupdict() == {"commit":
                "8a840cc3fd6b8c0f8172d359215ec5f7c02e3bb6"}

def test_author():
    prog = re.compile(author)
    assert matches(prog, "Author: Joe Schmoe")
    assert not matches(prog, "Joe Schmoe")
    assert prog.search(commit_message).groupdict() == {'name':
                                                       "Matthew Rocklin"}

def test_date():
    prog = re.compile(date)
    assert matches(prog, "Date:   Thu Jun 28 14:45:12 2012 -0500")
    assert prog.search(commit_message).groupdict() == \
                   {'day_number': '2',
                    'day_of_week': 'Mon',
                    'hour': '09',
                    'minute': '14',
                    'month': 'Jul',
                    'second': '15',
                    'timezone': '-0500',
                    'year': '2012'}

def test_file():
    prog = re.compile(file_regex)
    assert matches(prog, "hello.txt")
    assert matches(prog, "hello_world.c")

def test_path():
    prog = re.compile(path)
    assert matches(prog, "gha/log/regexes.py")
    assert matches(prog, "regexes.py")

def test_git_status():
    prog = re.compile(git_status)
    assert matches(prog, "A")
    assert matches(prog, "M")

def test_file_changed_line():
    prog = re.compile(file_changed_line)
    assert matches(prog, "A       gha/log/test/test_regex.py")
    assert matches(prog, "M       README.md")
    assert prog.findall(commit_message) == [
            ('M', 'gha/repositories/README.md'),
            ('A', 'new')]
