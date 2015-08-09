import json
import unittest
import subprocess
import tempfile


class BinSchemaInferer(unittest.TestCase):
    def test_end_to_end_simple_run(self):
        # given:
        _, filename = tempfile.mkstemp()
        with open(filename, 'w') as f:
            f.write('{"one": "two"}')

        expected = {
            "$schema": "http://json-schema.org/draft-04/schema",
            "required": [
                "one"
            ],
            "type": "object",
            "properties": {
                "one": {
                    "type": "string"
                }
            }
        }

        # when:
        output = subprocess.check_output(['schema_inferer', filename])
        # then:
        self.assertEqual(expected, json.loads(output))
