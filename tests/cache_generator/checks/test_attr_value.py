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


from eos.tests.cache_generator.generator_testcase import GeneratorTestCase
from eos.tests.environment import Logger


class TestAttrValue(GeneratorTestCase):
    """
    After cleanup generator should check that all attribute values
    are integers or floats, rows with other value types should be
    cleaned up.
    """

    def test_int(self):
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeattribs'].append({'typeID': 1, 'attributeID': 5, 'value': 8})
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['types']), 1)
        self.assertEqual(data['types'][1]['attributes'][5], 8)

    def test_float(self):
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeattribs'].append({'typeID': 1, 'attributeID': 5, 'value': 8.5})
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['types']), 1)
        self.assertEqual(data['types'][1]['attributes'][5], 8.5)

    def test_other(self):
        self.dh.data['invtypes'].append({'typeID': 1, 'groupID': 1, 'typeName': ''})
        self.dh.data['dgmtypeattribs'].append({'typeID': 1, 'attributeID': 5, 'value': None})
        data = self.run_generator()
        self.assertEqual(len(self.log), 2)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        log_record = self.log[1]
        self.assertEqual(log_record.name, 'eos_test.cache_generator')
        self.assertEqual(log_record.levelno, Logger.WARNING)
        self.assertEqual(log_record.msg, '1 attribute rows have non-numeric value, removing them')
        self.assertEqual(len(data['types']), 1)
        self.assertIn(1, data['types'])
        self.assertEqual(len(data['types'][1]['attributes']), 0)

    def test_cleanup(self):
        # Make sure cleanup runs before check being tested
        self.dh.data['invtypes'].append({'typeID': 1, 'typeName': ''})
        self.dh.data['dgmtypeattribs'].append({'typeID': 1, 'attributeID': 5, 'value': None})
        data = self.run_generator()
        self.assertEqual(len(self.log), 1)
        clean_stats = self.log[0]
        self.assertEqual(clean_stats.name, 'eos_test.cache_generator')
        self.assertEqual(clean_stats.levelno, Logger.INFO)
        self.assertEqual(len(data['types']), 0)
