def parse(filename):
    try:
        with open(filename, 'r') as fd:
            data = [x.split('=', 1) for x in fd.read().splitlines() if x]
            data = {x[0]: x[1] for x in data if len(x) == 2}
    except Exception as e:
        print(e)
        data = {}
    return data


def replace(old='.env', new='.newenv'):
    new = parse('.newenv')
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
