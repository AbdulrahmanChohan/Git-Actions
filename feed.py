from __future__ import annotations

from pathlib import Path
import xml.etree.ElementTree as ET

import yaml


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "feed.yaml"
OUTPUT = ROOT / "feed.xml"


def _to_length(value: str | int) -> str:
    return str(value).replace(",", "").strip()


def main() -> None:
    with SOURCE.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")

    ET.SubElement(channel, "title").text = data["title"]
    ET.SubElement(channel, "description").text = data["description"]
    ET.SubElement(channel, "language").text = data["language"]
    ET.SubElement(channel, "category").text = data["category"]

    image = ET.SubElement(channel, "image")
    ET.SubElement(image, "url").text = data["image"]
    ET.SubElement(image, "title").text = data["title"]
    ET.SubElement(image, "link").text = data["image"]

    for item in data.get("item", []):
        node = ET.SubElement(channel, "item")
        ET.SubElement(node, "title").text = item["title"]
        ET.SubElement(node, "description").text = item["description"]
        ET.SubElement(node, "pubDate").text = item["published"]
        ET.SubElement(node, "guid").text = item["file"]
        ET.SubElement(node, "enclosure", {
            "url": item["file"],
            "length": _to_length(item["length"]),
            "type": data["format"],
        })
        ET.SubElement(node, "duration").text = item["duration"]

    ET.indent(rss, space="  ")
    tree = ET.ElementTree(rss)
    tree.write(OUTPUT, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
