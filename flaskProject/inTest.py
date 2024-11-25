import os


def read_command(cmd):
    with os.popen(cmd) as p:
        res = p.read()
    return res


res = read_command(fr'svn up D:\share\junit_test\trunk_test\assetExecute\testcases\Chart\exp\Sort')
print(res.split('\n'))
print(len(res.split('\n')))
