from ShotsGenerator import ShotsGenerator
from FullShotAnalyzer import FullShotAnalyzer
from SubShotAnalyzer import SubShotAnalyzer

class CompoundAnalyzer:
    def __init__(self, data):
        self.data = data
        self.score = []

    def run(self):
        break_points = ShotsGenerator(self.data, 25).get_break_points()
        print('Finished shot seperation ----------')

        if len(break_points) < 45:
            subShotAnalyzer = SubShotAnalyzer(self.data, break_points)
            subShotAnalyzer.run()

        else:
            fullShotAnalyzer = FullShotAnalyzer(self.data, break_points)
            fullShotAnalyzer.run()
