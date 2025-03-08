from power_ctrl_2040 import PowerCtrl

class BinPowerCtrl(PowerCtrl):
    def __init__(self):
        super().__init__()
        self.disable_while_sleeping_all_but(
            # TIMER is required so time.sleep_ms and Timer  work
            self.EN1_CLK_SYS_TIMER,
            # USB enabled for using Thonny
            self.EN1_CLK_USB_USBCTRL,
            self.EN1_CLK_SYS_USBCTRL,
            self.EN0_CLK_SYS_PLL_USB
            # everything else is disabled while sleeping.
        )

        self.disable_while_awake(
            # These are blocks I know I don't need
            # Quick note: DMA is used to talk to the WIFI chip.
            # On PICO W the system LED is connected to the WIFI chip.
            self.EN0_CLK_SYS_SPI1,
            self.EN0_CLK_PERI_SPI1,
            self.EN0_CLK_SYS_SPI0,
            self.EN0_CLK_PERI_SPI0,
            self.EN0_CLK_SYS_I2C1,
            self.EN0_CLK_SYS_I2C0,
            self.EN0_CLK_SYS_PWM,
            self.EN0_CLK_SYS_PIO0,
            self.EN0_CLK_SYS_PADS,
            self.EN0_CLK_SYS_JTAG,
            self.EN0_CLK_SYS_ADC,
            self.EN0_CLK_ADC_ADC,
            self.EN1_CLK_SYS_UART1,
            self.EN1_CLK_PERI_UART1,
            self.EN1_CLK_SYS_UART0,
            self.EN1_CLK_PERI_UART0,
            self.EN1_CLK_SYS_WATCHDOG,
            self.EN1_CLK_SYS_TBMAN
        )
