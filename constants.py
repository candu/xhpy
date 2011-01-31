"""
Various constants for attribute types, child matching expressions, etc.
"""

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

# Child expression parameters
CHILD_EXPR_ONE = 0
CHILD_EXPR_ZERO_OR_MORE = 1
CHILD_EXPR_ZERO_OR_ONE = 2
CHILD_EXPR_ONE_OR_MORE = 3
CHILD_EXPR_CONCAT = 4
CHILD_EXPR_OR = 5

# Child rule parameters
CHILD_RULE_ANY = 1
CHILD_RULE_PCDATA = 2
CHILD_RULE_SPECIFIC = 3
CHILD_RULE_CATEGORY = 4
CHILD_RULE_NESTED = 5
