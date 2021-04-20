from MotionBlock import MotionBlock
from CompoundAnalyzer import CompoundAnalyzer

class AlgorithmFactory:
    factory = {
        "motionblock": MotionBlock,
        "compoundAnalyzer": CompoundAnalyzer
    }

    @staticmethod
    def create(name, data):
        return AlgorithmFactory.factory.get(name)(data)
