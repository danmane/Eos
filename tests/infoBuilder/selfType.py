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

from unittest import TestCase

from eos import const
from eos.eve.expression import Expression
from eos.calc.info.builder.builder import InfoBuilder

class TestSelfType(TestCase):
    """Test parsing of trees describing modification which contains reference to typeID of its carrier"""

    def testBuildSuccess(self):
        eTgtOwn = Expression(24, value="Char")
        eSelf = Expression(24, value="Self")
        eSelfType = Expression(36, arg1=eSelf)
        eTgtAttr = Expression(22, attributeId=64)
        eOptr = Expression(21, value="PostPercent")
        eSrcAttr = Expression(22, attributeId=292)
        eTgtItms = Expression(49, arg1=eTgtOwn, arg2=eSelfType)
        eTgtSpec = Expression(12, arg1=eTgtItms, arg2=eTgtAttr)
        eOptrTgt = Expression(31, arg1=eOptr, arg2=eTgtSpec)
        eAddMod = Expression(11, arg1=eOptrTgt, arg2=eSrcAttr)
        eRmMod = Expression(62, arg1=eOptrTgt, arg2=eSrcAttr)
        infos, status = InfoBuilder().build(eAddMod, eRmMod)
        expStatus = const.effectInfoOkFull
        self.assertEqual(status, expStatus, msg="expressions must be successfully parsed (ID {})".format(expStatus))
        self.assertEqual(len(infos), 1, msg="one info must be generated")
        info = infos.pop()
        expFilterType = const.filterSkill
        self.assertEqual(info.filterType, expFilterType, msg="info target filter type must be skill (ID {})".format(expFilterType))
        expFilterValue = const.selfTypeID
        self.assertEqual(info.filterValue, expFilterValue, msg="info target filter value must be reference to typeID of self {}".format(expFilterValue))