from MotionBlock import MotionBlock
from SubShotAnalyzer import SubShotAnalyzer
from FullShotAnalyzer import FullShotAnalyzer

class AlgorithmFactory:
    factory = {
        "motionblock": MotionBlock,
        "subShotAnalyzer": SubShotAnalyzer,
        "fullShotAnalyzer": FullShotAnalyzer
    }

    @staticmethod
    def create(name, data):
        return AlgorithmFactory.factory.get(name)(data)
