from epd_2in9_b import EPD_2in9_B, EPD_WIDTH, EPD_HEIGHT
import framebuf


class LandscapeEPD(EPD_2in9_B):
    def __init__(self):
        super().__init__()
        self.lwidth = EPD_HEIGHT
        self.lheight = EPD_WIDTH

        self.buffer_black_l = bytearray(self.lheight * self.lwidth // 8)
        self.buffer_red_l = bytearray(self.lheight * self.lwidth // 8)
        self.imageblack_l = framebuf.FrameBuffer(self.buffer_black_l, self.lwidth, self.lheight, framebuf.MONO_HLSB)
        self.imagered_l = framebuf.FrameBuffer(self.buffer_red_l, self.lwidth, self.lheight, framebuf.MONO_HLSB)

    def _rotate_90(self):
        for x in range(self.lwidth):
            for y in range(self.lheight):
                bpixel = self.imageblack_l.pixel(x, y)
                rpixel = self.imagered_l.pixel(x, y)
                # 90° clockwise transform
                new_x = (self.lheight - 1) - y
                new_y = x
                self.imageblack.pixel(new_x, new_y, bpixel)
                self.imagered.pixel(new_x, new_y, rpixel)

    def display(self):
        self._rotate_90()
        super().display()

