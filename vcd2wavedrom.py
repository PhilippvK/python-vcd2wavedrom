"""This module contains a class to waveforms for Wavedrom."""

from collections import OrderedDict

class VCD2Wavedrom(object):
    """This class converts waveforms in a JSON format\
 to be parsed by Wavedrom."""

    def __init__(self, vcd):
        self.vcd = vcd
        self.ticks = None
        self.timeline = None
        self.variables = None
        self.step_size = None
        self.steps = None
        self.waves = None

    def get_waves(self):
        """Fills the list of waves."""
        self.waves = []
        for variable in self.variables.values():
            wave = [(t//self.step_size, val) for (i, t) in enumerate(self.ticks)
                    for (var, val) in self.timeline[i] if var == variable]
            wave_ = ''
            for step in range(self.steps+1):
                changes = [s for (s, _) in wave]
                if step in changes:
                    if wave[changes.index(step)][1]:
                        wave_ = wave_ + '1'
                    else:
                        wave_ = wave_ + '0'
                else:
                    wave_ = wave_ + '.'
            self.waves.append(wave_)

    def build_json(self):
        """Returns string that can be intepreted by Wavedrom."""
        title = "Simulation Waveform"

        output = ""

        output = output + """{
    signal: [\n"""

        for i, variable in enumerate(self.variables.values()):
            output = output + \
                "\t\t{{ name: '{}',\twave: '{}' }},\n".format(
                    variable, self.waves[i])

        output = output + """    ],
    head: {{
        text: '{}',
        tick: {},
    }},
}}""".format(title, self.ticks[0]//self.step_size)

        return output

    def convert(self):
        """Parses the VCD dump"""
        self.ticks = []
        self.timeline = []
        #current_tick = 0
        self.variables = OrderedDict()
        searching = True
        gather_vars = True

        for line in self.vcd.split('\n'):
            if gather_vars:
                if '$timescale' in line:
                    split = line.split(' ')
                    #timescale = (int(split[-3]), split[-2])
                elif searching:
                    if '$var' in line:
                        searching = False
                        split = line.split(' ')
                        name = split[-2]
                        label = split[-3]
                        self.variables[label] = name
                else:
                    if '$var' not in line:
                        gather_vars = False
                    else:
                        split = line.split(' ')
                        name = split[-2]
                        label = split[-3]
                        self.variables[label] = name
            else:
                if len(line) == 0:
                    break
                if line[0] == '#':
                    tick = int(line[1:])
                    self.ticks.append(tick)
                    #current_tick = self.ticks[-1]
                    self.timeline.append([])
                elif line[0] == 'b':
                    split = line.split(' ')
                    label = split[-1]
                    value = bool(int(split[0][1:]))
                    self.timeline[-1].append((self.variables[label], value))

        self.step_size = min([self.ticks[i+1]-self.ticks[i]
                              for i in range(len(self.ticks)-1)]) # = 2
        self.steps = (self.ticks[-1]-self.ticks[0])//self.step_size # = 18

        self.get_waves()

        return self.build_json()
