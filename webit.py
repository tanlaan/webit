import sys
from markdown2 import Markdown
markdowner = Markdown()
categories = {}

def main(filename='bookmarks.mkd', prefix=''):
    print(prefix)
    if prefix[-1:] != '/':
        prefix += '/'
    infile = open(f'{filename}','r')
    outfile = open(f'{prefix + "index.html"}','w')
    categorize(infile, prefix)
    converted = markdowner.convert(infile.read())
    linked = linkify(converted)
    templated = templatize(linked, 'template.html')
    outfile.write(templated)
    outfile.close()
    infile.close()
    return


def categorize(infile, prefix=''):
    # Make sure we are at the beginning of the file
    infile.seek(0)
    for line in infile:
        for word in line.split():
            if word[0] == '#':
                if word not in categories:
                    categories[word] = []
                categories[word].append(line)
    seperator = ''
    for category in categories:
        catfile = open(prefix + category[1:] + '.html', 'w')
        # Join the file for edge case
        joined = seperator.join(categories[category])
        catfile.write(linkify(markdowner.convert(joined)))
        catfile.close()

    # Put our file pointer back
    infile.seek(0)
    return

def templatize(data, filename):
    tempPage = ''
    template = open(filename, 'r')
    for line in template:
        if '<!-- Insert Here -->' in line:
            tempPage += data
        else:
            tempPage += line

    return tempPage

def linkify(page):
    seperator = ''
    tempPage = ''
    for line in page.split('\n'):
        tempLine = ''
        for word in line.split():
            if word[0] == '#':
                tempLine += f'<a href = "{word[1:] + ".html"}">{word}</a> '

            else:
                tempLine += word + ' '
        tempPage += tempLine + '\n'
    return tempPage



if __name__ == '__main__':
    # Input markdown file and output folder
    try:
        main(sys.argv[1], sys.argv[2])
    except:
        main()

