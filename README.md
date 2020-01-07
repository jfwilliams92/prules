A simple implementation of a rules engine with a JSON backend.

Example:

```
eng = JSONEvaluationEngine("evaluate.json")


payload_test = {
    "RecallDate": "NULL",
    "DaysSincePlacement": 75,
    "MoneyInTheBank": 509.0,
    "DaysTillPayDay": 22
}

eng.evaluate(payload_test, verbose=True)

```

Output:
```
Evaluating Composite: 1, Level: 1
	Evaluating Composite: 1, Level: 2
		Evaluating Composite: 1, Level: 3
			Evaluating 75 le 31
			Evaluation Result: False

		OR 

		Evaluating Composite: 2, Level: 3
			Evaluating 509.0 ge 500.0
			Evaluation Result: True

		Composite Result: True

	AND 

	Evaluating Composite: 2, Level: 2
		Evaluating NULL eq NULL
		Evaluation Result: True

	AND 

	Evaluating Composite: 3, Level: 2
		Evaluating 22 lt 25
		Evaluation Result: True

	Composite Result: True

Composite Result: True
True
```