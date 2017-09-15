# encoding: utf-8


def replace(old='.env', new='.newenv'):
    try:
        with open('.newenv', 'r') as new:
            new = [x.split('=', 1) for x in new.read().splitlines() if x]
            new = {x[0]: x[1] for x in new}
    except Exception as e:
        print(e)
        new = {}
    lines = []
    with open('.env', 'r') as old:
        for line in old.read().splitlines():
            line = line.split('=', 1)
            if not len(line) == 2 and isinstance(line, list):
                lines.append('='.join(line))
            else:
                value = new.get(line[0], line[1])
                lines.append('{0}={1}'.format(line[0], value))
    with open('.env', 'w') as env:
        env.write('\n'.join(lines))
    import os
    try:
        os.unlink('.newenv')
    except:
        pass
