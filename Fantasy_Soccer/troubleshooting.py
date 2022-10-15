import fbref_lib as fb
import multiprocessing

matches = fb.get_fbref_files(leagues="*", season="2022")

count = 0
for match in matches:
    with open(match, "r", encoding="utf-8") as fp:
        text = fp.read().replace('<!--', '').replace('-->', '')

    if count % 50 == 0:
        print(count)

    try:
    # print(match)
        fb.parse_lake_match_file(match, text)
    except Exception:
        print(match)

    count += 1