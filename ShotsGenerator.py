
import time
"""
A demo generate shots based on histogram similarity.
Run costs 2.5 minutes.
"""

FPS = 30
GUARDIAN_SEC_BUFFER = 5


class ShotsGenerator:
    def __init__(self, data, threshold):
        self.threshold = threshold
        self.data = data
        self.rgb_frames = [frame.bgr for frame in self.data]
        self.width = self.data.width
        self.height = self.data.height

    def get_break_points(self):
        """
        Calculate video break points.
        The frames between each neighbouring
        break points is a shot.
        :return: A list contains break points.
        """
        print('------running get_mask------')
        breaks = []
        frame_count = self.data.frame_count
        prev_histogram = self._frame2rgb_histogram(0)
        breaks += [0]

        compare_hist = 3  # Compare every compare_hist of frames' histogram similarity
        till_compare_hist = 0  # A pointer denote how many frames have been passed not compare
        past_break = 0  # How many frames left to be able to add a break point
        for i in range(1, frame_count-1):
            if till_compare_hist == compare_hist:
                start = time.time()
                next_histogram = self._frame2rgb_histogram(i)
                val = self._histo_diff(prev_histogram, next_histogram)/(self.width*self.height)
                end = time.time()
                # print(end - start)
                val *= 100
                # print(val)
                if val > self.threshold and past_break <= 0 and val < 100:
                    breaks += [i]
                    past_break = FPS * GUARDIAN_SEC_BUFFER

                prev_histogram = next_histogram
                till_compare_hist = 0

            past_break -= 1
            till_compare_hist += 1

        breaks += [frame_count]
        print(breaks)
        return breaks

    def _frame2rgb_histogram(self, idx):
        """
        Convert frame with given index to
        rgb histogram.
        Divide 255 into four level, only
        value left two most significant bits
        so divide by 64.
        :param idx: A index indicates a frame in acquired data of frames
        :return: An (4, 4, 4) shape histogram indicates rgb distribution in this given frame.
        """
        # print('------running _frame2rgb_histogram------')
        # print('idx is '+str(idx))
        histogram = [[[0]*4]*4 for i in range(4)]
        rgb_frame = self.rgb_frames[idx].tolist()  #  Convert type to list cuz list access is 10 times faster than np.array
        for x in range(self.height):
            for y in range(self.width):
                b = rgb_frame[x][y][0]
                g = rgb_frame[x][y][1]
                r = rgb_frame[x][y][2]
                histogram[r//64][g//64][b//64] += 1
        return histogram

    def _histo_diff(self, prev, next):
        """
        Caculate total difference between two frame histograms.
        :param prev: Previous histogram
        :param next: The next histogram of previous one
        :return: The total sum of in position difference between two histograms
        """
        # print('------running _histo_diff------')
        total_diff = 0
        for i in range(4):
            for j in range(4):
                for k in range(4):
                    total_diff += abs(prev[i][j][k] - next[i][j][k])
        return total_diff
