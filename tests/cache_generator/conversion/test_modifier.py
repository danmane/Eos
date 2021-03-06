#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2013 Anton Vorobyov
#
# This file is part of Eos.
#
# Eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Eos. If not, see <http://www.gnu.org/licenses/>.
#===============================================================================


from unittest.mock import patch

from eos.tests.cache_generator.generator_testcase import GeneratorTestCase
from eos.tests.environment import Logger


@patch('eos.data.cache_generator.converter.ModifierBuilder')
class TestConversionModifier(GeneratorTestCase):
    """
    As modifiers generated by modifier builder have custom
    processing in converter, we have to test it too.
    """

    def test_fields(self, mod_builder):
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 1,
                                           'postExpression': 11, 'effectCategory': 111})
        mod = self.mod(state=2, context=3, source_attribute_id=4, operator=5,
                       target_attribute_id=6, location=7, filter_type=8, filter_value=9)
        mod_builder.return_value.build_effect.return_value = ([mod], 0)
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 1)
        self.assertIn(1, data['modifiers'])
        expected = {'modifier_id': 1, 'state': 2, 'context': 3, 'source_attribute_id': 4, 'operator': 5,
                    'target_attribute_id': 6, 'location': 7, 'filter_type': 8, 'filter_value': 9}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])

    def test_numbering_single_effect(self, mod_builder):
        # Check how multiple modifiers generated out of single effect are numbered
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 21,
                                           'postExpression': 21, 'effectCategory': 21})
        mod1 = self.mod(state=20, context=30, source_attribute_id=40, operator=50,
                        target_attribute_id=60, location=70, filter_type=80, filter_value=90)
        mod2 = self.mod(state=200, context=300, source_attribute_id=400, operator=500,
                        target_attribute_id=600, location=700, filter_type=800, filter_value=900)
        mod_builder.return_value.build_effect.return_value = ([mod1, mod2], 0)
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 2)
        self.assertIn(1, data['modifiers'])
        expected = {'modifier_id': 1, 'state': 20, 'context': 30, 'source_attribute_id': 40, 'operator': 50,
                    'target_attribute_id': 60, 'location': 70, 'filter_type': 80, 'filter_value': 90}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(2, data['modifiers'])
        expected = {'modifier_id': 2, 'state': 200, 'context': 300, 'source_attribute_id': 400, 'operator': 500,
                    'target_attribute_id': 600, 'location': 700, 'filter_type': 800, 'filter_value': 900}
        self.assertEqual(data['modifiers'][2], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(sorted(modifiers), [1, 2])

    def test_numbering_multiple_effects(self, mod_builder):
        # Check how multiple modifiers generated out of two effects are numbered
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 222})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 1,
                                           'postExpression': 11, 'effectCategory': 111})
        self.dh.data['dgmeffects'].append({'effectID': 222, 'preExpression': 111,
                                           'postExpression': 1, 'effectCategory': 111})
        mod1 = self.mod(state=2, context=3, source_attribute_id=4, operator=5,
                        target_attribute_id=6, location=7, filter_type=8, filter_value=9)
        mod2 = self.mod(state=22, context=33, source_attribute_id=44, operator=55,
                        target_attribute_id=66, location=77, filter_type=88, filter_value=99)
        arg_map = {(1, 11, 111): mod1, (111, 1, 111): mod2}
        mod_builder.return_value.build_effect.side_effect = lambda pre, post, cat: ([arg_map[(pre, post, cat)]], 0)
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 2)
        self.assertIn(1, data['modifiers'])
        expected = {'modifier_id': 1, 'state': 2, 'context': 3, 'source_attribute_id': 4, 'operator': 5,
                    'target_attribute_id': 6, 'location': 7, 'filter_type': 8, 'filter_value': 9}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(2, data['modifiers'])
        expected = {'modifier_id': 2, 'state': 22, 'context': 33, 'source_attribute_id': 44, 'operator': 55,
                    'target_attribute_id': 66, 'location': 77, 'filter_type': 88, 'filter_value': 99}
        self.assertEqual(data['modifiers'][2], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])
        self.assertIn(222, data['effects'])
        modifiers = data['effects'][222]['modifiers']
        self.assertEqual(modifiers, [2])

    def test_merge_signle_effect(self, mod_builder):
        # Check that if modifiers with the same values are generated on single effect,
        # they're assigned to single identifier and it is listed twice in list of
        # modifiers
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 22,
                                           'postExpression': 22, 'effectCategory': 22})
        mod1 = self.mod(state=32, context=43, source_attribute_id=54, operator=65,
                        target_attribute_id=76, location=87, filter_type=98, filter_value=90)
        mod2 = self.mod(state=32, context=43, source_attribute_id=54, operator=65,
                        target_attribute_id=76, location=87, filter_type=98, filter_value=90)
        mod_builder.return_value.build_effect.return_value = ([mod1, mod2], 0)
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 1)
        self.assertIn(1, data['modifiers'])
        expected = {'modifier_id': 1, 'state': 32, 'context': 43, 'source_attribute_id': 54, 'operator': 65,
                    'target_attribute_id': 76, 'location': 87, 'filter_type': 98, 'filter_value': 90}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1, 1])

    def test_merge_multiple_effects(self, mod_builder):
        # Check that if modifiers with the same values are generated on multiple effects,
        # they're assigned to single identifier
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 222})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 1,
                                           'postExpression': 11, 'effectCategory': 111})
        self.dh.data['dgmeffects'].append({'effectID': 222, 'preExpression': 111,
                                           'postExpression': 11, 'effectCategory': 1})
        mod1 = self.mod(state=2, context=3, source_attribute_id=4, operator=5,
                        target_attribute_id=6, location=7, filter_type=8, filter_value=9)
        mod2 = self.mod(state=2, context=3, source_attribute_id=4, operator=5,
                        target_attribute_id=6, location=7, filter_type=8, filter_value=9)
        arg_map = {(1, 11, 111): mod1, (111, 11, 1): mod2}
        mod_builder.return_value.build_effect.side_effect = lambda pre, post, cat: ([arg_map[(pre, post, cat)]], 0)
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['modifiers']), 1)
        self.assertIn(1, data['modifiers'])
        expected = {'modifier_id': 1, 'state': 2, 'context': 3, 'source_attribute_id': 4, 'operator': 5,
                    'target_attribute_id': 6, 'location': 7, 'filter_type': 8, 'filter_value': 9}
        self.assertEqual(data['modifiers'][1], expected)
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])
        self.assertIn(111, data['effects'])
        modifiers = data['effects'][111]['modifiers']
        self.assertEqual(modifiers, [1])
        self.assertIn(222, data['effects'])
        modifiers = data['effects'][222]['modifiers']
        self.assertEqual(modifiers, [1])

    def test_builder_usage(self, mod_builder):
        # Check that modifier builder is properly used
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 111})
        self.dh.data['dgmeffects'].append({'effectID': 111, 'preExpression': 56,
                                           'postExpression': 107, 'effectCategory': 108})
        self.dh.data['dgmexpressions'].append({'expressionID': 107, 'operandID': None, 'arg1': None, 'arg2': None,
                                               'expressionValue': None, 'expressionTypeID': None,
                                               'expressionGroupID': None, 'expressionAttributeID': None})
        self.dh.data['dgmexpressions'].append({'expressionID': 56, 'operandID': None, 'arg1': None, 'arg2': None,
                                               'expressionValue': None, 'expressionTypeID': None,
                                               'expressionGroupID': None, 'expressionAttributeID': None})
        mod_builder.return_value.build_effect.return_value = ([], 0)
        self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        call1, call2 = mod_builder.mock_calls
        # Check initialization
        name, args, kwargs = call1
        self.assertEqual(name, '')
        self.assertEqual(len(args), 2)
        self.assertEqual(len(kwargs), 0)
        expressions, logger = args
        # Expression order isn't stable in passed list, so verify
        # passed argument using membership check
        self.assertEqual(len(expressions), 2)
        expression_ids = set(row['expressionID'] for row in expressions)
        self.assertEqual(expression_ids, {56, 107})
        self.assertTrue(isinstance(logger, Logger))
        # Check request for building
        name, args, kwargs = call2
        self.assertEqual(name, '().build_effect')
        self.assertEqual(args, (56, 107, 108))
        self.assertEqual(len(kwargs), 0)
