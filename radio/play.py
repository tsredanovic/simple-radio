import json

from radio import Radio

radio = Radio()
print('Commands:')
radio.print_commands()
print('Stations:')
radio.print_stations()
radio.run()
