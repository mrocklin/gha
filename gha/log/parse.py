from subprocess import PIPE, Popen
# http://blog.lost-theory.org/post/how-to-parse-git-log-output/

git_fields = {'id': '%H',
              'author_name': '%an',
              'author_email':'%ae',
              'date': '%ad',
              'timestamp': '%at',
              'subject': '%s',
              'body': '%b'}

fields, formats= zip(*git_fields.items())

GIT_LOG_FORMAT = '%x1f'.join(formats) + '%x1e'

p = Popen('git log --format="%s"' % GIT_LOG_FORMAT, shell=True, stdout=PIPE)

(log, _) = p.communicate()

log = log.strip('\n\x1e').split("\x1e")
log = [row.strip().split("\x1f") for row in log]
log = [dict(zip(fields, row)) for row in log]

