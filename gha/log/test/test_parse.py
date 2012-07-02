from gha.log.parse_log import log, git_fields
from gha.log.parse_whatchanged import parse_commit, whatchanged

def test_log():
    stream = log()
    def correct_keys(d):
        return set(stream.next().keys()) == set(git_fields)

    assert all(correct_keys(d) for d in stream)

def test_parse_commit():
    s = """ 70d35b5d06c929e17cdfe45253adad7739b68c2f

    D       languages/README.md
    D       languages/data/language_connections
    """
    assert parse_commit(s) == ("70d35b5d06c929e17cdfe45253adad7739b68c2f",
            (('D','languages/README.md'),
             ('D','languages/data/language_connections')))

def test_whatchanged():
    stream = whatchanged()
    def valid(id, files):

        def is_status(stat):
            return stat in 'ACDMRTUX'
        def is_path(path):
            return isinstance(path, str)

        return (isinstance(id, str) and len(id) == 40 # this is a commit hash
                and
                all(is_status(stat) and is_path(path) for stat, path in files))
    assert all(valid(id, files) for id, files in stream)

