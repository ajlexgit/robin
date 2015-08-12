import os


def trail_file(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append('%s\n' % line.rstrip())

    with open(filename, 'w+') as f:
        f.writelines(lines)


for path, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(path, file)
            trail_file(filepath)
