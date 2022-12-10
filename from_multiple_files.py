import json
import os
import requests
import urllib

# languageFilesDir = fr'C:\garmin_language_files'
languageFilesDir = fr'D:\tmp\Vivoactive4_przerobiony_german.lnk_na PL\va4'
destLanguageFileName = 'polish.ln4'
destLangShortcut = 'pl'
translationsSeparator = ';'
resultFileName = 'translations.csv'

# languages files used as a source for translation (file name and google language code)
langFiles = {
    'german.ln4': 'de',
    'swedish.ln4': 'sv',
    'spanish.ln4': 'es',
    'portugue.ln4': 'pt',
    'norwegia.ln4': 'no',
    'italian.ln4': 'it',
    'french.ln4': 'fr',
    'finnish.ln4': 'fi',
    'dutch.ln4': 'nl',
    'danish.ln4': 'da',
    'brazilia.ln4': 'pt'
}

# list of codes that exists in destination file
# if file exists only missing codes are translated
# if file not exists all codes are translated
destLangCodes = []
destLangFilePath = os.path.join(languageFilesDir, destLanguageFileName)
if os.path.exists(destLangFilePath):
    destLangFile = open(destLangFilePath, 'r', encoding='utf8')
    for line in destLangFile.readlines()[1:]:
        lineSplit = line.split(' ')
        if lineSplit:
            destLangCodes.append(lineSplit[0])

# translating all missing texts, from all languages
translations = []
for langFile, langShortcut in langFiles.items():
    langFilePath = os.path.join(languageFilesDir, langFile)
    langFile = open(langFilePath, 'r', encoding='utf8')
    for line in langFile.readlines()[1:]:
        lineSplit = line.split(' ')
        if lineSplit:
            code = lineSplit[0]
            if code not in destLangCodes:
                text = line[len(code)+1:].rstrip()

                response = requests.get(
                    f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={langShortcut}"
                    f"&tl={destLangShortcut}&dt=t&q={urllib.parse.quote_plus(text)}")
                translation = json.loads(response.text)[0][0][0]

                print(f'{code} {text} -> {translation}')
                translations.append((code, text, translation))

# writing translations to CSV file
if os.path.exists(resultFileName):
    os.remove(resultFileName)
resultFile = open(os.path.join(languageFilesDir, resultFileName), 'w', encoding='utf-8-sig')

translatedCodes = []
for code, text, translation in translations:
    if code in translatedCodes:
        continue

    allTranslations = [item for item in translations if item[0] == code]
    result = fr'{code}{translationsSeparator}'
    print(fr'{result}', end='')
    resultFile.write(result)
    for allTranslation in allTranslations:
        result = fr'{allTranslation[1]}{translationsSeparator}{allTranslation[2]}{translationsSeparator}'
        print(result, end='')
        resultFile.write(result)
    print()
    resultFile.write('\n')
    translatedCodes.append(code)

