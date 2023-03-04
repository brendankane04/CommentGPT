import difflib


# Returns True if the given line is a line comment, False otherwise
# TODO: Expand this to multiple programming languages. Multiline comments? How...?
def is_comment(line):
    line = line.strip()
    is_a_comment = False

    # If the line starts with comment-indicating characters, the line is a comment
    is_a_comment = is_a_comment or line.startswith('//')    # common in most OOP languages (C/C++, Java, Go)
    # TODO: this filter would remove scripting-style comments that begin with the word "include", might wanna fix this. Won't ruin things though
    is_a_comment = is_a_comment or (line.startswith('#') and not line.startswith('#include'))    # common in scripting languages (Python, R, Perl), also don't add includes
    is_a_comment = is_a_comment or line.startswith('--')    # SQL common style
    is_a_comment = is_a_comment or line.startswith(';')     # Assembly-style comments
    is_a_comment = is_a_comment or line.startswith('%')     # MATLAB-style comments
    is_a_comment = is_a_comment or line.startswith('!')     # Fortran-style comments
    is_a_comment = is_a_comment or line.startswith('*')     # ABAP/SAS-style comments (whatever those are...)

    return is_a_comment

def get_new_lines(original, modified):
    """
    Returns the original string with the new lines added from the modified string.
    """
    # Split the original and modified strings into lists of lines
    original_lines = original.splitlines()
    modified_lines = modified.splitlines()

    # Use difflib to compare the two lists of lines and identify the newly added lines
    differ = difflib.Differ()
    diff = list(differ.compare(original_lines, modified_lines))
    new_lines = [line for line in diff if line.startswith('+ ') or line.startswith('  ') or line.startswith('- ')]

    # get the lines that are common & are new, not ones that are changed
    filtered_lines = []
    # if the line is a subtraction ('- '), the next line is the replacement of the same line.
    # this is bad since it's an intraline change (VERY BAD)
    found_minus_block = False
    for line in new_lines:
        if found_minus_block: # iterating over block of changed lines
            if line.startswith('+ '):
                continue # altered block of bad code, skip
            elif line.startswith('  '):
                filtered_lines.append(line[2:]) # bad section of code is over, go back to normal
                found_minus_block = False
            elif line.startswith('- '):
                filtered_lines.append(line[2:]) # old code, good, add in
        else: # iterating over lines that weren't changed or new comments
            if line.startswith('+ '):
                if is_comment(line[2:]):
                    filtered_lines.append(line[2:]) # new comment
                else:
                    continue # not a comment, ignore
            elif line.startswith('  '):
                filtered_lines.append(line[2:]) # original text
            elif line.startswith('- '):
                filtered_lines.append(line[2:]) # old code, but there will be a section of altered code
                found_minus_block = True

    # Join the new original lines into a single string
    new_original_string = '\n'.join(filtered_lines)
    return new_original_string
