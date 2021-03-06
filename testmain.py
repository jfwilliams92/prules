# run interactively

def main():
    from pystrategy import *
    import json 
    json_path = "./tests/test_config.json"
    with open(json_path) as f:
        json1 = json.load(f)

    eng = JsonEvaluationEngine(json1)

    payload_test = {
        "RecallDate": "1/20/2022",
        "DaysSincePlacement": 75,
        "MoneyInTheBank": 509.0,
        "DaysTillPayDay": 22,
        "OffersSent": ["PayDaySpecial", "AARP Discount"],
        "DaysBeforeBirthday": 10,
        "TimeSinceLastDiscountOffer": {
            "OfferSent": "YahBoy",
            "LastSent": "2020-01-02",
            "DaysSince": 200
        }
    }

    rez = eng.evaluate(payload_test)

    # should fail due to invalid operator
    json_path2 = "./tests/test_config2.json"
    with open(json_path2) as f:
        json2 = json.load(f)
    eng2 = JsonEvaluationEngine(json2)

    # even a single evaluation is a composite of length one.
    json_path3 = "./tests/test_config3.json"
    with open(json_path3) as f:
        json3 = json.load(f)
    eng3 = JsonEvaluationEngine(json3)
    eng3.evaluate(payload_test)

    # remove required field, should fail evaluation
    _ = payload_test.pop("TimeSinceLastDiscountOffer", None)
    eng.evaluate(payload_test)

main()

