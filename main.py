import gdown
import os
import re
import sys


def regex_compile(word_dict: list) -> re.Pattern:
    print("Coverting dictionary into regex format")
    pattern = '|'.join(word_dict)
    print("Compiling regex")
    rule = re.compile(pattern)
    return rule


def split_chinese_sentence(sentence: str, rule: re.Pattern) -> list:
    words = []
    index = 0
    while index < len(sentence):
        match = rule.search(sentence[index:])
        # print(sentence[index:])
        if match:
            # print(match.span())
            if match.span()[0] == 0:
                word = match.group()
                words.append(word)
                index += len(word)
            else:
                words.append(sentence[index:index + match.span()[0]])
                words.append(sentence[index + match.span()[0]:index + match.span()[1]])
                index += match.span()[1]
        else:
            words.append(sentence[index:])
            break
    return words


def main():
    # Read dictionary
    words_path = "dict_no_space.txt"
    if not os.path.isfile(words_path):
        print(f"Warning, {words_path} doesn't exist, download from Google Drive automatically.")
        gdown.download("https://drive.google.com/file/d/1XD1BhHda7qsX7vu2ec0ZXIBv5RP8pauo/view?usp=sharing", output=f"./{words_path}", fuzzy=True)
    with open(words_path, "r", encoding="utf-8") as f:
        words = f.read()
    words = words.split('\n')
    if words[-1] == "":
        words = words[:-1]
    words = list(words)
    words = sorted(words, key=lambda x: len(x), reverse=True)

    # Segmentation
    sentence = "這裡是MI2S實驗室,位於資訊工程學系的65802室" if len(sys.argv) == 1 else sys.argv[1]
    rule = regex_compile(words)
    result = split_chinese_sentence(sentence, rule)
    print(result)


if __name__ == "__main__":
    main()
