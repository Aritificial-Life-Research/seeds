# -*- coding: utf-8 -*-
"""
Print the number of Cells for each cell type for all populations
"""

__author__ = "Brian Connelly <bdc@msu.edu>"
__credits__ = "Brian Connelly"


import csv

from seeds.Action import *

class PrintCellTypeCount(Action):
    """ Write the number of cells of each type for all populations

        Config file settings:
        [PrintCellTypeCount]
        epoch_start = 3    Epoch at which to start writing (default 0)
        epoch_end = 100    Epoch at which to stop writing (default end of experiment)
        frequency = 2      Frequency (epochs) to write.  In this example, we write every other epoch.  (default 1)
        priority = 0       Priority of this Action.  Higher priority Actions run first. (default 0)
        filename = cell_type_count.csv  Filename to be written to

    """

    def __init__(self, world):
        """Initialize the PrintCellTypeCount Action"""

        super(PrintCellTypeCount, self).__init__(world)
        self.epoch_start = self.world.config.getint('PrintCellTypeCount', 'epoch_start', 0)
        self.epoch_end = self.world.config.getint('PrintCellTypeCount', 'epoch_end', default=self.world.config.getint('Experiment', 'epochs', default=-1))
        self.frequency = self.world.config.getint('PrintCellTypeCount', 'frequency', 1)
        self.priority = self.world.config.getint('PrintCellTypeCount', 'priority', 0)
        self.filename = self.world.config.get('PrintCellTypeCount', 'filename', 'cell_type_count.csv')
        self.name = "PrintCellTypeCount"

        c = self.world.topology_manager.topologies[0].cell_manager.newcell(-1,-1)
        self.types = c.types
        self.world.topology_manager.topologies[0].decrement_type_count(c.type)
        c = None

        header = ['epoch', 'population']
        header += self.types

        data_file = self.datafile_path(self.filename)
        self.writer = csv.DictWriter(open(data_file, 'w'), header)
        self.writer.writeheader()

    def update(self):
        """Execute the action"""
        if self.skip_update():
	        return

        for top in self.world.topology_manager.topologies:
            row = dict(epoch=self.world.epoch, population=top.id)
            for i in xrange(len(self.types)):
                row[self.types[i]] = top.typeCount[i]
            self.writer.writerow(row)
