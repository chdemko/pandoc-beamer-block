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
            # pylint: disable=bad-continuation
            if (
                isinstance(definition, dict)
                and "classes" in definition
                and isinstance(definition["classes"], list)
            ):
                definition["classes"] = frozenset(definition["classes"])
                definition["type"] = definition.get("type", "info")
                doc.defined.append(definition)


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
                    return [
                        RawBlock("\\begin{alertblock}%s" % title, "tex"),
                        elem,
                        RawBlock("\\end{alertblock}", "tex"),
                    ]
                if definition["type"] == "example":
                    return [
                        RawBlock("\\begin{exampleblock}%s" % title, "tex"),
                        elem,
                        RawBlock("\\end{exampleblock}", "tex"),
                    ]
                return [
                    RawBlock("\\begin{block}%s" % title, "tex"),
                    elem,
                    RawBlock("\\end{block}", "tex"),
                ]
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
