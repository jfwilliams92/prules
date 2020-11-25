A simple implementation of a rules engine with a JSON backend.
Inspired by huttotw's <a href="https://github.com/huttotw/grules"> grules </a>

Example:

```
json_path = "./tests/test_config.json"
eng = JsonEvaluationEngine(json_path)

payload_test = {
    "RecallDate": "NULL",
    "DaysSincePlacement": 75,
    "MoneyInTheBank": 509.0,
    "DaysTillPayDay": 22,
    "OffersSent": ["PayDaySpecial", "AARP Discount"],
    "DaysBeforeBirthday": 10,
    "TimeSinceLastDiscountOffer": 23
}

eng.evaluate(payload_test)
```

Output:
```
Evaluating Child 1, Level 1 - Composite
	Evaluating Child 1, Level 2 - Evaluation
		Evaluating DaysSincePlacement: 75 le 31
		Evaluation Result: False

	OR 

	Evaluating Child 2, Level 2 - Evaluation
		Evaluating MoneyInTheBank: 509.0 ge 500.0
		Evaluation Result: True

	Composite Result: True

AND 

Evaluating Child 2, Level 1 - Evaluation
	Evaluating RecallDate: NULL eq NULL
	Evaluation Result: True

AND 

Evaluating Child 3, Level 1 - Evaluation
	Evaluating DaysTillPayDay: 22 between [21, 55]
	Evaluation Result: True

AND 

Evaluating Child 4, Level 1 - Evaluation
	Evaluating OffersSent: ['PayDaySpecial', 'AARP Discount'] not contains 10 OFF
	Evaluation Result: True

AND 

Evaluating Child 5, Level 1 - Composite
	Evaluating Child 1, Level 2 - Evaluation
		Evaluating DaysBeforeBirthday: 10 in [1, 2, 6, 9, 22]
		Evaluation Result: False

	XOR 

	Evaluating Child 2, Level 2 - Evaluation
		Evaluating TimeSinceLastDiscountOffer: 23 not in [1, 2, 3, 4, 5]
		Evaluation Result: True

	XOR 

	Evaluating Child 3, Level 2 - Evaluation
		Evaluating DaysSincePlacement: 75 between [12, 78]
		Evaluation Result: True

	Composite Result: False

Composite Result: False
False
```