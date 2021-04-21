from MotionBlock import MotionBlock
from SubShotAnalyzer import SubShotAnalyzer

class AlgorithmFactory:
    factory = {
        "motionblock": MotionBlock,
        "subShotAnalyzer": SubShotAnalyzer
    }

    @staticmethod
    def create(name, data):
        return AlgorithmFactory.factory.get(name)(data)
