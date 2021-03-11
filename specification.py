from collections import OrderedDict
from enum import Enum

import pandas as pd
from pylatex import LongTable, NewLine
from pylatex.utils import bold


def get_column_content_for_row(i_column_name, i_row):
    return getattr(i_row, i_column_name) if (i_column_name is not None and not pd.isna(
        getattr(i_row, i_column_name))) else None


class CharacteristicStyle(Enum):
    TABLE = 'table'
    INLINE = 'inline'


class CharacteristicPosition(Enum):
    BEFORE = 'before'
    AFTER = 'after'


class CharacteristicBloc:
    def __init__(self, i_style=CharacteristicStyle.TABLE, i_position=CharacteristicPosition.AFTER):
        self.bloc = None
        self.style = i_style
        self.position = i_position
        self.characteristic_names = []
        self.characteristic_values = []

    def add_characteristics(self, i_characteristics_dict):
        if len(self.characteristic_names) == 0:
            self.characteristic_names = [*i_characteristics_dict.keys()]
        self.characteristic_values.append([i_characteristics_dict[it_key] for it_key in self.characteristic_names])

    def write_in_bloc(self):
        if self.bloc is not None:
            if self.style == CharacteristicStyle.TABLE:
                with self.bloc.create(LongTable('|' + 'c|' * len(self.characteristic_names))) as table:
                    table.add_hline()
                    table.add_row(self.characteristic_names, color='lightgray')
                    table.add_hline()
                    for it_characteristic_values in self.characteristic_values:
                        table.add_row(it_characteristic_values)
                        table.add_hline()
            else:
                for it_index in range(len(self.characteristic_names)):
                    text_list = [",".join(it_list) for it_list in zip(*self.characteristic_values)]
                    if self.position == CharacteristicPosition.AFTER:
                        self.bloc.append(bold(":".join([self.characteristic_names[it_index], text_list[it_index]])))
                        self.bloc.append(NewLine())
                    else:
                        self.bloc.insert(2 * it_index,
                                         bold(":".join([self.characteristic_names[it_index], text_list[it_index]])))
                        self.bloc.insert(2 * it_index + 1, NewLine())
            self.bloc = None
            self.characteristic_names = []
            self.characteristic_values = []


class SpecificationLine:
    def __init__(
            self,
            i_section_column,
            i_sub_section_column,
            i_sub_sub_section_column,
            i_description_column,
            i_characteristic_columns,
            i_data_row):
        self.section_column = i_section_column
        self.sub_section_column = i_sub_section_column
        self.sub_sub_section_column = i_sub_sub_section_column
        self.description_column = i_description_column
        self.characteristics = OrderedDict(
            {it_char_name: get_column_content_for_row(it_char_name, i_data_row) for it_char_name
             in i_characteristic_columns})
        self.section = get_column_content_for_row(i_section_column, i_data_row)
        self.sub_section = get_column_content_for_row(i_sub_section_column, i_data_row)
        self.sub_sub_section = get_column_content_for_row(i_sub_sub_section_column, i_data_row)
        self.description = get_column_content_for_row(i_description_column, i_data_row)

    def has_section(self):
        return self.section is not None

    def has_sub_section(self):
        return self.has_section and self.sub_section is not None

    def has_sub_sub_section(self):
        return self.has_sub_section() and self.sub_sub_section is not None

    def has_description(self):
        return self.description is not None

    def has_characteristics(self):
        return sum([1 if it_value is not None else 0 for it_value in self.characteristics.values()]) > 0
