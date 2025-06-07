from datetime import date
import re
from typing import List
import xml.etree.ElementTree as ET

from .speech_item import SpeechItem


class SpeechParser:

    attrib_class = 'klasse'
    class_speaker = 'redner'
    class_j1 = "J_1"
    tag_comment = 'kommentar'
    tag_name = 'name'

    @staticmethod
    def parse(xml_str: str) -> List[SpeechItem]:

        speech_date = None

        try:
            xml_root = ET.XML(SpeechParser.clean_xml(xml_str))
        except ET.ParseError as ex:
            print(ex)
            return []

        speech_date = xml_root.attrib.get('sitzung-datum')
        speech_items = []

        for topic in xml_root.iter('tagesordnungspunkt'):
            top_id = topic.attrib.get('top-id')

            for speech in topic.iter('rede'):

                speech_id = speech.attrib.get('id')
                speaker_id = None
                skip_chairman = False
                speech_type = "rede"
                text = ""

                for line in speech:
                    if line.attrib.get(SpeechParser.attrib_class) in (SpeechParser.class_speaker, SpeechParser.tag_comment):
                        skip_chairman = False

                    if line.attrib.get(SpeechParser.attrib_class) == SpeechParser.class_speaker:
                        speaker_id = line.find(
                            SpeechParser.class_speaker).get('id')
                        continue

                    if line.tag == SpeechParser.tag_name:
                        skip_chairman = True

                    if skip_chairman:
                        continue

                    text += "".join(line.itertext())
                
                text = text.strip()
                if len(text) > 0: 
                    speech_items.append(
                        SpeechItem(
                            top_id,
                            speech_id,
                            speaker_id,
                            speech_date,
                            speech_type,
                            text
                        )
                    )

        return speech_items

    @staticmethod
    def clean_xml(xml_str: str) -> str:
        # clean protected characters
        xml_str = \
            (xml_str.replace('\xa0', ' ')
                    .replace('\xad', '')
                    .replace('\u2011', '-')
                    .replace('\u2013', '-')
             )

        # remove line breaks and identing blanks
        if '\n' in xml_str:
            xml_str = re.sub('\n\s*', ' ', xml_str)

        return xml_str