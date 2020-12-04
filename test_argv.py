from sys import argv

if len(argv) < 2:
    raise ValueError('Please pass a game to this program.')

print('Script name: {}'.format(argv[0]))
print('Game name: {}'.format(argv[1]))
