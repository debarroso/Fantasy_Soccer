import fbref_lib as fb

matches = fb.get_fbref_files(leagues="FA_Cup", season="*")

for match in matches:
    with open(match, "r", encoding="utf-8") as fp:
        text = fp.read().replace('<!--', '').replace('-->', '')

    try:
    # print(match)
        fb.parse_lake_match_file(match, text)
    except Exception:
        print(match)