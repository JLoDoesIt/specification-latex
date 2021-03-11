import argparse
import sys
from collections import defaultdict

import pandas as pd
from pylatex import Document, Section, NewPage, Command, Subsection, Subsubsection, NewLine
from pylatex.utils import NoEscape

from specification import SpecificationLine, CharacteristicBloc, CharacteristicStyle, CharacteristicPosition


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
        i_file_name='specification',
        i_characteristic_style=CharacteristicStyle.TABLE,
        i_characteristic_position=CharacteristicPosition.AFTER):
    a_ranking_columns = get_ranking_columns(i_ranking_columns, i_section_column, i_sub_section_column,
                                            i_sub_sub_section_column)
    geometry_options = {}
    a_doc = Document(geometry_options=geometry_options)
    add_first_page(a_doc, i_title, i_authors)
    a_doc.append(NoEscape(r'\tableofcontents'))
    a_doc.append(NewPage())
    if len(a_ranking_columns) > 0:
        i_feature_list.sort_values(by=a_ranking_columns, inplace=True)
    a_sections_dict = defaultdict(lambda: defaultdict(list))
    a_current_characteristic_bloc = CharacteristicBloc(i_characteristic_style, i_characteristic_position)
    for it_feature_row in i_feature_list.itertuples():
        a_specification_line = SpecificationLine(
            i_section_column,
            i_sub_section_column,
            i_sub_sub_section_column,
            i_description_column,
            i_characteristic_columns,
            it_feature_row
        )
        create_section(a_doc, a_specification_line, a_sections_dict, a_current_characteristic_bloc)
    a_current_characteristic_bloc.write_in_bloc()
    a_doc.generate_pdf(i_file_name, clean_tex=False)


def get_ranking_columns(i_ranking_columns, i_section_column, i_sub_section_column, i_sub_sub_section_column):
    r_ranking_columns = []
    if i_ranking_columns is not None and len(i_ranking_columns) > 0 and i_ranking_columns[0] != '':
        r_ranking_columns = i_ranking_columns
    elif i_section_column is not None:
        r_ranking_columns.append(i_section_column)
        if i_sub_section_column is not None:
            r_ranking_columns.append(i_sub_section_column)
            if i_sub_sub_section_column is not None:
                r_ranking_columns.append(i_sub_sub_section_column)
    return r_ranking_columns


def create_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.has_section():
        if i_specification_line.section not in io_sections_dict:
            with io_doc.create(Section(i_specification_line.section)) as section:
                fill_section(section, i_specification_line, io_sections_dict, io_characteristic_bloc)
        else:
            fill_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)
    else:
        fill_paragraph(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)


def fill_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.has_sub_section():
        create_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)
    else:
        fill_paragraph(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc)


def create_sub_section(io_doc, i_specification_line, io_sections_dict, io_characteristic_bloc):
    if i_specification_line.sub_section not in io_sections_dict[i_specification_line.section]:
        with io_doc.create(Subsection(i_specification_line.sub_section)) as sub_section:
            fill_sub_section(sub_section, i_specification_line, io_sections_dict, io_characteristic_bloc)
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
        with io_doc.create(Subsubsection(i_specification_line.sub_sub_section)) as sub_sub_section:
            fill_paragraph(sub_sub_section, i_specification_line, io_sections_dict, io_characteristic_bloc)
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
    elif not i_specification_line.has_section() and i_specification_line.has_description():
        pass
    else:
        should_add_description = False
    if should_add_description:
        io_characteristic_bloc.write_in_bloc()
        if i_specification_line.has_description():
            io_doc.append(i_specification_line.description)
            io_doc.append(NewLine())
    if i_specification_line.has_characteristics():
        if io_characteristic_bloc.bloc is None:
            io_characteristic_bloc.bloc = io_doc
        io_characteristic_bloc.add_characteristics(i_specification_line.characteristics)


def add_first_page(io_doc, i_title, i_authors):
    io_doc.preamble.append(Command('title', i_title))
    io_doc.preamble.append(Command('author', i_authors))
    io_doc.preamble.append(Command('date', NoEscape(r'\today')))
    io_doc.append(NoEscape(r'\maketitle'))
    io_doc.append(NewPage())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert CSV files to textual structured document using PyTex',
        epilog="Now, let's have specify freely !")
    parser.add_argument('program', help='Default program argument in case files is called from Python executable')
    parser.add_argument('--default', action='store_true',
                        help='Specify that you want default parameters')
    parser.add_argument('--title', default='Default title',
                        help='Specify the title of your document on the first page')
    parser.add_argument('--author', default='Default author',
                        help='Specify the authoring you wish to make appear on the first page')
    parser.add_argument('--pdffile', default='specification_doc',
                        help='Specify the name of the tex/pdf file you want to save to')
    parser.add_argument('--csvfile',
                        help='Specify the name of the csv file you want to parse from')
    parser.add_argument('--separator', default=';', help='Define the separator of the CSV file (default to ";")')
    parser.add_argument('--section',
                        help='Specify the header of the column you want to use for sections in your document')
    parser.add_argument('--subsection',
                        help='Specify the header of the column you want to use for subsections in your document')
    parser.add_argument('--subsubsection',
                        help='Specify the header of the column you want to use for subsubsection in your document')
    parser.add_argument('--description',
                        help='Specify the header of the column you want to use to add descriptions in your document')
    parser.add_argument('--characteristics', default='',
                        help='Specify the slash (/) separated headers of the columns you want to use for characteristics in your document')
    parser.add_argument('--ranking', default='',
                        help='Specify the slash (/) separated headers of the columns you want to use for ranking in your document')
    parser.add_argument('--characstyle', choices=['table', 'inline'], default='table')
    parser.add_argument('--characposition', choices=['before', 'after'], default='after')
    arguments = vars(parser.parse_args(sys.argv))
    if arguments.get('default'):
        df = pd.read_csv('specifications.csv', sep=';')
        create_latex_specification(
            df,
            i_title='Ulysseus Digital Platform Specification',
            i_authors='Université Côte d\'Azure & Accenture',
            i_file_name='Functional specification',
            i_section_column="Service",
            i_sub_section_column="Epic",
            i_description_column="Description",
            i_characteristic_columns=["User", "WP"],
            i_characteristic_style=CharacteristicStyle.INLINE,
            i_characteristic_position=CharacteristicPosition.BEFORE,
            i_ranking_columns=['ID']
        )
        create_latex_specification(
            df,
            i_title='Ulysseus Digital Platform Specification - by Work Package',
            i_authors='Université Côte d\'Azure & Accenture',
            i_file_name='Functional specification - by WP',
            i_section_column="WP",
            i_sub_section_column="Service",
            i_sub_sub_section_column="Epic",
            i_description_column="Description",
            i_characteristic_columns=["User"],
            i_characteristic_style=CharacteristicStyle.INLINE,
            i_characteristic_position=CharacteristicPosition.BEFORE,
            i_ranking_columns=["WP", 'ID']
        )
        df_tech = pd.read_csv('tech_spec.csv', sep=';')
        create_latex_specification(
            df_tech,
            i_title='Ulysseus Community Technical Solutions',
            i_authors='Université Côte d\'Azure & Accenture',
            i_file_name='Technical solutions',
            i_section_column="Theme",
            i_sub_section_column="Service",
            i_description_column="Service_Description",
            i_characteristic_columns=["Tool", "University"],
            i_characteristic_position=CharacteristicPosition.AFTER,
            i_characteristic_style=CharacteristicStyle.TABLE
        )
    else:
        if arguments.get('csvfile') is not None:
            df = pd.read_csv(arguments.get('csvfile'), sep=arguments.get('separator'))
            a_characteristic_columns = arguments.get('characteristics').split('/') if arguments.get(
                'characteristics') != '' else []
            a_ranking_columns = arguments.get('ranking').split('/') if arguments.get('ranking') != '' else []
            create_latex_specification(
                df,
                i_title=arguments.get('title'),
                i_authors=arguments.get('author'),
                i_file_name=arguments.get('pdffile'),
                i_section_column=arguments.get('section'),
                i_sub_section_column=arguments.get('subsection'),
                i_sub_sub_section_column=arguments.get('subsubsection'),
                i_description_column=arguments.get('description'),
                i_characteristic_columns=a_characteristic_columns,
                i_ranking_columns=a_ranking_columns,
                i_characteristic_style=CharacteristicStyle(arguments.get('characstyle')),
                i_characteristic_position=CharacteristicPosition(arguments.get('characposition'))
            )
        else:
            raise Exception('No output CSV file found, use --csvfile or --default')
