import yaml

import pikepdf
from pikepdf import OutlineItem


def create_item(item: dict[str, str]) -> OutlineItem:
    return OutlineItem(title=item["title"], destination=int(item["page"]) - 1)


def create_toc(toc: dict) -> OutlineItem:
    return create_item(toc)


def create_preface(preface: dict) -> OutlineItem:
    return create_item(preface)


def create_part(part: dict) -> OutlineItem:
    part_item = create_item(part)
    for chapter in part["chapters"]:
        try:
            part_item.children.append(create_chapter(chapter))
        except KeyError:
            # review part
            part_item.children.append(create_item(chapter))

    return part_item


def create_chapter(chapter: dict) -> OutlineItem:
    chapter_item = create_item(chapter)
    for section in chapter["sections"]:
        chapter_item.children.append(create_item(section))
    return chapter_item


def create_appendix(appendixes: list[dict]) -> list[OutlineItem]:
    appendix_items = []
    for appendix in appendixes:
        appendix_item = create_item(appendix)
        appendix_items.append(appendix_item)

    return appendix_items


if __name__ == "__main__":
    pdf = pikepdf.open("./book.pdf")
    with open("./outline.yaml", "r") as f:
        outline_input = yaml.safe_load(f)

    with pdf.open_outline() as outline:
        toc = create_toc(outline_input["toc"])
        preface = create_preface(outline_input["preface"])
        outline_parts: list[OutlineItem] = [
            create_part(part) for part in outline_input["parts"]
        ]
        appendixies = create_appendix(outline_input["appendixes"])

        # set the outline
        for item in [toc] + [preface] + outline_parts + appendixies:
            outline.root.append(item)

    pdf.save("output.pdf")
