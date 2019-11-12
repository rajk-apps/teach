import re


def remove_animation(content):
    return re.sub(re.compile('<!--.*?-->'),
                  '',
                  str(content.text))


def upto_level(content, level):
    out = content.text
    for ss in [x[0] for x in
               re.findall(re.compile('(\s*.*<!--.*?level=(\d+)*.*?-->)'),  # FIXME: this is probably wrong, test it
                          str(content.text)) if float(x[1]) > level]:
        out = out.replace(ss, "")
    return out