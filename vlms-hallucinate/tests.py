import unittest
from tabulate import tabulate
from main import main
from parameterized import parameterized


PROTOS = [
    "protos/receipt.proto:Receipt",
    "protos/receipt_comments.proto:Receipt",
    "protos/receipt_item_comments.proto:Receipt",
    "protos/receipt_optionals.proto:Receipt",
]

MODELS = [
    # "openai",
    # "anthropic",
    "gemini",
]

TEST_RESULTS = []


class TestMainFunctions(unittest.TestCase):
    @parameterized.expand(
        [
            (proto, model, "docs/receipt-original.pdf")
            for proto in PROTOS
            for model in MODELS
        ]
    )
    def test_original_receipt(self, proto, model, file_path):
        try:
            result = main(proto, file_path, model)
            self.assertIsNotNone(result, "main() should return a non-None value")
            self.validate_receipt(result, self.get_original_receipt_data())
            TEST_RESULTS.append([model, proto, file_path, "Pass", ""])
        except Exception as e:
            TEST_RESULTS.append([model, proto, file_path, "Fail", str(e)])
            self.fail(f"main() raised {type(e).__name__} unexpectedly: {e}")

    @parameterized.expand(
        [
            (proto, model, "docs/receipt-no-tax-or-totals.pdf")
            for proto in PROTOS
            for model in MODELS
        ]
    )
    def test_no_tax_or_totals_receipt(self, proto, model, file_path):
        try:
            result = main(proto, file_path, model)
            self.assertIsNotNone(result, "main() should return a non-None value")
            self.validate_receipt(result, self.get_no_tax_or_totals_receipt_data())
            TEST_RESULTS.append([model, proto, file_path, "Pass", ""])
        except Exception as e:
            TEST_RESULTS.append([model, proto, file_path, "Fail", str(e)])
            self.fail(f"main() raised {type(e).__name__} unexpectedly: {e}")

    @parameterized.expand(
        [
            (proto, model, "docs/receipt-no-total-labels.pdf")
            for proto in PROTOS
            for model in MODELS
        ]
    )
    def test_no_total_labels_receipt(self, proto, model, file_path):
        try:
            result = main(proto, file_path, model)
            self.assertIsNotNone(result, "main() should return a non-None value")
            self.validate_receipt(result, self.get_no_tax_or_totals_receipt_data())
            TEST_RESULTS.append([model, proto, file_path, "Pass", ""])
        except Exception as e:
            TEST_RESULTS.append([model, proto, file_path, "Fail", str(e)])
            self.fail(f"main() raised {type(e).__name__} unexpectedly: {e}")

    @parameterized.expand(
        [
            (proto, model, "docs/receipt-wild-numbers.pdf")
            for proto in PROTOS
            for model in MODELS
        ]
    )
    def test_wild_numbers_receipt(self, proto, model, file_path):
        try:
            result = main(proto, file_path, model)
            self.assertIsNotNone(result, "main() should return a non-None value")
            self.validate_receipt(result, self.get_wild_numbers_receipt_data())
            TEST_RESULTS.append([model, proto, file_path, "Pass", ""])
        except Exception as e:
            TEST_RESULTS.append([model, proto, file_path, "Fail", str(e)])
            self.fail(f"main() raised {type(e).__name__} unexpectedly: {e}")

    def validate_receipt(self, result, expected_data):
        self.assertEqual(
            result.merchant.lower(),
            expected_data["merchant"].lower(),
            "Incorrect merchant name",
        )
        self.assertEqual(result.date, expected_data["date"], "Incorrect date")
        self.assertAlmostEqual(
            result.subtotal,
            expected_data["subtotal"],
            places=2,
            msg="Incorrect subtotal",
        )
        self.assertAlmostEqual(
            result.tax, expected_data["tax"], places=2, msg="Incorrect tax"
        )
        self.assertAlmostEqual(
            result.total, expected_data["total"], places=2, msg="Incorrect total"
        )

        self.assertEqual(
            len(result.line_items),
            len(expected_data["line_items"]),
            "Incorrect number of line items",
        )

        for i, (expected_item, expected_price) in enumerate(
            expected_data["line_items"]
        ):
            self.assertIn(
                expected_item,
                result.line_items[i].item,
                f"Item {i+1} does not contain '{expected_item}'",
            )
            self.assertAlmostEqual(
                result.line_items[i].price,
                expected_price,
                places=2,
                msg=f"Incorrect price for line item {i+1}",
            )

    def get_original_receipt_data(self):
        return {
            "merchant": "walmart",
            "date": "08/15/2024",
            "subtotal": 31.82,
            "tax": 2.07,
            "total": 33.89,
            "line_items": [
                ("Great Value Milk", 3.27),
                ("Bananas", 1.36),
                ("Tide Pods", 12.97),
                ("Bread Wheat", 1.88),
                ("Eggs Large", 4.23),
                ("Chicken Breast", 8.11),
            ],
        }

    def get_no_tax_or_totals_receipt_data(self):
        return {
            "merchant": "walmart",
            "date": "08/15/2024",
            "subtotal": 0.0,
            "tax": 0.0,
            "total": 0.0,
            "line_items": [
                ("Great Value Milk", 3.27),
                ("Bananas", 1.36),
                ("Tide Pods", 12.97),
                ("Bread Wheat", 1.88),
                ("Eggs Large", 4.23),
                ("Chicken Breast", 8.11),
            ],
        }

    def get_wild_numbers_receipt_data(self):
        return {
            "merchant": "walmart",
            "date": "08/15/2024",
            "subtotal": 0.0,
            "tax": 0.0,
            "total": 0.0,
            "line_items": [
                ("Moonlight Moo Juice", 34.56),
                ("Curved Yellow Happiness", 12.94),
                ("Soap Bubbles in a Box", 524.01),
                ("Yeasty Rectangle of Joy", 0.17),
                ("Hen Fruit Carton Large", 1455.99),
                ("Clucky Slices", 8.11),
            ],
        }


if __name__ == "__main__":
    unittest.main(exit=False)
    print("\nTest Results:")
    print(
        tabulate(
            TEST_RESULTS,
            headers=["Model", "Proto", "PDF", "Result", "Failure Reason"],
            tablefmt="grid",
        )
    )
