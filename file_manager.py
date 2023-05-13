import json
import logging


class FileManager():

    def __init__(self) -> None:
        logging.basicConfig(filename='file_manager.log', level=logging.DEBUG,
                            format='%(asctime)s:%(levelname)s:%(message)s')
        self._are_settings_loaded = False
        self._settings_path = ""
        self._hash = ""
        self._bin = ""
        self._last_symbols = ""
        self._output_path = ""
        self._card_number_path = ""
        self._plot_img_path = ""
        self._time_statistic_path = ""

    def write_output(self, text: str) -> None:
        """Writes output to a .txt file
        """
        try:
            with open(self._output_path, "w") as file:
                file.write(text)
        except Exception as e:
            logging.exception(f'Exception: {e}')
            raise e

    def load_text(self, path: str) -> str:
        """Reads text from file
        Args:
            path (str): path to file

        Returns:
            str: text from file
        """
        try:
            with open(path, "r") as file:
                result = file.read()
            return result
        except Exception as e:
            logging.exception(f'Exception: {e}')
            raise e

    @property
    def are_settings_loaded(self) -> bool:
        return self._are_settings_loaded

    @property
    def settings_path(self) -> str:
        return self._settings_path

    @settings_path.setter
    def settings_path(self, new_value):
        self._settings_path = new_value
        self._are_settings_loaded = True
        self.load_settings()

    @property
    def hash(self):
        return self._hash

    @property
    def bin(self):
        return self._bin

    @property
    def last_symbols(self):
        return self._last_symbols

    @property
    def output_path(self):
        return self._output_path

    @property
    def card_number_path(self):
        return self._card_number_path

    @property
    def plot_img_path(self):
        return self._plot_img_path

    @property
    def time_statistic_path(self):
        return self._time_statistic_path

    def load_settings(self):
        """Loads settings dictionary from .json file
        """
        try:
            with open(self._settings_path, "r") as file:
                data = json.load(file)
                self._hash = self.load_text(data["hash"])
                self._bin = self.load_text(data["bin"])
                self._last_symbols = self.load_text(data["last_symbols"])
                self._output_path = data["output"]
                self._card_number_path = data["card_number"]
                self._plot_img_path = data["plot_img"]
                self._time_statistic_path = data["time_statistic"]
        except Exception as e:
            logging.exception(f'Exception: {e}')
            raise e
