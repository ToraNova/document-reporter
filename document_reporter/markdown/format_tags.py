# special formatting tokens to ease report writing to md

import re
import webcolors
from mistletoe.span_token import SpanToken, RawText
from mistletoe.block_token import BlockToken, tokenize

def _build_regex_ftag_pattern(tag):
    return f'<{tag}\\s*([#0-9a-zA-Z]+)?>(.*?)</{tag}>'

def _build_regex_ftag_start_pattern(tag):
    return f'<{tag}\\s*([#0-9a-zA-Z]+)?[ >\n]'

class FormatSpan(SpanToken):
    parse_group = 2

    def __init__(self, match):
        if match.group(1) is not None:
            self.format_value = match.group(1).casefold()
        else:
            self.format_value = None
        # do not define children ourselves, allow for nested formats
        #self.children = (RawText(match.group(2) if match.group(2) is not None else match.group(4)),)

class ColorSpan(FormatSpan):
    pattern = re.compile(_build_regex_ftag_pattern('c'), re.DOTALL)

    def __init__(self, match):
        super().__init__(match)
        if not self.format_value.startswith('#'):
            self.format_value = webcolors.name_to_hex(self.format_value)[1:]

class BoldSpan(FormatSpan):
    pattern = re.compile(_build_regex_ftag_pattern('b'), re.DOTALL)

class ItalicSpan(FormatSpan):
    pattern = re.compile(_build_regex_ftag_pattern('i'), re.DOTALL)

class UnderlineSpan(FormatSpan):
    pattern = re.compile(_build_regex_ftag_pattern('u'), re.DOTALL)

class StrikethroughSpan(FormatSpan):
    pattern = re.compile(_build_regex_ftag_pattern('strike'), re.DOTALL)

class FontSpan(FormatSpan):
    pattern = re.compile(_build_regex_ftag_pattern('font'), re.DOTALL)

class FormatBlock(BlockToken):

    _end_cond = None

    def __init__(self, lines):
        start_token = re.search(_build_regex_ftag_start_pattern(self.tag), lines[0])
        self.format_value = start_token.group(1).casefold()
        lines[0] = lines[0][start_token.span()[1]:]
        end_token =re.search(f'</{self.tag}>', lines[-1])
        lines[-1] = lines[-1][:end_token.span()[0]]
        super().__init__(lines, tokenize)

    @classmethod
    def start(cls, line):
        stripped = line.lstrip()
        if len(line) - len(stripped) >= 4:
            return False

        # rule 1: <pre>, <script> or <style> tags, allow newlines in block
        match_obj = re.match(_build_regex_ftag_start_pattern(cls.tag), stripped)
        cls._end_cond = f'</{cls.tag}>'
        if match_obj is not None:
            return 1
        return False

    @classmethod
    def read(cls, lines):
        # note: stop condition can trigger on the starting line
        line_buffer = []
        for line in lines:
            line_buffer.append(line)
            if cls._end_cond is not None:
                if cls._end_cond in line.casefold():
                    break
            elif line.strip() == '':
                line_buffer.pop()
                break
        return line_buffer

class AlignBlock(FormatBlock):
    tag = 'align'