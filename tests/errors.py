# base
class SwirlError(Exception):
    def __init__(self, ref, message) -> None:
        super().__init__()
        self.ref = ref
        self.message = message


# validation
class LengthError(SwirlError):
    def __init__(self, ref: str) -> None:
        self.ref = ref
        self.message = f'"{self.ref}" should not be longer than 30 characters!'
        super().__init__(self.ref, self.message)


class InvalidNameError(SwirlError):
    def __init__(self, ref: str) -> None:
        self.ref = ref
        self.message = f'"{self.ref}" is not a valid name!'
        super().__init__(self.ref, self.message)


class KeywordNameError(SwirlError):
    def __init__(self, ref: str) -> None:
        self.ref = ref
        self.message = f'"{self.ref}" is already used! Please use another name for this.'
        super().__init__(self.ref, self.message)


# testing
class NameAlreadyUsedError(SwirlError):
    def __init__(self, ref: str) -> None:
        self.ref = ref
        self.message = f'"{self.ref}" is already used! Please use another name for this.'
        super().__init__(self.ref, self.message)
