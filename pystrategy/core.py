import operator
import json
from .operators import between, not_between, not_contains, in_, not_in, re_contains

class Evaluation():
    """The simplest logical unit in an evaluation.

    Attributes:
        func_ (function): comparison operator function
        field_ (str): name of field where field_value resides in evaluation payload.
        value_ (str/float): value to compare to field_value
        op_str_ (str): string representation of comparison operator
    """

    def __init__(self, field, value, operator_str):

        operators = {
            "lt": operator.lt,
            "le": operator.le,
            "eq": operator.eq,
            "ne": operator.ne,
            "ge": operator.ge,
            "gt": operator.gt,
            "contains": operator.contains,
            "not contains": not_contains,
            "in": in_,
            "not in": not_in,
            "regex match": re_contains,
            "between": between,
            "not between": not_between
        }

        if operator_str not in operators.keys():
            raise ValueError(f"Operator must be a valid value. '{operator_str}' is not valid. Valid operators are: {list(operators.keys())}")

        self.func_ = operators[operator_str] # functions are first class objects and can be passed around
        self.field_ = field
        self.value_ = value
        self.op_str_ = operator_str

    def evaluate(self, payload, level=0, verbose=True):
        """Evaluate a payload against this Evaluation.

        Args:
            payload (dict): dictionary containing the data to evaluate.
            level (int): represents the level of deepness in the evaluation hierarchy
            verbose (bool): whether to print results
        
        Returns:
            result (bool): T/F of evaluation
        """
        # find the value to compare in the payload dict
        field_value_ = payload.get(self.field_)
        if not field_value_:
            raise ValueError(f"Required field '{self.field_}' not in payload.")
        
        if verbose:
            tabs = "\t" * level
            print(tabs + f"Evaluating {self.field_}: {field_value_} {self.op_str_} {self.value_}")
        
        # run the comparison operation based on the initialzed operator
        result = self.func_(field_value_, self.value_)
        if verbose: print(tabs + f"Evaluation Result: {result}")
        
        return result

class Composite():
    """A logical composite made of children evaluations joined by logical
    OR or AND or NOR or XOR or NAND (conjunction). Children evaluations can be Composites
    or Evaluations.

    Attributes:
        conjunction_ (str): Logical AND or OR or NOR or XOR or NAND
        children_ (list): list of logical children
    """

    def __init__(self, children, conjunction='AND'):
        
        valid_conjunctions = ['AND', 'OR', 'NOR', 'XOR', 'NAND']
        if conjunction not in valid_conjunctions:
            raise ValueError(f"conjunction must be a valid value. '{conjunction}' is not valid. Valid conjunctions are: {valid_conjunctions}.")

        if not isinstance(children, list):
            raise ValueError('Children must be a list, empty or otherwise.')
        
        self.conjunction_ = conjunction
        self.children_ = children

    def evaluate(self, payload, level=0, verbose=True):
        """Evaluate a payload against the Composite's logic

        Args:
            payload (dict): dictionary containing the data to evaluate.
            level (int): represents the level of deepness in the evaluation hierarchy
            verbose (bool): whether to print results

        Returns:
            result (bool): T/F of the composite logical evaluation
        """

        # if children are joined by AND, evaluate every child until all children
        # are evaluated or until a False breaks the loop (Need all True for AND)
        if self.conjunction_ in ['AND', 'NAND']:
            result = True
            i = 0
            while result and (i < len(self.children_)):
                
                if verbose:
                    tabs = "\t" * level
                    if i > 0: print("\n" + tabs + f"{self.conjunction_} \n")
                    print(tabs + f"Evaluating Composite: {i + 1}, Level: {level + 1}")
                
                result = self.children_[i].evaluate(payload, level + 1, verbose=verbose)
                i += 1
            if self.conjunction_ == 'NAND':
                result = not result


        # if children are joined by OR, evaluate every child until all children
        # are evaluated or until a True breaks the loop (only need 1 True for OR)
        elif self.conjunction_ in ['OR', 'NOR']:
            result = False
            i = 0
            while result == False and (i < len(self.children_)):
                
                if verbose:
                    tabs = "\t" * level
                    if i > 0: print("\n" + tabs + f"{self.conjunction_} \n")
                    print(tabs + f"Evaluating Composite: {i + 1}, Level: {level + 1}")
                
                result = self.children_[i].evaluate(payload, level + 1, verbose=verbose)
                i += 1
            if self.conjunction_ == 'NOR':
                result = not result

        # XOR evaluation - 1 and only 1 can be True. Have to iterate over all children unless the number of trues becomes greater than 1
        else:
            i = 0
            true_count = 0
            while true_count < 2 and (i < len(self.children_)):
                if verbose:
                    tabs = "\t" * level
                    if i > 0: print("\n" + tabs + f"{self.conjunction_} \n")
                    print(tabs + f"Evaluating Composite: {i + 1}, Level: {level + 1}")
                    
                # += a boolean is equivalent to += 1 for T and += 0 for False
                true_count += self.children_[i].evaluate(payload, level + 1, verbose=verbose)
                i += 1

            if true_count == 1:
                result = True
            else:
                result = False

        if verbose: 
            tabs = "\t" * level
            print("\n" + tabs + f"Composite Result: {result}")

        return result

class JSONEvaluationEngine():
    """Engine builds the logical components from a properly formatted
        JSON backend.
        evaluate() method is implemented for prebuilt engines, and 
        dynamic_evaluate() method is implemented for engines that receive both payload and JSON in the 
        same call.
    
    Attributes:
        prebuilt_ (bool): indicates whether engine is prebuilt or dynamic
        composite_ (Composite): master composite of all logical components, if prebuilt
    
    """

    def __init__(self, json_path=None, verbose=True):
        """Initializes the engine instance. Engine can be prebuilt, offering evaluation
        based on a particular JSON backend, or can be dynamic, building new logical components
        with each call.

        Args:
            prebuilt (bool): whether to prebuild engine with JSON backend
            json_path (str): path to JSON backend, optional
            verbose (bool): whether to print intermediate steps of composite build.
        
        Returns:
            None
        """

        if json_path:
            self.composite_ = self.build_engine_from_json(json_path=json_path, verbose=verbose)
            self.prebuilt_ = True
        else:
            self.prebuilt_ = False

    def build_engine_from_json(self, json_path, verbose=True):
        """Constructs the logical components of the engine from JSON file

        Args:
            json_path (str): path to JSON backend
            verbose (bool): whether to print intermediate steps of composite build.
        
        Returns:
            None
        """
        # TODO JSON schema validation 

        with open(json_path) as f:
            json_ = json.load(f)

        first_children = json_['children']
        first_conj = json_['conjunction']

        composite_ = self.build_engine(children=first_children, conjunction=first_conj, verbose=verbose)

        return composite_

    def build_engine(self, children, conjunction, verbose=True):
        """Recursively joins all logical components into a master composite.

        Args:
            children (list): list of logical children, either Evaluations or Composites.
            conjunction (str): one of {'AND', 'OR', 'NOR', 'XOR', 'NAND'} - how to logically join children.
            verbose (bool): whether to print intermediate steps of composite build.

        Returns:
            composite (Composite): composite of logical children.
        """
        comp_children = []
        if verbose: print(f"\nCalling build_engine with {children}")
        for child in children:        
            if child.get('field'):
                comp_children.append(Evaluation(child['field'], child['value'], child['operator']))
                #print(comp_children)
            else:
                new_children = child.get('children')
                conj = child.get('conjunction')
                comp_children.append(self.build_engine(new_children, conjunction=conj))
    
        return Composite(comp_children, conjunction=conjunction)

    def evaluate(self, payload, verbose=True):
        """Evaluate payload data against engine logical composite

        Args:
            payload (dict): dictionary of data to be evaluated.
            verbose (bool): whether to print intermediate steps of evaluation.
        
        Returns:
            result (bool): result of logical evaluation of engine against payload
        """
        if not self.prebuilt_:
            raise AttributeError('Engine is not prebuilt. Prebuild engine or use dynamic_evaluate().')

        return self.composite_.evaluate(payload, verbose=verbose)

    def dynamic_evaluate(self, payload, json_path, verbose=True):
        """Builds the logical composite on the fly from JSON, then evaluates against payload
        
        Args:
            payload(dict): dictionary of data to be evaluated.
            verbose (bool): whether to print intermediate steps of build and evaluation
            
        Returns: 
            result (bool): result of logical evaluation of engine against payload
            
        """

        composite_ = self.build_engine_from_json(json_path=json_path, verbose=verbose)

        return composite_.evaluate(payload, verbose=verbose)


    #def pretty_print(self):
    #    pass

    #def __repr__(self):
    #    self.pretty_print()
