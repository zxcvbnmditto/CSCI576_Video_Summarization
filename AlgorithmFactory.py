from MotionBlock import MotionBlock


class AlgorithmFactory:
    factory = {
        "motionblock": MotionBlock
    }

    @staticmethod
    def create(name, data):
        return AlgorithmFactory.factory.get(name)(data)
