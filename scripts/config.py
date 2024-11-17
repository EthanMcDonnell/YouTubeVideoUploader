import toml


class Config:
    _instance = None
    file_path = "config.toml"

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

    def get(self, heading, sub_key):
        """Get a value from the configuration using heading and sub-key."""
        return self.config.get(heading, {}).get(sub_key, None)
