import xml.etree.ElementTree as ET

def parse_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    rois_info = {}

    for track in root.findall('.//track'):
        label = int(track.get('label'))
        rois_info[label] = []
        for box in track.findall('box'):
            frame_number = int(box.get('frame'))
            xtl = float(box.get('xtl'))
            ytl = float(box.get('ytl'))
            xbr = float(box.get('xbr'))
            ybr = float(box.get('ybr'))
            rois_info[label].append({"frame": frame_number, "xtl": xtl, "ytl": ytl, "xbr": xbr, "ybr": ybr})

    return rois_info
