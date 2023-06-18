#!/usr/bin/env python

"""
Pandoc filter for adding beamer block on specific div.
"""

from panflute import Div, RawBlock, convert_text, run_filter  # type: ignore


def prepare(doc):
    """
    Prepare the document.

    Arguments
    ---------
    doc
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
    Generate the LaTeX code.

    Arguments
    ---------
    elem
        The current element

    environment
        The environment to add

    title
        The environment title

    Returns
    -------
        A list of pandoc elements.
    """
    return [
        RawBlock(f"\\begin{{{environment}}}{title}", "tex"),
        elem,
        RawBlock(f"\\end{{{environment}}}", "tex"),
    ]


def block(elem, doc):
    """
    Transform div element.

    Arguments
    ---------
    elem
        current element
    doc
        pandoc document

    Returns
    -------
        A list of pandoc elements or None.
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
                    title = f"{{{convert_text(escaped, output_format='latex')}}}"
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
    Convert the pandoc document.

    Arguments
    ---------
    doc
        pandoc document

    Returns
    -------
        The modified pandoc document.
    """
    return run_filter(block, doc=doc, prepare=prepare)


if __name__ == "__main__":
    main()
