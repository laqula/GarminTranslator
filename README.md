# GarminTranslator
Language files for garmin watches and python script for translation. 
It uses Google Translate Service for translation

## Adding language file to watch
If you want to add new language, you must replace one of existing langueages files, eg:
to add polish.ln4 change it name to german.ln4 (if you have german.ln4 in your watch) and upload.

Files are stored in GARMIN\TEXT folder.

Before uploading file to the watch mark it as "Read only". Right click in Windows -> Porperties -> Read only checkbox.
You can't do that when the file is in you watch.

## Creating translations

### From one language file (faster but not recommended)
1. open "from_one_file.py" script
2. set destionation langueage code and filename
3. set source language filename and code
4. run script

Upload generated file to the watch.

It is strongly advised to review automatic translations.

### From many language files (slower, needs more effort, gives better results)
1. download source files from watch (or from other place)
2. open "from_multiple_files.py" script
3. set working directory (with language files)
4. set destination language file and codes,
5. set destination file name and values separator (it can be different in different countries, default ',')
6. set source files names and codes
7. run script
8. script will create CSV file with code and all translations
9. select one translated column as final translation
10. verify translations with other languages and change values when it's needed (you can change manually or copy from other languages)
11. after verification delete other columns (leave only code column and selected translation column)
12. save file and open it in text editor
13. replace separator with space
14. done, translation completed
15. add result to original file (if you translated only missing values)
16. upload file to watch

## Language codes
If you want to know the language code for a language you can check it on Google Translator page:
1. open url: https://translate.google.com/
2. select source and/or destination language
3. translate any word and check url, eg: https://translate.google.com/?sl=de&tl=pl&text=test&op=translate
4. 'sl' attribute is a source language code
5. 'tl' attribute is a destination language code
