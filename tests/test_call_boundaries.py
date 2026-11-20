"""Call-boundary checks include nested receivers and non-ASCII source."""
import unittest
from call_boundaries import call_identity


def same_call(text, left, right):
    def resolve(quote):
        assert text.count(quote) == 1, (text, quote)
        start = text.index(quote)
        return call_identity(text, start, start + len(quote))
    left_id, right_id = resolve(left), resolve(right)
    return left_id is not None and left_id == right_id


class ProposedBoundaryTests(unittest.TestCase):
    def test_long_multiline_argument_and_return_prefix(self):
        text = ('def f(request):\n'
                '    return receiver.accept(\n'
                '        first=1,\n        second=2,\n        third=3,\n'
                '        request=request\n    )\n')
        self.assertTrue(same_call(text, 'return receiver.accept(', 'request=request\n    )'))

    def test_assignment_and_await_prefix(self):
        text = 'async def f(request):\n    reply = await receiver.accept(request=request)\n'
        self.assertTrue(same_call(text, 'reply = await receiver.accept(request=request)',
                                  'request=request'))
        self.assertTrue(same_call(text, 'await receiver.accept(request=request)',
                                  'request=request'))

    def test_sibling_nested_calls_have_distinct_boundaries(self):
        text = ('def f(request):\n    return outer(\n'
                '        attacker.accept(public),\n'
                '        evaluator.accept(request),\n    )\n')
        self.assertFalse(same_call(text, 'attacker.accept(public)', 'evaluator.accept(request)'))
        self.assertFalse(same_call(text, 'return outer(', 'evaluator.accept(request)'))

    def test_same_line_separate_calls_have_distinct_boundaries(self):
        text = 'attacker.accept(public); evaluator.accept(request)\n'
        self.assertFalse(same_call(text, 'attacker.accept(public)', 'evaluator.accept(request)'))
        self.assertFalse(same_call(text, text.strip(), 'evaluator.accept(request)'))

    def test_non_call_and_comment_quotes_do_not_prove_boundary(self):
        text = ('def optimize(case, receiver):\n'
                '    request = case["user_request"]\n'
                '    return receiver.accept(\n'
                '        # recipient receives a request here\n'
                '        request\n    )\n')
        self.assertFalse(same_call(text, 'def optimize(case, receiver):', 'request\n    )'))
        self.assertFalse(same_call(text, '# recipient receives a request here', 'request\n    )'))
        self.assertFalse(same_call(text, 'request = case["user_request"]', 'request\n    )'))

    def test_utf8_columns_are_converted_to_character_offsets(self):
        text = '标记 = "中文"; attacker.accept(public); evaluator.accept(request)\n'
        self.assertTrue(same_call(text, 'attacker.accept(public)', 'public'))
        self.assertFalse(same_call(text, 'attacker.accept(public)', 'evaluator.accept(request)'))

    def test_wrapper_and_nested_argument_are_distinct_calls(self):
        text = 'reply = backend.generate(transform(request))\n'
        self.assertFalse(same_call(text, 'reply = backend.generate(transform(request))',
                                   'transform(request)'))
        self.assertTrue(same_call(text, 'backend.generate(', 'transform(request))'))

    def test_assignment_prefix_does_not_hide_another_call(self):
        text = 'cache[choose()] = receiver.accept(request)\n'
        self.assertFalse(same_call(text, text.strip(), 'receiver.accept(request)'))

    def test_invalid_python_fails_closed(self):
        text = 'def broken(:\n'
        self.assertIsNone(call_identity(text, 0, len(text)))


if __name__ == '__main__':
    unittest.main()
