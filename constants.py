"""
Various constants for attribute types, child matching expressions, etc.
"""

# Token sentinel
XHPY_SENTINEL = -1

# Type parameters
TYPE_STRING = 1
TYPE_BOOL   = 2
TYPE_INT    = 3
TYPE_LIST   = 4
TYPE_OBJECT = 5
TYPE_VAR    = 6
TYPE_ENUM   = 7
TYPE_FLOAT  = 8

# Child declaration parameters
CHILD_DECL_EMPTY = 0
CHILD_DECL_ANY = 1

# Child atom parameters
CHILD_ATOM_ANY = 0
CHILD_ATOM_PCDATA = 1
CHILD_ATOM_SPECIFIC = 2
CHILD_ATOM_CATEGORY = 3

# Child expression parameters
CHILD_EXPR_ONE = 4
CHILD_EXPR_ZERO_OR_MORE = 5
CHILD_EXPR_ZERO_OR_ONE = 6
CHILD_EXPR_ONE_OR_MORE = 7
CHILD_EXPR_CONCAT = 8
CHILD_EXPR_OR = 9

