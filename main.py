from collections import defaultdict

import pandas as pd
from pylatex import Document, Section, Subsection, NewPage, Command
from pylatex.utils import bold, NoEscape


def create_latex_specification(
        i_subsections_list,
        i_section_column="Service",
        i_sub_section_column="Epic",
        i_sub_section_description_column="Description",
        i_sub_section_characteristic_column="User",
        i_title='Specification',
        i_authors='Author NAMES',
        i_file_name='full'):
    geometry_options = {}
    doc = Document(geometry_options=geometry_options)
    add_first_page(doc, i_title, i_authors)
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NewPage())
    i_subsections_list.sort_values(by=[i_section_column, i_sub_section_column], inplace=True)
    a_sections_dict = defaultdict(lambda: defaultdict(list))
    for it_subsection_row in i_subsections_list.itertuples():
        if not pd.isna(getattr(it_subsection_row, i_sub_section_column)):
            a_section_name = get_column_content_for_row(i_section_column, it_subsection_row)
            a_subsection_name = get_column_content_for_row(i_sub_section_column, it_subsection_row)
            a_subsection_description = get_column_content_for_row(i_sub_section_description_column, it_subsection_row)
            a_subsection_characteristic = get_column_content_for_row(i_sub_section_characteristic_column,
                                                                     it_subsection_row)
            # print(an_epic + ' - ' + a_description)
            create_section(a_section_name, a_sections_dict, a_subsection_characteristic, a_subsection_description,
                           a_subsection_name, doc, i_sub_section_characteristic_column)
    doc.generate_pdf(i_file_name, clean_tex=False)


def create_section(a_section_name, a_sections_dict, a_subsection_characteristic, a_subsection_description,
                   a_subsection_name, doc, i_sub_section_characteristic_column):
    if a_section_name not in a_sections_dict:
        with doc.create(Section(a_section_name)):
            create_subsection(a_section_name, a_sections_dict, a_subsection_characteristic, a_subsection_description,
                              a_subsection_name, doc, i_sub_section_characteristic_column)
    else:
        create_subsection(a_section_name, a_sections_dict, a_subsection_characteristic, a_subsection_description,
                          a_subsection_name, doc, i_sub_section_characteristic_column)


def create_subsection(i_section_name, io_sections_dict, i_subsection_characteristic, i_subsection_description,
                      i_subsection_name, io_doc, i_sub_section_characteristic_column):
    if i_subsection_name not in io_sections_dict[i_section_name]:
        with io_doc.create(Subsection(i_subsection_name)):
            fill_subsection(i_subsection_description, i_subsection_name, io_doc,
                            i_sub_section_characteristic_column, i_subsection_characteristic, io_sections_dict,
                            i_section_name)
    else:
        fill_subsection(i_subsection_description, i_subsection_name, io_doc,
                        i_sub_section_characteristic_column, i_subsection_characteristic, io_sections_dict,
                        i_section_name)


def get_column_content_for_row(i_column_name, i_row):
    return getattr(i_row, i_column_name) if not pd.isna(
        getattr(i_row, i_column_name)) else 'No ' + i_column_name


def fill_subsection(i_subsection_description, i_subsection_name, io_doc, i_sub_section_characteristic_column,
                    i_subsection_characteristic, io_sections_dict, i_section_name):
    if i_subsection_characteristic not in io_sections_dict[i_section_name][i_subsection_name]:
        io_sections_dict[i_section_name][i_subsection_name].append(i_subsection_characteristic)
        io_doc.append(bold(i_sub_section_characteristic_column + ": " + i_subsection_characteristic + "\n"))
        io_doc.append(i_subsection_description + "\n")


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
        i_file_name='Functional specification'
    )
    df_tech = pd.read_csv('tech_spec.csv', sep=';')
    create_latex_specification(
        df_tech,
        i_title='Ulysseus Community Technical Solutions',
        i_authors='Candice OUDOT, Mathilde La Plaze, Jean-Loic CAVAZZA',
        i_section_column="Theme",
        i_sub_section_column="Service",
        i_sub_section_description_column="Description",
        i_sub_section_characteristic_column="Tool",
        i_file_name='Technical solutions'
    )
