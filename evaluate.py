import operator
import json

class Evaluation():
    def __init__(self, field, value, operator_str):

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

    def evaluate(self, payload, level=0, verbose=True):
        
        field_value_ = payload[self.field_]
        
        if verbose:
            tabs = "\t" * level
            print(tabs + f"Evaluating {field_value_} {self.op_str_} {self.value_}")
        
        result = self.func_(field_value_, self.value_)
        if verbose: print(tabs + f"Evaluation Result: {result}")
        
        return result

class Composite():
    def __init__(self, children, conjuction='AND'):
        
        if conjuction not in ['AND', 'OR']:
            raise ValueError('Conjuction must be a valid value.')

        if not isinstance(children, list):
            raise ValueError('Children must be a list, empty or otherwise.')
        
        self.conjuction_ = conjuction
        self.children_ = children

    def evaluate(self, payload, level=0, verbose=True):

        if self.conjuction_ == 'AND':
            result = True
            i = 0
            while result and (i < len(self.children_)):
                
                if verbose:
                    tabs = "\t" * level
                    if i > 0: print("\n" + tabs + f"{self.conjuction_} \n")
                    print(tabs + f"Evaluating Composite: {i + 1}, Level: {level + 1}")
                
                result = self.children_[i].evaluate(payload, level + 1, verbose=verbose)
                i += 1

        else:
            result = False
            i = 0
            while result == False and (i < len(self.children_)):
                
                if verbose:
                    tabs = "\t" * level
                    if i > 0: print("\n" + tabs + f"{self.conjuction_} \n")
                    print(tabs + f"Evaluating Composite: {i + 1}, Level: {level + 1}")
                
                result = self.children_[i].evaluate(payload, level + 1, verbose=verbose)
                i += 1

        if verbose: 
            tabs = "\t" * level
            print("\n" + tabs + f"Composite Result: {result}")

        return result

class JSONEvaluationEngine():
    
    def __init__(self, json_path, verbose=True):
        with open(json_path) as f:
            self.json_ = json.load(f)

        self.composite_ = self.build_engine(self.json_)

    def build_engine(self, children, verbose=True):
        comp_children = []
        if verbose: print(f"calling build_engine with {children}")
        for child in children:
            if child.get('field'):
                comp_children.append(Evaluation(child['field'], child['value'], child['operator']))
            else:
                new_children = child.get('children')
                conj = child.get('conjuction')
                return Composite(self.build_engine(new_children), conjuction=conj)
    
        return comp_children

    def evaluate(self, payload, verbose=True):
        return self.composite_.evaluate(payload, verbose=verbose)


eng = JSONEvaluationEngine("evaluate.json")


payload_test = {
    "RecallDate": "NULL",
    "DaysSincePlacement": 75
}

payload_test_2 = {
    "RecallDate": "NULL",
    "DaysSincePlacement": 31
}

eng.evaluate(payload_test_2, verbose=True)