#===============================================================================
# Copyright (C) 2011 Diego Duclos
# Copyright (C) 2011-2012 Anton Vorobyov
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


from eos.const import State, Location, Context, Operator
from eos.eve.const import EffectCategory
from eos.fit.attributeCalculator.modifier.modifier import Modifier
from eos.tests.attributeCalculator.attrCalcTestCase import AttrCalcTestCase
from eos.tests.attributeCalculator.environment import Fit, IndependentItem
from eos.tests.environment import Logger


class TestLocationDirectTarget(AttrCalcTestCase):
    """Test location.target for direct modifications"""

    def testError(self):
        tgtAttr = self.dh.attribute(attributeId=1)
        srcAttr = self.dh.attribute(attributeId=2)
        modifier = Modifier()
        modifier.state = State.offline
        modifier.context = Context.local
        modifier.sourceAttributeId = srcAttr.id
        modifier.operator = Operator.postPercent
        modifier.targetAttributeId = tgtAttr.id
        modifier.location = Location.target
        modifier.filterType = None
        modifier.filterValue = None
        effect = self.dh.effect(effectId=1, categoryId=EffectCategory.passive)
        effect._modifiers = (modifier,)
        fit = Fit()
        influenceSource = IndependentItem(self.dh.type_(typeId=102, effects=(effect,), attributes={srcAttr.id: 20}))
        # This functionality isn't implemented for now
        fit.items.append(influenceSource)
        self.assertEqual(len(self.log), 1)
        logRecord = self.log[0]
        self.assertEqual(logRecord.name, "eos_test.attributeCalculator")
        self.assertEqual(logRecord.levelno, Logger.WARNING)
        self.assertEqual(logRecord.msg, "malformed modifier on item 102: unsupported target location {} for direct modification".format(Location.target))
        fit.items.remove(influenceSource)
        self.assertBuffersEmpty(fit)
