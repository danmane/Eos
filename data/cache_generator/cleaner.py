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


from eos.const.eve import Group, Category


class Cleaner:
    """
    Class responsible for cleaning up unnecessary data
    from the database in automatic mode, using several
    pre-defined data relations.

    Required arguments:
    logger -- logger to use
    """

    def __init__(self, logger):
        self._logger = logger

    def clean(self, data):
        self.data = data
        # Container to store signs of so-called strong data,
        # such rows are immune to removal. Dictionary structure
        # is the same as structure of general data container
        self.strong_data = {}
        # Move some rows to strong data container
        self._pump_invtypes()
        # Also contains data in the very same format, but tables/rows
        # in this table are considered as pending for removal
        self.trashed_data = {}
        self._autocleanup()
        self._report_results()

    def _pump_invtypes(self):
        """
        Mark some hardcoded invtypes as strong.
        """
        # Tuple with categoryIDs of items we want to keep
        strong_categories = (Category.ship, Category.module, Category.charge,
                             Category.skill, Category.drone, Category.implant,
                             Category.subsystem)
        # Set with groupIDs of items we want to keep
        # It is set because we will need to modify it
        strong_groups = {Group.character, Group.effect_beacon}
        # Go through table data, filling valid groups set according to valid categories
        for datarow in self.data['invgroups']:
            if datarow.get('categoryID') in strong_categories:
                strong_groups.add(datarow['groupID'])
        rows_to_pump = set()
        for datarow in self.data['invtypes']:
            if datarow.get('groupID') in strong_groups:
                rows_to_pump.add(datarow)
        self._pump_data('invtypes', rows_to_pump)

    def _autocleanup(self):
        """
        Define auto-cleanup workflow.
        """
        self._kill_weak()
        self._changed = True
        # Cycle as long as we have changes during previous iteration.
        # We need this because contents of even invtypes may change, which,
        # by turn, will need to pull additional data into other tables
        while self._changed is True:
            self._changed = False
            self._reanimate_auxiliary_friends()
            self._reestablish_broken_relationships()

    def _kill_weak(self):
        """
        Trash all data which isn't marked as strong.
        """
        for table_name, table in self.data.items():
            to_trash = set()
            strong_rows = self.strong_data.get(table_name, set())
            to_trash.update(table.difference(strong_rows))
            self._trash_data(table_name, to_trash)

    def _reanimate_auxiliary_friends(self):
        """
        Restore rows in tables, which complement invtypes
        or serve as m:n mapping between invtypes and other tables.
        """
        # As we filter whole database using invtypes table,
        # gather invtype IDs we currently have in there
        type_ids = set(row['typeID'] for row in self.data['invtypes'])
        # Auxiliary tables are those which do not define
        # any entities, they just map one entities to others
        # or complement entities with additional data
        aux_tables = ('dgmtypeattribs', 'dgmtypeeffects')
        for table_name in aux_tables:
            to_restore = set()
            # Restore rows which map other entities to types
            for row in self.trashed_data[table_name]:
                if row['typeID'] in type_ids:
                    to_restore.add(row)
            if to_restore:
                self._changed = True
                self._restore_data(table_name, to_restore)

    def _reestablish_broken_relationships(self):
        """
        Restore all rows targeted by FKs of rows, which
        exist in actual data.
        """
        foreign_keys = {
            'dgmattribs': {
                'maxAttributeID': ('dgmattribs', 'attributeID')
            },
            'dgmeffects': {
                'preExpression': ('dgmexpressions', 'expressionID'),
                'postExpression': ('dgmexpressions', 'expressionID'),
                'durationAttributeID': ('dgmattribs', 'attributeID'),
                'trackingSpeedAttributeID': ('dgmattribs', 'attributeID'),
                'dischargeAttributeID': ('dgmattribs', 'attributeID'),
                'rangeAttributeID': ('dgmattribs', 'attributeID'),
                'falloffAttributeID': ('dgmattribs', 'attributeID'),
                'fittingUsageChanceAttributeID': ('dgmattribs', 'attributeID')
            },
            'dgmexpressions': {
                'arg1': ('dgmexpressions', 'expressionID'),
                'arg2': ('dgmexpressions', 'expressionID'),
                'expressionTypeID': ('invtypes', 'typeID'),
                'expressionGroupID': ('invgroups', 'groupID'),
                'expressionAttributeID': ('dgmattribs', 'attributeID')
            },
            'dgmtypeattribs': {
                'typeID': ('invtypes', 'typeID'),
                'attributeID': ('dgmattribs', 'attributeID')
            },
            'dgmtypeeffects': {
                'typeID': ('invtypes', 'typeID'),
                'effectID': ('dgmeffects', 'effectID')
            },
            'invtypes': {
                'groupID': ('invgroups', 'groupID')
            }
        }
        # Container for 'target data', matches with which are
        # going to be restored
        # Format: {(target table name, target column name): {data}}}
        target_data = {}
        for source_table_name, table_fks in foreign_keys.items():
            for source_field_name, fk_target in table_fks.items():
                target_table_name, target_field_name = fk_target
                for row in self.data[source_table_name]:
                    fk_value = row.get(source_field_name)
                    # If there's no such field in a row or it is None,
                    # this is not a valid FK reference
                    if fk_value is None:
                        continue
                    data_set = target_data.setdefault((target_table_name, target_field_name), set())
                    data_set.add(fk_value)
        # Now, when we have all the target data values, we may look for
        # rows, which have matching values, and restore them
        for target_spec, target_values in target_data.items():
            target_table_name, target_field_name = target_spec
            to_restore = set()
            for row in self.trashed_data[target_table_name]:
                if row.get(target_field_name) in target_values:
                    to_restore.add(row)
            if to_restore:
                self._changed = True
                self._restore_data(target_table_name, to_restore)

    def _report_results(self):
        """
        Run calculations to report about cleanup results
        to the logger.
        """
        table_msgs = []
        for table_name in sorted(self.data):
            datalen = len(self.data[table_name])
            trashedlen = len(self.trashed_data[table_name])
            try:
                ratio = trashedlen / (datalen + trashedlen)
            # Skip results if table was empty
            except ZeroDivisionError:
                continue
            table_msgs.append('{:.1%} from {}'.format(ratio, table_name))
        if table_msgs:
            msg = 'cleaned: {}'.format(', '.join(table_msgs))
            self._logger.info(msg, child_name='cache_generator')

    def _pump_data(self, table_name, datarows):
        """
        Auxiliary method, mark data rows as strong.

        Required arguments:
        table_name -- name of table for which we're pumping data
        datarows -- set with rows to pump
        """
        strong_rows = self.strong_data.setdefault(table_name, set())
        strong_rows.update(datarows)

    def _trash_data(self, table_name, datarows):
        """
        Auxiliary method, mark data rows as pending removal.

        Required arguments:
        table_name -- name of table for which we're removing data
        datarows -- set with rows to remove
        """
        data_table = self.data[table_name]
        trash_table = self.trashed_data.setdefault(table_name, set())
        # Update both trashed data and source data
        trash_table.update(datarows)
        data_table.difference_update(datarows)

    def _restore_data(self, table_name, datarows):
        """
        Auxiliary method, move data from trash back to actual
        data container.

        Required arguments:
        table_name -- name of table for which we're restoring data
        datarows -- set with rows to restore
        """
        data_table = self.data[table_name]
        trash_table = self.trashed_data[table_name]
        # Update both trashed data and source data
        data_table.update(datarows)
        trash_table.difference_update(datarows)
