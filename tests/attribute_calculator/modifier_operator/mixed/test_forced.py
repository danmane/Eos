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


from eos.const.eos import State, Location, Context, FilterType, Operator
from eos.const.eve import EffectCategory
from eos.data.cache_object.modifier import Modifier
from eos.tests.attribute_calculator.attrcalc_testcase import AttrCalcTestCase
from eos.tests.attribute_calculator.environment import IndependentItem, ShipItem


class TestOperatorForcedValue(AttrCalcTestCase):
    """Test that post-assignment forces value of attribute"""

    def test_forced_value(self):
        tgt_attr = self.ch.attribute(attribute_id=1)
        src_attr = self.ch.attribute(attribute_id=2)
        modifier_pre_ass = Modifier()
        modifier_pre_ass.state = State.offline
        modifier_pre_ass.context = Context.local
        modifier_pre_ass.source_attribute_id = src_attr.id
        modifier_pre_ass.operator = Operator.pre_assignment
        modifier_pre_ass.target_attribute_id = tgt_attr.id
        modifier_pre_ass.location = Location.ship
        modifier_pre_ass.filter_type = FilterType.all_
        modifier_pre_ass.filter_value = None
        effect_pre_ass = self.ch.effect(effect_id=1, category_id=EffectCategory.passive)
        effect_pre_ass.modifiers = (modifier_pre_ass,)
        influence_source_pre_ass = IndependentItem(self.ch.type_(type_id=1, effects=(effect_pre_ass,),
                                                                 attributes={src_attr.id: 5}))
        self.fit.items.add(influence_source_pre_ass)
        modifier_pre_mul = Modifier()
        modifier_pre_mul.state = State.offline
        modifier_pre_mul.context = Context.local
        modifier_pre_mul.source_attribute_id = src_attr.id
        modifier_pre_mul.operator = Operator.pre_mul
        modifier_pre_mul.target_attribute_id = tgt_attr.id
        modifier_pre_mul.location = Location.ship
        modifier_pre_mul.filter_type = FilterType.all_
        modifier_pre_mul.filter_value = None
        effect_pre_mul = self.ch.effect(effect_id=2, category_id=EffectCategory.passive)
        effect_pre_mul.modifiers = (modifier_pre_mul,)
        influence_source_pre_mul = IndependentItem(self.ch.type_(type_id=2, effects=(effect_pre_mul,),
                                                                 attributes={src_attr.id: 50}))
        self.fit.items.add(influence_source_pre_mul)
        modifier_pre_div = Modifier()
        modifier_pre_div.state = State.offline
        modifier_pre_div.context = Context.local
        modifier_pre_div.source_attribute_id = src_attr.id
        modifier_pre_div.operator = Operator.pre_div
        modifier_pre_div.target_attribute_id = tgt_attr.id
        modifier_pre_div.location = Location.ship
        modifier_pre_div.filter_type = FilterType.all_
        modifier_pre_div.filter_value = None
        effect_pre_div = self.ch.effect(effect_id=3, category_id=EffectCategory.passive)
        effect_pre_div.modifiers = (modifier_pre_div,)
        influence_source_pre_div = IndependentItem(self.ch.type_(type_id=3, effects=(effect_pre_div,),
                                                                 attributes={src_attr.id: 0.5}))
        self.fit.items.add(influence_source_pre_div)
        modifier_mod_add = Modifier()
        modifier_mod_add.state = State.offline
        modifier_mod_add.context = Context.local
        modifier_mod_add.source_attribute_id = src_attr.id
        modifier_mod_add.operator = Operator.mod_add
        modifier_mod_add.target_attribute_id = tgt_attr.id
        modifier_mod_add.location = Location.ship
        modifier_mod_add.filter_type = FilterType.all_
        modifier_mod_add.filter_value = None
        effect_mod_add = self.ch.effect(effect_id=4, category_id=EffectCategory.passive)
        effect_mod_add.modifiers = (modifier_mod_add,)
        influence_source_mod_add = IndependentItem(self.ch.type_(type_id=4, effects=(effect_mod_add,),
                                                                 attributes={src_attr.id: 10}))
        self.fit.items.add(influence_source_mod_add)
        modifier_mod_sub = Modifier()
        modifier_mod_sub.state = State.offline
        modifier_mod_sub.context = Context.local
        modifier_mod_sub.source_attribute_id = src_attr.id
        modifier_mod_sub.operator = Operator.mod_sub
        modifier_mod_sub.target_attribute_id = tgt_attr.id
        modifier_mod_sub.location = Location.ship
        modifier_mod_sub.filter_type = FilterType.all_
        modifier_mod_sub.filter_value = None
        effect_mod_sub = self.ch.effect(effect_id=5, category_id=EffectCategory.passive)
        effect_mod_sub.modifiers = (modifier_mod_sub,)
        influence_source_mod_sub = IndependentItem(self.ch.type_(type_id=5, effects=(effect_mod_sub,),
                                                                 attributes={src_attr.id: 63}))
        self.fit.items.add(influence_source_mod_sub)
        modifier_post_mul = Modifier()
        modifier_post_mul.state = State.offline
        modifier_post_mul.context = Context.local
        modifier_post_mul.source_attribute_id = src_attr.id
        modifier_post_mul.operator = Operator.post_mul
        modifier_post_mul.target_attribute_id = tgt_attr.id
        modifier_post_mul.location = Location.ship
        modifier_post_mul.filter_type = FilterType.all_
        modifier_post_mul.filter_value = None
        effect_post_mul = self.ch.effect(effect_id=6, category_id=EffectCategory.passive)
        effect_post_mul.modifiers = (modifier_post_mul,)
        influence_source_post_mul = IndependentItem(self.ch.type_(type_id=6, effects=(effect_post_mul,),
                                                                  attributes={src_attr.id: 1.35}))
        self.fit.items.add(influence_source_post_mul)
        modifier_post_div = Modifier()
        modifier_post_div.state = State.offline
        modifier_post_div.context = Context.local
        modifier_post_div.source_attribute_id = src_attr.id
        modifier_post_div.operator = Operator.post_div
        modifier_post_div.target_attribute_id = tgt_attr.id
        modifier_post_div.location = Location.ship
        modifier_post_div.filter_type = FilterType.all_
        modifier_post_div.filter_value = None
        effect_post_div = self.ch.effect(effect_id=7, category_id=EffectCategory.passive)
        effect_post_div.modifiers = (modifier_post_div,)
        influence_source_post_div = IndependentItem(self.ch.type_(type_id=7, effects=(effect_post_div,),
                                                                  attributes={src_attr.id: 2.7}))
        self.fit.items.add(influence_source_post_div)
        modifier_post_perc = Modifier()
        modifier_post_perc.state = State.offline
        modifier_post_perc.context = Context.local
        modifier_post_perc.source_attribute_id = src_attr.id
        modifier_post_perc.operator = Operator.post_percent
        modifier_post_perc.target_attribute_id = tgt_attr.id
        modifier_post_perc.location = Location.ship
        modifier_post_perc.filter_type = FilterType.all_
        modifier_post_perc.filter_value = None
        effect_post_perc = self.ch.effect(effect_id=8, category_id=EffectCategory.passive)
        effect_post_perc.modifiers = (modifier_post_perc,)
        influence_source_post_perc = IndependentItem(self.ch.type_(type_id=8, effects=(effect_post_perc,),
                                                                   attributes={src_attr.id: 15}))
        self.fit.items.add(influence_source_post_perc)
        modifier_post_ass = Modifier()
        modifier_post_ass.state = State.offline
        modifier_post_ass.context = Context.local
        modifier_post_ass.source_attribute_id = src_attr.id
        modifier_post_ass.operator = Operator.post_assignment
        modifier_post_ass.target_attribute_id = tgt_attr.id
        modifier_post_ass.location = Location.ship
        modifier_post_ass.filter_type = FilterType.all_
        modifier_post_ass.filter_value = None
        effect_post_ass = self.ch.effect(effect_id=9, category_id=EffectCategory.passive)
        effect_post_ass.modifiers = (modifier_post_ass,)
        influence_source_post_ass = IndependentItem(self.ch.type_(type_id=9, effects=(effect_post_ass,),
                                                                  attributes={src_attr.id: 68}))
        self.fit.items.add(influence_source_post_ass)
        influence_target = ShipItem(self.ch.type_(type_id=10, attributes={tgt_attr.id: 100}))
        self.fit.items.add(influence_target)
        # Post-assignment value must override all other modifications
        self.assertAlmostEqual(influence_target.attributes[tgt_attr.id], 68)
        self.fit.items.remove(influence_source_pre_ass)
        self.fit.items.remove(influence_source_pre_mul)
        self.fit.items.remove(influence_source_pre_div)
        self.fit.items.remove(influence_source_mod_add)
        self.fit.items.remove(influence_source_mod_sub)
        self.fit.items.remove(influence_source_post_mul)
        self.fit.items.remove(influence_source_post_div)
        self.fit.items.remove(influence_source_post_perc)
        self.fit.items.remove(influence_source_post_ass)
        self.fit.items.remove(influence_target)
        self.assertEqual(len(self.log), 0)
        self.assert_link_buffers_empty(self.fit)
