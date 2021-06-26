class Runtime:
    def __init__(self, logic_list):
        self._logic_list = logic_list

    def run(self):
        for logic in self._logic_list:
            print(logic.compute())
