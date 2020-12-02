import re


def plural(noun):

    if re.search('[sxz]$', noun):
        return re.sub('$','es', noun)

    elif re.search('[^aeioudgkprt]h$', noun):
        return re.sub('$', 'es', noun)

    elif re.search('[^aeiou]y', noun):
        return re.sub('y$','ies', noun)

    else:
        return noun + 's'



if __name__ == '__main__':
    while True:
        noun = input('Please enter a noun >>>')
        print('Plural form of {} is {}'.format(noun, plural(noun)))
        quit = input('Try again[y/n] >>>')
        if quit.lower() == 'n':
            break

            
