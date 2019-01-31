# File: voom_mode_starhash.py
# Last Modified: 2017-01-07
# Description: VOoM -- two-pane outliner plugin for Python-enabled Vim
# Website: http://www.vim.org/scripts/script.php?script_id=2657
# Author: Vlad Irnov (vlad DOT irnov AT gmail DOT com)
# License: CC0, see http://creativecommons.org/publicdomain/zero/1.0/

"""
VOoM markup mode for headlines marked with #'s (atx-headers, a subset of Markdown format).
See |voom-mode-hashes|,  ../../../doc/voom.txt#*voom-mode-starhash*

# heading level 1
##heading level 2
### heading level 3

Also supports a slash-star prefix for languages with C-style comments:

/* # heading level 1
/* ##heading level 2
/* ### heading level 3
"""

import sys
if sys.version_info[0] > 2:
        xrange = range

import re

CHAR = '#'
COMMENT_LEADER = '/* '
PREFIX1 = CHAR
PREFIX2 = COMMENT_LEADER + CHAR

HEADLINE_MATCH = re.compile(r'^(?:/\* )?(%s+)' % re.escape(CHAR)).match

def hook_makeOutline(VO, blines):
    """Return (tlines, bnodes, levels) for Body lines blines.
    blines is either Vim buffer object (Body) or list of buffer lines.
    """
    Z = len(blines)
    tlines, bnodes, levels = [], [], []
    tlines_add, bnodes_add, levels_add = tlines.append, bnodes.append, levels.append
    for i in xrange(Z):
        if (not blines[i].startswith(PREFIX1)
            and not blines[i].startswith(PREFIX2)):
            continue
        bline = blines[i]
        m = HEADLINE_MATCH(bline)
        lev = len(m.group(1))
        head = bline[m.end(1):].strip()
        tline = '  %s|%s' % ('. '*(lev-1), head)
        tlines_add(tline)
        bnodes_add(i+1)
        levels_add(lev)
    return (tlines, bnodes, levels)


def hook_newHeadline(VO, level, blnum, tlnum):
    """Return (tree_head, body_lines).
    tree_head is new headline string in Tree buffer (text after |).
    body_lines is list of lines to insert in Body buffer.
    """
    tree_head = 'NewHeadline'
    body_lines = ['%s %s' % (CHAR * level, tree_head), '']
    return (tree_head, body_lines)


def hook_changeLevBodyHead(VO, h, levDelta):
    """Increase of decrease level number of Body headline by levDelta."""
    if levDelta==0: return h

    m = HEADLINE_MATCH(h)
    level = len(m.group(1))

    new_markers = CHAR * (level + levDelta)
    remainder_of_line =  h[m.end(1):]
    line = new_markers + remainder_of_line

    if h.startswith(PREFIX2):
        return '%s%s' % (COMMENT_LEADER, line)
    else:
        return line


