from tika import parser
import argparse
from utils import remove_char_range, split_on_points
from regexes import r_name_vote_separator, r_non_word_characters
import re


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f',
        '--file',
        help='input pdf',
        default='/Users/Dhruv/Downloads/Sample roll call vote PDF_multiple columns[2].pdf'
    )

    return parser.parse_args()


def drop_non_word_chars(line: str):

    return re.sub(r_non_word_characters, '', line)


def replace_em_dash(line: str, rep="<sep>"):
    return re.sub(r"[-\u2014\_]", rep, line)


def combine_sep(line: str, rep="<sep>"):
    p = r"((?:{}){{2,}})".format(rep)

    return re.sub(p, rep, line)


if __name__ == '__main__':
    args = get_args()

    raw = parser.from_file(args.file)
    print(raw['content'])
    unmatched_lines = []
    matched_lines = []
    incorrect_number_of_votes = []
    irrelevant_lines = 0

    for line_no, line in enumerate(raw['content'].splitlines()):
        if line.strip() == "":
            irrelevant_lines += 1

            continue
        m = re.search(r_name_vote_separator, line)

        if m:
            print("Matched:", line)
            new_line = remove_char_range((m.start(), m.end()), line)
            name, _, votes = split_on_points(line, m.start(), m.end())
            votes = replace_em_dash(votes)
            votes = drop_non_word_chars(votes)
            votes = combine_sep(votes)
            votes = votes.split()

            if len(votes) != 5:
                unmatched_lines.append((line_no, line))
                incorrect_number_of_votes.append((line_no, line))
            matched_lines.append((line_no, name, votes))
            print("Name:", name, "\t Votes:", votes)
        else:
            unmatched_lines.append((line_no, line))
            print("Not matched")
            print(line)

    for line_no, name, votes in matched_lines:
        print(line_no, ",", name, ",", votes)
    print("total_lines:", line_no, "\tirrelevant_lines:", irrelevant_lines,
          "\tunmatched_lines:", len(unmatched_lines), "\tmatched_lines:",
          len(matched_lines), "\tincorrect_number_of_votes:",
          len(incorrect_number_of_votes))
