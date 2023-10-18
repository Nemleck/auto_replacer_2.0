from requests import get

def get_wiki_info(theme: str):
    res = get(f"https://fr.wikipedia.org/wiki/{theme.lower().capitalize()}")

    start_text = '</head> <body class="skin-vector skin-vector-search-vue mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject mw-editable page-Dauphin rootpage-Dauphin skin-vector-2022 action-view"><a class="mw-jump-link" href="#bodyContent">Aller au contenu</a> '
    start_text = res.text.replace("\n","").replace("\t", "")

    text = [""]
    in_p = False
    main_content = start_text.split('id="mw-content-text"')[1].split(" homonymie ")[-1]
    oppened = False

    curr_i = 0

    for char_i in range(len(main_content)):
        char = main_content[char_i]

        if main_content[char_i:char_i+3].startswith("<p>"):
            in_p = True
            continue
        elif main_content[char_i:char_i+4].startswith("</p>"):
            # print(main_content[char_i:char_i+4])
            
            in_p = False
            text.append("")
            text[curr_i] = text[curr_i].replace("&#160;", " ")

            curr_i += 1
            if curr_i > 5:
                break

            continue
        
        if in_p:
            if char == "<":
                oppened = True
            elif char == ">":
                oppened = False
                continue
            elif char == "p" and main_content[char_i+1] == ">":
                continue

            if not oppened:
                text[curr_i] += main_content[char_i]

    kept_part = 0
    for i in range(len(text)):
        if (i != 0 and text[i] != "" and not "homonyme" in text[i]) and not "répertorie" in text[i]:
            kept_part = i
            break
    
    return [text[kept_part], text[kept_part+1]]