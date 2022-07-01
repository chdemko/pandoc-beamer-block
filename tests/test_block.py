# This Python file uses the following encoding: utf-8

from unittest import TestCase

from panflute import convert_text, Para, Image

import pandoc_beamer_block


class BlockTest(TestCase):
    @classmethod
    def conversion(cls, markdown, fmt="markdown"):
        doc = convert_text(markdown, standalone=True)
        doc.format = fmt
        pandoc_beamer_block.main(doc)
        return doc

    def test_simple(self):
        doc = BlockTest.conversion(
            """
---
pandoc-beamer-block:
  - classes: ['class1', 'class2']
---
::: {.class1 .class2}
:::
            """,
            "beamer",
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="latex",
            extra_args=["--wrap=none"],
        )
        self.assertIn("\\begin{block}", text)
        self.assertIn("\\end{block}", text)

    def test_title(self):
        doc = BlockTest.conversion(
            """
---
pandoc-beamer-block:
  - classes: ['class1', 'class2']
---
::: {.class1 .class2 title="My Title"}
:::
            """,
            "beamer",
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="latex",
            extra_args=["--wrap=none"],
        )
        self.assertIn("\\begin{block}{My Title}", text)
        self.assertIn("\\end{block}", text)

    def test_alert(self):
        doc = BlockTest.conversion(
            """
---
pandoc-beamer-block:
  - classes: ['class1', 'class2']
    type: alert
---
::: {.class1 .class2}
:::
            """,
            "beamer",
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="latex",
            extra_args=["--wrap=none"],
        )
        self.assertIn("\\begin{alertblock}", text)
        self.assertIn("\\end{alertblock}", text)

    def test_example(self):
        doc = BlockTest.conversion(
            """
---
pandoc-beamer-block:
  - classes: ['class1', 'class2']
    type: example
---
::: {.class1 .class2}
:::
            """,
            "beamer",
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="latex",
            extra_args=["--wrap=none"],
        )
        self.assertIn("\\begin{exampleblock}", text)
        self.assertIn("\\end{exampleblock}", text)

    def test_title_complex(self):
        doc = BlockTest.conversion(
            """
---
pandoc-beamer-block:
  - classes: ['class1', 'class2']
---
::: {.class1 .class2 title="**My Title**"}
:::
            """,
            "beamer",
        )
        text = convert_text(
            doc,
            input_format="panflute",
            output_format="latex",
            extra_args=["--wrap=none"],
        )
        self.assertIn("\\begin{block}{\\textbf{My Title}}", text)
        self.assertIn("\\end{block}", text)
