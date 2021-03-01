from collections import defaultdict

import pandas as pd
from pylatex import Document, Section, NewPage, Command, Subsection, Subsubsection, Tabular, NewLine
from pylatex.utils import NoEscape

from specification import SpecificationLine, CurrentCharacteristicBloc


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
    a_ranking_columns = i_ranking_columns if i_ranking_columns is not None else [i_section_column, i_sub_section_column]
    geometry_options = {}
    a_doc = Document(geometry_options=geometry_options)
    add_first_page(a_doc, i_title, i_authors)
    a_doc.append(NoEscape(r'\tableofcontents'))
    a_doc.append(NewPage())
    i_feature_list.sort_values(by=a_ranking_columns, inplace=True)
    a_sections_dict = defaultdict(lambda: defaultdict(list))
    a_characteristic_bloc = CurrentCharacteristicBloc()
    for it_feature_row in i_feature_list.itertuples():
        a_specification_line = SpecificationLine(
            i_section_column,
            i_sub_section_column,
            i_sub_sub_section_column,
            i_description_column,
            i_characteristic_columns,
            it_feature_row
        )
        create_section(a_doc, a_specification_line, a_sections_dict, a_characteristic_bloc)
    a_doc.generate_pdf(i_file_name, clean_tex=False)


def create_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.has_section():
        if i_specification_line.section not in io_sections_dict:
            with io_doc.create(Section(i_specification_line.section)):
                fill_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)
        else:
            fill_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)


def fill_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.has_sub_section():
        create_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)
    else:
        fill_paragraph(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)


def create_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.sub_section not in io_sections_dict[i_specification_line.section]:
        with io_doc.create(Subsection(i_specification_line.sub_section)):
            fill_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)
    else:
        fill_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)


def fill_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.has_sub_sub_section():
        create_sub_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)
    else:
        fill_paragraph(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)


def create_sub_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.sub_sub_section not in io_sections_dict[i_specification_line.section][
        i_specification_line.sub_section]:
        with io_doc.create(Subsubsection(i_specification_line.sub_sub_section)):
            fill_paragraph(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)
    else:
        fill_paragraph(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)


def fill_paragraph(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    should_add_description = True
    if i_specification_line.has_sub_sub_section() and i_specification_line.sub_sub_section not in \
            io_sections_dict[i_specification_line.section][i_specification_line.sub_section]:
        io_sections_dict[i_specification_line.section][i_specification_line.sub_section].append(
            i_specification_line.sub_sub_section)
    elif i_specification_line.has_sub_section() and i_specification_line.sub_section not in io_sections_dict[
        i_specification_line.section]:
        io_sections_dict[i_specification_line.section][i_specification_line.sub_section] = []
    elif i_specification_line.has_section() and i_specification_line.section not in io_sections_dict:
        io_sections_dict[i_specification_line.section] = {}
    else:
        should_add_description = False
    if should_add_description:
        io_characteristic_bloc.bloc = None
        if i_specification_line.has_description():
            io_doc.append(i_specification_line.description)
            io_doc.append(NewLine())
    if i_specification_line.has_characteristics():
        if io_characteristic_bloc.bloc is None:
            with io_doc.create(Tabular('|' + 'c|' * len(i_specification_line.characteristics))) as table:
                io_characteristic_bloc.bloc = table
                table.add_hline()
                table.add_row(i_specification_line.characteristics.keys(), color='lightgray')
                table.add_hline()
                table.add_row(i_specification_line.characteristics.values())
                table.add_hline()
        else:
            io_characteristic_bloc.bloc.add_row(i_specification_line.characteristics.values())
            io_characteristic_bloc.bloc.add_hline()


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
