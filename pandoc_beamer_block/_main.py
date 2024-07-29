#!/usr/bin/env python

"""
Pandoc filter for adding beamer block on specific div.
"""

from panflute import Div, Doc, Element, RawBlock, convert_text, run_filter


def prepare(doc: Doc):
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


def latex(
    elem: Element, environment: str, title: str, optional: bool = False
) -> list[Element]:
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

    optional
        The title optionality

    Returns
    -------
    list[Element]
        A list of pandoc elements.
    """
    if optional:
        if title:
            return [
                RawBlock(f"\\begin{{{environment}}}[{title}]", "tex"),
                elem,
                RawBlock(f"\\end{{{environment}}}", "tex"),
            ]
        return [
            RawBlock(f"\\begin{{{environment}}}", "tex"),
            elem,
            RawBlock(f"\\end{{{environment}}}", "tex"),
        ]
    return [
        RawBlock(f"\\begin{{{environment}}}{{{title}}}", "tex"),
        elem,
        RawBlock(f"\\end{{{environment}}}", "tex"),
    ]


# pylint: disable=too-many-return-statements
def block(elem: Element, doc: Doc) -> list[Element] | None:
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
    list[Element] | None
        A list of pandoc elements or None.
    """
    if doc.format == "beamer" and isinstance(elem, Div):
        classes = frozenset(elem.classes)

        # Loop on all fontsize definition
        for definition in doc.defined:
            # Are the classes correct?
            if classes >= definition["classes"]:
                if "title" in elem.attributes:
                    title = convert_text(
                        elem.attributes["title"],
                        output_format="latex",
                    )
                else:
                    title = ""

                if definition["type"] == "alert":
                    return latex(elem, "alertblock", title)
                if definition["type"] == "example":
                    return latex(elem, "exampleblock", title)
                if definition["type"] in (
                    "theorem",
                    "proof",
                    "corollary",
                    "definition",
                    "lemma",
                    "fact",
                ):
                    return latex(elem, definition["type"], title, True)
                return latex(elem, "block", title)
    return None


def main(doc: Doc | None = None) -> Doc:
    """
    Convert the pandoc document.

    Arguments
    ---------
    doc
        pandoc document

    Returns
    -------
    Doc
        The modified pandoc document.
    """
    return run_filter(block, doc=doc, prepare=prepare)


if __name__ == "__main__":
    main()
