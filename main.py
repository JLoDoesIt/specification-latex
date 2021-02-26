import collections
from collections import defaultdict

import pandas as pd
from pylatex import Document, Section, NewPage, Command, Subsection, Subsubsection, Tabular, NewLine
from pylatex.utils import bold, NoEscape


def create_latex_specification(
        i_feature_list,
        i_section_column,
        i_sub_section_column=None,
        i_sub_sub_section_column=None,
        i_description_column=None,
        i_characteristic_columns=None,
        i_ranking_columns=None,
        i_title='Specification',
        i_authors='Author NAMES',
        i_file_name='specification'):
    finest_section_level = i_section_column if i_sub_section_column is None else (
        i_sub_section_column if i_sub_sub_section_column is None else i_sub_sub_section_column)
    a_ranking_columns = i_ranking_columns if i_ranking_columns is not None else [i_section_column, i_sub_section_column]
    geometry_options = {}
    doc = Document(geometry_options=geometry_options)
    add_first_page(doc, i_title, i_authors)
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NewPage())
    i_feature_list.sort_values(by=a_ranking_columns, inplace=True)
    a_sections_dict = defaultdict(lambda: defaultdict(list))
    for it_feature_row in i_feature_list.itertuples():
        if not pd.isna(getattr(it_feature_row, finest_section_level)):
            a_section_name = get_column_content_for_row(i_section_column, it_feature_row)
            a_sub_section_name = get_column_content_for_row(i_sub_section_column,
                                                            it_feature_row) if i_sub_section_column is not None else None
            a_sub_sub_section_name = get_column_content_for_row(i_sub_sub_section_column,
                                                                it_feature_row) if i_sub_sub_section_column is not None else None
            a_description = get_column_content_for_row(i_description_column, it_feature_row)
            a_characteristics = collections.OrderedDict(
                {it_char_name: get_column_content_for_row(it_char_name, it_feature_row) for it_char_name
                 in i_characteristic_columns})
            # print(an_epic + ' - ' + a_description)
            create_section(a_section_name, a_sections_dict, a_characteristics, a_description,
                           a_sub_section_name, doc, a_sub_sub_section_name,
                           i_description_column)
    doc.generate_pdf(i_file_name, clean_tex=False)


def create_section(i_section_name, io_sections_dict, i_characteristics, i_description,
                   i_sub_section_name, io_doc, i_sub_sub_section_name, i_description_column):
    if i_section_name not in io_sections_dict:
        with io_doc.create(Section(i_section_name)):
            fill_section(i_characteristics, i_description, i_section_name, i_sub_section_name,
                         i_sub_sub_section_name, io_doc, io_sections_dict, i_description_column)
    else:
        fill_section(i_characteristics, i_description, i_section_name, i_sub_section_name,
                     i_sub_sub_section_name, io_doc, io_sections_dict, i_description_column)


def fill_section(i_characteristics, i_description, i_section_name, i_sub_section_name,
                 i_sub_sub_section_name, io_doc, io_sections_dict, i_description_column):
    if i_sub_section_name is not None:
        create_sub_section(i_section_name, io_sections_dict, i_characteristics,
                           i_description,
                           i_sub_section_name, io_doc, i_sub_sub_section_name,
                           i_description_column)
    else:
        fill_paragraph(i_description, i_sub_section_name, io_doc,
                       i_characteristics, io_sections_dict,
                       i_section_name, i_sub_sub_section_name, i_description_column
                       )


def create_sub_section(i_section_name, io_sections_dict, i_characteristics, i_description,
                       i_sub_section_name, io_doc, i_sub_sub_section_name,
                       i_description_column):
    if i_sub_section_name not in io_sections_dict[i_section_name]:
        with io_doc.create(Subsection(i_sub_section_name)):
            fill_sub_section(i_characteristics, i_description, i_section_name,
                             i_sub_section_name, i_sub_sub_section_name, io_doc, io_sections_dict, i_description_column)
    else:
        fill_sub_section(i_characteristics, i_description, i_section_name,
                         i_sub_section_name, i_sub_sub_section_name, io_doc, io_sections_dict, i_description_column)


def fill_sub_section(i_characteristics, i_description, i_section_name, i_sub_section_name,
                     i_sub_sub_section_name, io_doc, io_sections_dict, i_description_column):
    if i_sub_sub_section_name is not None:
        create_sub_sub_section(i_section_name, io_sections_dict, i_characteristics, i_description,
                               i_sub_section_name, io_doc, i_sub_sub_section_name,
                               i_description_column)
    else:
        fill_paragraph(i_description, i_sub_section_name, io_doc,
                       i_characteristics, io_sections_dict,
                       i_section_name, i_sub_sub_section_name, i_description_column
                       )


def create_sub_sub_section(i_section_name, io_sections_dict, i_characteristics, i_description,
                           i_sub_section_name, io_doc, i_sub_sub_section_name,
                           i_description_column):
    if i_sub_sub_section_name not in io_sections_dict[i_section_name][i_sub_section_name]:
        with io_doc.create(Subsubsection(i_sub_sub_section_name)):
            fill_paragraph(i_description, i_sub_section_name, io_doc,
                           i_characteristics, io_sections_dict,
                           i_section_name, i_sub_sub_section_name, i_description_column)
    else:
        fill_paragraph(i_description, i_sub_section_name, io_doc,
                       i_characteristics, io_sections_dict,
                       i_section_name, i_sub_sub_section_name, i_description_column)


def fill_paragraph(i_description, i_sub_section_name, io_doc,
                   i_characteristics, io_sections_dict, i_section_name, i_sub_sub_section_name, i_description_column):
    should_add_description = False
    if i_sub_section_name is not None:
        if i_sub_sub_section_name is not None:
            if i_sub_sub_section_name not in io_sections_dict[i_section_name][i_sub_section_name]:
                io_sections_dict[i_section_name][i_sub_section_name].append(i_sub_sub_section_name)
                should_add_description = True
        elif i_sub_section_name not in io_sections_dict[i_section_name]:
            io_sections_dict[i_section_name][i_sub_section_name] = []
            should_add_description = True
    elif i_section_name not in io_sections_dict:
        io_sections_dict[i_section_name] = {}
        should_add_description = True
    if should_add_description:
        if i_description_column is not None:
            io_doc.append(i_description)
            io_doc.append(NewLine())
    if len(i_characteristics) > 0:
        with io_doc.create(Tabular('|'+'c|'*len(i_characteristics))) as table:
            table.add_hline()
            table.add_row(i_characteristics.keys(), color='lightgray')
            table.add_hline()
            table.add_row(i_characteristics.values())
            table.add_hline()
        io_doc.append(NewLine())


def get_column_content_for_row(i_column_name, i_row):
    return getattr(i_row, i_column_name) if not pd.isna(
        getattr(i_row, i_column_name)) else 'No ' + i_column_name


def add_first_page(io_doc, i_title, i_authors):
    io_doc.preamble.append(Command('title', i_title))
    io_doc.preamble.append(Command('author', i_authors))
    io_doc.preamble.append(Command('date', NoEscape(r'\today')))
    io_doc.append(NoEscape(r'\maketitle'))
    io_doc.append(NewPage())


if __name__ == '__main__':
    df = pd.read_csv('specifications.csv', sep=';')
    create_latex_specification(
        df,
        i_title='Ulysseus Digital Platform Specification',
        i_authors='Candice OUDOT, Mathilde La Plaze, Jean-Loic CAVAZZA',
        i_file_name='Functional specification',
        i_section_column="Service",
        i_sub_section_column="Epic",
        i_description_column="Description",
        i_characteristic_columns=["User"],
        i_ranking_columns=['ID']
    )
    create_latex_specification(
        df,
        i_title='Ulysseus Digital Platform Specification - by Work Package',
        i_authors='Candice OUDOT, Mathilde La Plaze, Jean-Loic CAVAZZA',
        i_file_name='Functional specification - by WP',
        i_section_column="WP",
        i_sub_section_column="Service",
        i_sub_sub_section_column="Epic",
        i_description_column="Description",
        i_characteristic_columns=["User"],
        i_ranking_columns=["WP", 'ID']
    )
    df_tech = pd.read_csv('tech_spec.csv', sep=';')
    create_latex_specification(
        df_tech,
        i_title='Ulysseus Community Technical Solutions',
        i_authors='Candice OUDOT, Mathilde La Plaze, Jean-Loic CAVAZZA',
        i_file_name='Technical solutions',
        i_section_column="Theme",
        i_sub_section_column="Service",
        i_description_column="Service_Description",
        i_characteristic_columns=["Tool", "University"]
    )
