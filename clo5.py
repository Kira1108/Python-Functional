import re

def build_match_and_apply_rule(pattern, search, replace):

    def match_rule(word):
        return re.search(pattern, word)

    def apply_rule(word):
        return re.sub(search, replace, word)
    return match_rule, apply_rule

def rules(filename):
    with open(filename,'r') as f:
        for line in f:
            match, search, replace = line.split(None, 3)
            yield build_match_and_apply_rule(match, search, replace)

def plural(noun, pattern_file = 'patterns.txt'):
    for match_rule, apply_rule in rules(pattern_file):
        if match_rule(noun):
            return apply_rule(noun)

if __name__ == '__main__':
    while True:
        noun = input('Please enter a noun >>>')
        print('Plural form of {} is {}'.format(noun, plural(noun)))
        quit = input('Try again[y/n] >>>')
        if quit.lower() == 'n':
            break
