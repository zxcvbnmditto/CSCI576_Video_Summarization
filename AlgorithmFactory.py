from MotionBlock import MotionBlock
from SubShotAnalyzer import SubShotAnalyzer
from FullShotAnalyzer import FullShotAnalyzer
from CompoundAnalyzer import CompoundAnalyzer

class AlgorithmFactory:
    factory = {
        "motionblock": MotionBlock,
        "subShotAnalyzer": SubShotAnalyzer,
        "fullShotAnalyzer": FullShotAnalyzer,
        "compoundAnalyzer": CompoundAnalyzer
    }

    @staticmethod
    def create(name, data):
        return AlgorithmFactory.factory.get(name)(data)
