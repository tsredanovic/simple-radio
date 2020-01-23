from radio import Radio

radio = Radio()

printout = ''
for command_data in sorted(radio.commands, key=lambda command_data: command_data['command']):

    # Description
    printout += '#### `{}`\n'.format(command_data['description'])

    # Keywords
    keywords_str = ''
    for keyword in command_data['keywords']:
        keywords_str += '`{}`, '.format(keyword)
    keywords_str = keywords_str.rstrip(', ')
    printout += '- Command keywords: {}\n'.format(keywords_str)

    # Example
    printout += '- Example: `{}`\n'.format(command_data['example'])


    printout += '\n'

printout = printout.rstrip('\n')
print(printout)