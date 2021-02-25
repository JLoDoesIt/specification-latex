import pandas as pd
from pylatex import Document, Section, Subsection, NewPage, Command
from pylatex.utils import bold, NoEscape


def create_latex_specification(i_epic_list):
    geometry_options = {}
    doc = Document(geometry_options=geometry_options)
    add_first_page(doc)
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NewPage())
    i_epic_list.sort_values(by=['Service'], inplace=True)
    a_service_list = []
    for it_epic_row in i_epic_list.itertuples():
        if not pd.isna(it_epic_row.Epic):
            a_service = it_epic_row.Service if not pd.isna(it_epic_row.Service) else 'No service name'
            an_epic = it_epic_row.Epic
            a_description = it_epic_row.Description if not pd.isna(it_epic_row.Description) else 'No description'
            a_user = it_epic_row.Utilisateur if not pd.isna(it_epic_row.Utilisateur) else 'No user'
            # print(an_epic + ' - ' + a_description)
            if a_service not in a_service_list:
                a_service_list.append(a_service)
                with doc.create(Section(a_service)):
                    create_epic_subsection(a_description, an_epic, doc, a_user)
            else:
                create_epic_subsection(a_description, an_epic, doc, a_user)
    doc.generate_pdf('full', clean_tex=False)


def create_epic_subsection(i_description, i_epic, io_doc, i_user):
    with io_doc.create(Subsection(i_epic)):
        io_doc.append(bold("User: " + i_user+"\n"))
        io_doc.append(i_description)


def add_first_page(io_doc):
    io_doc.preamble.append(Command('title', 'Ulysseus Digital Platform Specification'))
    io_doc.preamble.append(Command('author', 'Candice OUDOT, Mathilde La Plaze, Jean-Loic CAVAZZA'))
    io_doc.preamble.append(Command('date', NoEscape(r'\today')))
    io_doc.append(NoEscape(r'\maketitle'))
    io_doc.append(NewPage())


if __name__ == '__main__':
    df = pd.read_csv('specifications.csv', sep=';')
    create_latex_specification(df)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
