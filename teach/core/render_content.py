import re
import urllib.parse


class FormatParser:

    default_format = 'md'

    format_choices = ['md', 'html', 'python']

    @staticmethod
    def _reduce_to_level(text: str,
                         upto_level: int):
        for ss in [x[0] for x in
                   re.findall('(\s*.*<!--.*?level=(\d+)*.*?-->)',
                              text) if float(x[1]) > upto_level]:
            text = text.replace(ss, "")
        return text

    @classmethod
    def render(cls,
               content,
               upto_level=0,
               animate=True):

        out_text = content.text

        if content.format == 'md':

            if upto_level > 0:
                out_text = cls._reduce_to_level(out_text,
                                                upto_level)

            if not animate:
                out_text = re.sub('<!--.*?-->',
                                  '',
                                  out_text)
        elif content.format == 'python':
            link = get_pythontutor_link(out_text)

            out_text = '\n'.join(
                ['[**pythontutor**]({})'.format(link),
                 '```python',
                 out_text,
                 '```'
                 ]
            )
        elif content.format == 'iframe':
            out_text = '<iframe width="1000" height="600" frameborder="0" src="{}"> </iframe>'.format(out_text)
        elif content.format == 'img':
            out_text = '<img src="{}">'.format(out_text)

        return out_text


def get_pythontutor_link(code,
                         iframe=False,
                         height=400,
                         width=350):
    urlsafe_code = urllib.parse.quote(code)

    code_frame = ['http://www.pythontutor.com/{}.html'.format('iframe-embed'
                                                              if iframe
                                                              else 'visualize'),
                  '#code=',
                  urlsafe_code]
    if iframe:
        code_frame += [
            '&codeDivHeight={}'.format(height),
            '&codeDivWidth={}'.format(width)
        ]

    code_frame += [
        '&cumulative=false',
        '&curInstr=0'
        '&heapPrimitives=nevernest',
        '&mode=display',
        '&origin=opt-frontend.js',
        '&py=3',
        '&rawInputLstJSON=%5B%5D',
        '&textReferences=false'
    ]

    return ''.join(code_frame)

