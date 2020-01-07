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
#prints True
```