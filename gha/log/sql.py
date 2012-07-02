def stringify(s):
    return '"%s"'%s

def insert_statement(d, table_name):
    keys = sorted(d.keys())
    values = [d[key] for key in keys]

    return "INSERT INTO %s\n(%s)\nVALUES\n(%s);"%(
            table_name,
            ', '.join(keys),
            ', '.join(map(stringify, values)))
