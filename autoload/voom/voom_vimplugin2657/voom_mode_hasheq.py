# File: voom_mode_hasheq.py
# Last Modified: 2018-05-17
# Description: VOoM -- two-pane outliner plugin for Python-enabled Vim
# Website: http://www.vim.org/scripts/script.php?script_id=2657
# Authors:
#   This file: Mabel Cow (mabel AT baffledcow DOT com)
#   Original file: Vlad Irnov (vlad DOT irnov AT gmail DOT com)
# License: CC0, see http://creativecommons.org/publicdomain/zero/1.0/
"""
hasheq: A VOoM markup mode for headlines marked as `# = `, `# == `, ...

For example:
 # = Heading level 1
 # == Heading level 2
 # === Heading level 3
"""

# = Imports

import re

# = Exports

__all__ = (
    "hook_changeLevBodyHead",
    "hook_makeOutline",
    "hook_newHeadline",
    )


# = Interface

# == Create the outline

def hook_makeOutline(_, body_lines):  # noqa: E501 # pylint: disable=invalid-name
    """
    Return (tree_lines, body_nodes, levels) for body lines body_lines.

    Parameter body_lines is either a Vim buffer object (body) or a list
    of buffer lines.
    """
    tree_lines = []
    body_nodes = []
    levels = []

    for i in generate_range(len(body_lines)):
        if not body_lines[i].startswith(_LEADER):
            continue

        match = _HEADING_MATCH(body_lines[i])
        if not match:
            continue

        level = len(match.group(1))
        heading_text = match.group(2)
        tree_line = make_tree_line(level, heading_text)

        tree_lines.append(tree_line)
        body_nodes.append(i + 1)
        levels.append(level)

    return (tree_lines, body_nodes, levels)


# == Add a heading

def hook_newHeadline(_, level, __, ___):  # noqa: E501 # pylint: disable=invalid-name
    """
    Return (heading_text, body_lines).

    heading_text is new headline string in Tree buffer (text after |).
    body_lines is list of lines to insert in body buffer.
    """
    heading_text = 'NewHeadline'
    body_lines = [
        make_heading_line(level, heading_text),
        '',
        ]
    return (heading_text, body_lines)


# == Change heading level

def hook_changeLevBodyHead(_, heading_line, level_delta):  # noqa: E501 # pylint: disable=invalid-name
    """
    Increase or decrease the level number of a body headline by
    level_delta.
    """
    if level_delta == 0:
        return heading_line

    match = _HEADING_MATCH(heading_line)
    level = len(match.group(1))
    heading_text = match.group(2)

    new_level = level + level_delta
    assert new_level >= 0

    return make_heading_line(new_level, heading_text)


# = Implementation

# == Module constants

_LEADER = "# "
_LEVEL = "="
_HEADING_MATCH = re.compile(r"^# (=+)\s+(\S.*)\S*$").match


# == Output formatting

def make_heading_line(level, heading_text):
    """Return a heading line suitable for inclusion in body text."""
    return '%s%s %s' % (_LEADER, _LEVEL * level, heading_text)


def make_tree_line(level, heading_text):
    """Return a tree entry representing a heading at a particular level."""
    return '  %s|%s' % ('. ' * (level - 1), heading_text)


# == Utilities

def generate_range(stop):
    """Emulate Python 3's range() function."""
    i = 0
    while i < stop:
        yield i
        i += 1
