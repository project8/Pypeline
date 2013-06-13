'''
    Classes related to building scripts and/or script GUIs will go here
'''

class _fake_guiVar:
    def __init__(self, value=False):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value

class _fake_BooleanVar:
    def __init__(self, value=False):
        self.value = value

    def get(self):
        return (self.value is True)

    def set(self, value):
        self.value = (value is True)

class _fake_StingVar:
    def __init__(self, value=''):
        self.value = value

    def get(self):
        return str(self.value)

    def set(self, value):
        self.value = str(value)

class _fake_IntVar:
    def __init__(self, value=''):
        self.value = value

    def get(self):
        return int(self.value)

    def set(self, value):
        self.value = int(value)

class _fake_DoubleVar:
    def __init__(self, value=''):
        self.value = value

    def get(self):
        return float(self.value)

    def set(self, value):
        self.value = float(value)
