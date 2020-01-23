import json

import vlc

class Radio():
    # INIT
    def __init__(self):
        # define VLC instance
        self.vlc_instance = vlc.Instance()

        # disable logging
        self.vlc_instance.log_unset()

        # define VLC player
        self.player = self.vlc_instance.media_player_new()

        # define stations
        self.stations = self.load_stations()
        for station_data in self.stations.values():
            station_data['media'] = self.vlc_instance.media_new(station_data['url'])

        # set default station
        media = sorted(self.stations.items(), key=lambda item: item[0])[0][1]['media']
        self.player.set_media(media)        

        # define commands
        self.commands = [
            {
                'command': 's',
                'description': 'Change station.',
                'generic_example': 's {station_id}',
                'example': 's 1',
                'execute': self.cmd_change_station,
                'keywords': ['s', 'station']
            },
            {
                'command': 'v',
                'description': 'Change volume.',
                'generic_example': 'v {volume}',
                'example': 'v 50',
                'execute': self.cmd_change_volume,
                'keywords': ['v', 'vol', 'volume']
            },
            {
                'command': 'stop',
                'description': 'Stop playing.',
                'generic_example': 'stop',
                'example': 'stop',
                'execute': self.cmd_stop,
                'keywords': ['stop']
            },
            {
                'command': 'start',
                'description': 'Start playing.',
                'generic_example': 'start',
                'example': 'start',
                'execute': self.cmd_start,
                'keywords': ['start', 'play']
            },
            {
                'command': 'help',
                'description': 'Show commands.',
                'generic_example': 'help',
                'example': 'help',
                'execute': self.cmd_print_commands,
                'keywords': ['help', 'cmds', 'commands', 'h']
            },
            {
                'command': 'stations',
                'description': 'Show available stations.',
                'generic_example': 'stations',
                'example': 'stations',
                'execute': self.cmd_print_stations,
                'keywords': ['stations']
            },
            {
                'command': 'q',
                'description': 'Shut down the radio.',
                'generic_example': 'q',
                'example': 'q',
                'execute': self.cmd_quit,
                'keywords': ['q', 'quit', 'off', 'shutdown']
            }
        ]
    
    def load_stations(self, file_path='./stations.json'):
        with open(file_path) as json_file:
            return json.load(json_file)
    
    # ACTIONS
    def print_stations(self):
        printout = ''
        for station_id, station_data in sorted(self.stations.items(), key=lambda item: item[0]):
            printout += '\t{} : {}\n'.format(station_id, station_data['name'])
        printout = printout.rstrip('\n')
        print(printout)
    
    def print_commands(self):
        printout = ''
        for command_data in sorted(self.commands, key=lambda command_data: command_data['command']):
            printout += '\t{} - {}\n'.format(command_data['generic_example'], command_data['description'])
        printout = printout.rstrip('\n')
        print(printout)
    
    def change_station(self, station_id):
        media = self.stations[station_id]['media']
        self.player.set_media(media)
        self.player.play()
    
    def change_volume(self, volume):
        self.player.audio_set_volume(volume)
    
    def start(self):
        self.player.play()
    
    def stop(self):
        self.player.stop()

    # COMMANDS
    def cmd_print_commands(self, arguments):
        self.print_commands()

    def cmd_print_stations(self, arguments):
        self.print_stations()

    def cmd_change_station(self, arguments):
        station_id = arguments[0]
        self.change_station(station_id)
        print('\tPlaying: {}'.format(self.stations[station_id]['name']))
    
    def cmd_change_volume(self, arguments):
        volume = int(arguments[0])
        self.change_volume(volume)
        print('\tVolume: {}'.format(volume))
    
    def cmd_start(self, arguments):
        self.start()
        print('\tStarted playing.')
    
    def cmd_stop(self, arguments):
        self.stop()
        print('\tStopped playing.')

    def cmd_quit(self, arguments):
        exit()

    # RUN
    def get_command_from_keyword(self, keyword):
        for command in self.commands:
            if keyword in command['keywords']:
                return command
        return None

    def execute_command(self, command):
        split_command = command.split(' ')
        base = split_command[0]
        arguments = split_command[1:]
        command = self.get_command_from_keyword(base)
        if not command:
            print('\tUnknown command (use command `help` for a list of commands).')
            return
        command['execute'](arguments)

    def run(self):
        while True:
            command = input('Enter command: ')
            self.execute_command(command)
