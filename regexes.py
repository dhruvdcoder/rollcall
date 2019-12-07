import re

r_name_vote_separator = r"[\.\s]+(?=(?:\.|(?:\s\.)))[\.]"
# unicode chars:
# \u2014 = em dash
r_non_word_characters = r"[\^!-\.0-9\u2014]"
