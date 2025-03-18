class ErrorContainer:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.errors = []
        return cls._instance
    def log_error(self, message):
        self.errors.append(message)
    def get_errors(self):
        return self.errors


