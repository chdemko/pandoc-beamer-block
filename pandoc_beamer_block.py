#!/usr/bin/env python

"""
Pandoc filter for adding beamer block on specific div
"""

from panflute import run_filter, Div, RawBlock


def prepare(doc):
    """
    Prepare the document

    Arguments
    ---------
        doc:
            The pandoc document
    """

    # Prepare the definitions
    doc.defined = []

    # Get the meta data
    meta = doc.get_metadata("pandoc-beamer-block")

    if isinstance(meta, list):

        # Loop on all definitions
        for definition in meta:

            # Verify the definition
            if (
                isinstance(definition, dict)
                and "classes" in definition
                and isinstance(definition["classes"], list)
            ):
                definition["classes"] = frozenset(definition["classes"])
                definition["type"] = definition.get("type", "info")
                doc.defined.append(definition)


def latex(elem, environment, title):
    """
    Generate the LaTeX code

    Arguments
    ---------
        elem:
            The current element

        environment:
            The environment to add

        title:
            The environment title

    Returns
    -------
        A list of pandoc elements.
    """
    return [
        RawBlock("\\begin{%s}%s" % (environment, title), "tex"),
        elem,
        RawBlock("\\end{%s}" % environment, "tex"),
    ]


def block(elem, doc):
    """
    Transform div element.

    Arguments
    ---------
        elem:
            current element
        doc:
            pandoc document
    """
    if doc.format == "beamer" and isinstance(elem, Div):
        classes = frozenset(elem.classes)

        # Loop on all fontsize definition
        for definition in doc.defined:

            # Are the classes correct?
            if classes >= definition["classes"]:
                if "title" in elem.attributes:
                    escaped = elem.attributes["title"].translate(
                        str.maketrans({"{": r"\{", "}": r"\}", "%": r"\%"})
                    )
                    title = "{%s}" % escaped
                else:
                    title = ""

                if definition["type"] == "alert":
                    return latex(elem, "alertblock", title)
                if definition["type"] == "example":
                    return latex(elem, "exampleblock", title)
                return latex(elem, "block", title)
    return None


def main(doc=None):
    """
    main function.

    Arguments
    ---------
        doc:
            pandoc document
    """
    return run_filter(block, doc=doc, prepare=prepare)


if __name__ == "__main__":
    main()
