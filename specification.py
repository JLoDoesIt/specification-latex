from collections import OrderedDict

import pandas as pd


def get_column_content_for_row(i_column_name, i_row):
    return getattr(i_row, i_column_name) if (i_column_name is not None and not pd.isna(
        getattr(i_row, i_column_name))) else None


class CurrentCharacteristicBloc:
    def __init__(self):
        self.bloc = None


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
