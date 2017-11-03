from beep.constants import FRAME_SIZE


class AudioElement:

    def gen_frame(self):
        frame = bytearray()
        for i in range(0, FRAME_SIZE):
            frame.append(self.gen_sample())
        return bytes(frame)

    def gen_sample(self):
        pass

    def _print_bytearray(self, ba):
        print ''.join('0x{:02x}/'.format(x) for x in ba)
