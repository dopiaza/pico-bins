import os
import time


class Logger:
    def __init__(self, log_file="debug.log", max_size=10_000, backup_file="debug_old.log"):
        """
        Logger for writing debug logs to a file.

        :param log_file: Name of the primary log file.
        :param max_size: Maximum size of log file before rollover (in bytes).
        :param backup_file: Backup file to store old logs.
        """
        self.log_file = log_file
        self.backup_file = backup_file
        self.max_size = max_size
        self.start_time = time.ticks_ms()  # Relative time reference

        # Ensure log file exists
        try:
            with open(self.log_file, "a") as _:
                pass
        except OSError:
            print("Error creating log file.")

    def _get_timestamp(self):
        """Returns a formatted timestamp (RTC time if available, otherwise relative time)."""
        try:
            t = time.localtime()
            return f"{t[0]:04}-{t[1]:02}-{t[2]:02} {t[3]:02}:{t[4]:02}:{t[5]:02}"
        except:
            # Use relative milliseconds if RTC is not available
            return f"{time.ticks_ms() - self.start_time}ms"

    def _check_rollover(self):
        """Checks if the log file exceeds the maximum size and rolls over if needed."""
        try:
            if os.stat(self.log_file)[6] > self.max_size:
                os.rename(self.log_file, self.backup_file)
                with open(self.log_file, "w") as f:
                    f.write("Log rolled over.\n")
        except OSError:
            pass  # Ignore errors (file may not exist initially)

    def log(self, message, level="INFO"):
        """
        Writes a log message to the file with a timestamp.

        :param message: The message to log.
        :param level: Log level (INFO, WARNING, ERROR, DEBUG).
        """
        self._check_rollover()
        timestamp = self._get_timestamp()
        log_entry = f"[{timestamp}] [{level}] {message}\n"

        print(log_entry)

        try:
            with open(self.log_file, "a") as f:
                f.write(log_entry)
                f.flush()  # Ensure data is written immediately
        except OSError as e:
            print(f"Logging error: {e}")

    def clear_logs(self):
        """Clears the log file."""
        try:
            with open(self.log_file, "w") as f:
                f.write("Log cleared.\n")
        except OSError as e:
            print(f"Error clearing log: {e}")

# Example usage:
# logger = PicoLogger()
# logger.log("System initialized")
# logger.log("Something went wrong", level="ERROR")
# logger.clear_logs()