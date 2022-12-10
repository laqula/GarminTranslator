import json
import os

import requests
import urllib

languageFilesDir = fr'C:\garmin_language_files'

# file to get existing translation, if you want to add missing translations
# can have any value if you want to translate everything
destLanguageFileName = 'polish.ln4'
destLangShortcut = 'pl'
# file name to write translations, can be same as destLanguageFileName if you want to append new translations
# it is better to write result in separate file, review, correct and paste to destination
resultFileName = 'polish_new.ln4'

sourceLanguageFileName = 'german.ln4'
sourceLangShortcut = 'de'

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

# translating all missing texts, from source language file
translations = []
langFilePath = os.path.join(languageFilesDir, sourceLanguageFileName)
langFile = open(langFilePath, 'r', encoding='utf8')
sourceLangFileHeader = langFile.readline()
for line in langFile.readlines()[1:]:
    lineSplit = line.split(' ')
    if lineSplit:
        code = lineSplit[0]
        if code not in destLangCodes:
            text = line[len(code)+1:].rstrip()

            response = requests.get(
                f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={sourceLangShortcut}"
                f"&tl={destLangShortcut}&dt=t&q={urllib.parse.quote_plus(text)}")
            translation = json.loads(response.text)[0][0][0]

            print(f'{code} {text} -> {translation}')
            translations.append((code, text, translation))

# writing translations file
resultFilePath = os.path.join(languageFilesDir, resultFileName)
resultFileExists = os.path.exists(resultFilePath)
resultFile = open(resultFilePath, 'a', encoding='utf-8-sig')

if not resultFileExists:
    resultFile.write(sourceLangFileHeader)

translatedCodes = []
for code, text, translation in translations:
    if code in translatedCodes:
        continue

    result = fr'{code} {translation}'
    print(fr'{result}')
    resultFile.write(f'{result}\n')

    translatedCodes.append(code)

