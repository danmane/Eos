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


class TestConversionEffect(GeneratorTestCase):
    """
    Appropriate data should be saved into appropriate
    indexes of object representing effect.
    """

    @patch('eos.data.cache_generator.converter.ModifierBuilder')
    def test_fields(self, mod_builder):
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeeffects'].append({'typeID': 1, 'effectID': 112})
        self.dh.data['dgmeffects'].append({
            'postExpression': 11, 'effectID': 112, 'isOffensive': True, 'falloffAttributeID': 3,
            'rangeAttributeID': 2, 'fittingUsageChanceAttributeID': 96, 'preExpression': 1,
            'durationAttributeID': 781, 'randomField': 666,  'dischargeAttributeID': 72,
            'isAssistance': False, 'effectCategory': 111, 'trackingSpeedAttributeID': 6})
        mod = self.mod(state=2, context=3, source_attribute_id=4, operator=5,
                       target_attribute_id=6, location=7, filter_type=8, filter_value=9)
        mod_builder.return_value.build_effect.return_value = ([mod], 29)
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['effects']), 1)
        self.assertIn(112, data['effects'])
        expected = {'effect_id': 112, 'effect_category': 111, 'is_offensive': True,
                    'is_assistance': False, 'duration_attribute_id': 781,
                    'discharge_attribute_id': 72, 'range_attribute_id': 2,
                    'falloff_attribute_id': 3, 'tracking_speed_attribute_id': 6,
                    'fitting_usage_chance_attribute_id': 96, 'build_status': 29, 'modifiers': [1]}
        self.assertEqual(data['effects'][112], expected)
