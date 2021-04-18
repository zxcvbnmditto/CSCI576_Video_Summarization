from MotionBlock import MotionBlock
from MotionDetector import MotionDetector

class AlgorithmFactory:
    factory = {
        "motionblock": MotionBlock,
        "MotionDetector": MotionDetector
    }

    @staticmethod
    def create(name, data):
        return AlgorithmFactory.factory.get(name)(data)
