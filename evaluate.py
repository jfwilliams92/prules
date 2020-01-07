import operator

class Evaluation():
    def __init__(self, field, value, operator_str, verbose=True):

        operators = {
            "lt": operator.lt,
            "le": operator.le,
            "eq": operator.eq,
            "ne": operator.ne,
            "ge": operator.ge,
            "gt": operator.gt,
            "in": operator.contains
        }

        if operator_str not in operators.keys():
            raise ValueError('Operator must be a valid value.')

        self.func_ = operators[operator_str]
        self.field_ = field
        self.value_ = value
        self.op_str_ = operator_str
        self.verbose_ = verbose

    def evaluate(self, payload, level=0):
        
        field_value_ = payload[self.field_]
        
        if self.verbose_:
            tabs = "\t" * level
            print(tabs + f"Evaluating {field_value_} {self.op_str_} {self.value_}")
        
        result = self.func_(field_value_, self.value_)
        if self.verbose_: print(tabs + f"Evaluation Result: {result}")
        
        return result


class Composite():
    def __init__(self, children, conjuction='AND', verbose=True):
        
        if conjuction not in ['AND', 'OR']:
            raise ValueError('Conjuction must be a valid value.')

        if not isinstance(children, list):
            raise ValueError('Children must be a list, empty or otherwise.')
        
        self.conjuction_ = conjuction
        self.children_ = children
        self.verbose_ = verbose

    def evaluate(self, payload, level=0):

        if self.conjuction_ == 'AND':
            result = True
            i = 0
            while result and (i < len(self.children_)):
                
                if self.verbose_:
                    tabs = "\t" * level
                    if i > 0: print("\n" + tabs + f"{self.conjuction_} \n")
                    print(tabs + f"Evaluating Composite: {i + 1}, Level: {level + 1}")
                
                result = self.children_[i].evaluate(payload, level + 1)
                i += 1

        else:
            result = False
            i = 0
            while result == False and (i < len(self.children_)):
                
                if self.verbose_:
                    tabs = "\t" * level
                    if i > 0: print("\n" + tabs + f"{self.conjuction_} \n")
                    print(tabs + f"Evaluating Composite: {i + 1}, Level: {level + 1}")
                
                result = self.children_[i].evaluate(payload, level + 1)
                i += 1

        if self.verbose_: 
            tabs = "\t" * level
            print(tabs + f"Composite Result: {result}")

        return result


# RecallDate IS NULL
eval1 = Evaluation("RecallDate", "NULL", 'eq')
# Days Since Placement >= 60
eval2 = Evaluation("DaysSincePlacement", 60, 'ge')

# OR

# RecallDate IS NOT NULL
eval3 = Evaluation("RecallDate", "NULL", 'ne')
# DaysSincePlacement >= 170
eval4 = Evaluation("DaysSincePlacement", 170, 'ge')


c1 = Composite([eval1, eval2], conjuction='AND')
c2 = Composite([eval3, eval4], conjuction='AND')

c3 = Composite([c1, c2], conjuction='OR')


payload_test = {
    "RecallDate": "NULL",
    "DaysSincePlacement": 75
}

payload_test_2 = {
    "RecallDate": "NULL",
    "DaysSincePlacement": 31
}

c3.evaluate(payload_test_2)