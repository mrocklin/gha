from subprocess import PIPE, Popen

def whatchanged():
    delimiter = "--new-commit--"
    format = delimiter+'%H'
    p = Popen('git whatchanged --format="%s" --name-status'%(format),
            shell=True, stdout=PIPE)
    s = p.stdout.read() # sigh

    text_stream = filter(lambda x: x.strip(), s.split(delimiter))
    return map(parse_commit, text_stream)

def parse_commit(s):
    lines = s.split('\n')
    id = lines[0].strip()

    return id, tuple(tuple(line.strip().split())
                            for line in lines[1:] if line.strip())
