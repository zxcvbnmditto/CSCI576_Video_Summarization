from MotionBlock import MotionBlock
from ShotAnalyzer import ShotAnalyzer

class AlgorithmFactory:
    factory = {
        "motionblock": MotionBlock,
        "ShotAnalyzer": ShotAnalyzer
    }

    @staticmethod
    def create(name, data):
        return AlgorithmFactory.factory.get(name)(data)
