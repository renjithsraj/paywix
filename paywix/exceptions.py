
class ModeException(Exception):

    def __init__(self, *args):
        self.message = f"Payment gateway expected valid mode ('test', 'live')" \
                       f" requested args: {args}"
        super().__init__(self.message)


class PaywixValidationException(Exception):

    def __init__(self, required_items, missing_items, pg, action):
        self.required_items = required_items
        self.missing_items = missing_items
        self.pg = pg
        self.action = action
        self.message = f" {self.pg} required {self.required_items} to process {self.action}" \
                       f" requested data missing: {self.missing_items}"
        super().__init__(self.message)
