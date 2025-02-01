from landscape_epd import LandscapeEPD
import time

class BinDisplay:

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    def day_with_suffix(self, mday: int) -> str:
        suffix = (
            "th" if 11 <= mday % 100 <= 13 else
            "st" if mday % 10 == 1 else
            "nd" if mday % 10 == 2 else
            "rd" if mday % 10 == 3 else
            "th"
        )

        return str(mday) + suffix

    def bins(self, bins):
        self.init_display()

        x = 0
        y = 0

        bin_width = self.epd.lwidth // len(bins)

        for bin in bins:
            (name, year, month, mday, is_next) = bin
            text = f"{self.day_with_suffix(mday)} {self.months[month - 1]}"
            if is_next:
                self.epd.imagered_l.fill_rect(x, y, bin_width, 40, 0x00)
                self.epd.imagered_l.text(name, x + 10, y + 15, 0xff)
            else:
                self.epd.imageblack_l.fill_rect(x, y, bin_width, 40, 0x00)
                self.epd.imageblack_l.text(name, x + 10, y + 15, 0xff)

            self.epd.imageblack_l.text(text, x, y + 60, 0x00)

            x += bin_width

        (year, month, mday, hour, minute, second, weekday, yearday) = time.localtime()
        text = f"Last updated: {hour:02d}:{minute:02d}:{second:02d} {self.day_with_suffix(mday)} {self.months[month - 1]} {year}"
        self.epd.imageblack_l.text(text, 0, self.epd.lheight - 8, 0x00)

        self.epd.display()

        self.sleep()

    def sleep(self):
        self.epd.delay_ms(2000)
        print("sleep")
        self.epd.sleep()

    def init_display(self):
        self.epd = LandscapeEPD()
        self.epd.Clear(0xff, 0xff)
        self.epd.imageblack_l.fill(0xff)
        self.epd.imagered_l.fill(0xff)

    def error(self, message):
        self.init_display()
        self.epd.imageblack_l.text(message, 60, self.epd.lheight // 2 - 4, 0x00)
        self.epd.display()
        self.sleep()