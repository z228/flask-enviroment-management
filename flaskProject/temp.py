from os import popen

with popen(
        'svn up D:\share\junit_test\\trunk_test\\assetExecute\\testcases\DBPainter\exp') as cmd:
    res = cmd.read()
print('111')
print(res)
