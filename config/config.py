import toml
import os

class Config:
    _instance = None

    # Get the absolute path to the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Safely join the directory path with the config file name
    file_path = os.path.join(script_dir, "config.toml")

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            if cls.file_path:
                cls._instance.load_config(cls.file_path)
        return cls._instance

    def load_config(self, file_path):
        """Load the TOML configuration file into a dictionary."""
        try:
            with open(file_path, 'r') as file:
                self.config = toml.load(file)
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' was not found.")
            self.config = {}
        except toml.TomlDecodeError:
            print(f"Error: Failed to parse TOML file '{file_path}'.")
            self.config = {}

    def get(self, heading, sub_key=None):
        """Get a value from the configuration using heading and sub-key."""
        if sub_key is None:
            return self.config.get(heading, {})
        return self.config.get(heading, {}).get(sub_key, None)
