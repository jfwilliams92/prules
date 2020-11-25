# run interactively

import pystrategy
import json 

def main():
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

    # should fail due to invalid operator
    json_path2 = "./tests/test_config2.json"
    eng2 = JsonEvaluationEngine(json_path2)
    eng2.evaluate(payload_test)

    # even a single evaluation is a composite of length one.
    json_path3 = "./tests/test_config3.json"
    eng3 = JsonEvaluationEngine(json_path3)
    eng3.evaluate(payload_test)

    # remove required field, should fail evaluation
    _ = payload_test.pop("DaysSincePlacement", None)
    eng.evaluate(payload_test)

main()

