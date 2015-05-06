#!/bin/zsh
source /Users/hayashitoshiki/.zprofile
PRJ_DIR="/Users/hayashitoshiki/Documents/Programming/Mercurial_Repository/Personal_Python/airport_weather/app"


case $1 in
        "init")
                workon airport_weather
                cd ${PRJ_DIR}
                pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
                pybabel init -i messages.pot -d translations -l ja
                pybabel init -i messages.pot -d translations -l en
                deactivate
                echo "fin."
                ;;
        "update")
                workon airport_weather
                cd ${PRJ_DIR}
                pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .
                pybabel update -i messages.pot -d translations
                deactivate
                echo "fin."
                ;;
        "cmp")
                workon airport_weather
                cd ${PRJ_DIR}
                pybabel compile -d translations
                deactivate
                echo "fin."
                ;;
        *)
                echo "init   : 翻訳ファイルのテンプレート作成"
                echo "update : 翻訳ファイルのテンプレート再作成"
                echo "cmp    : 翻訳ファイルを言語ファイルに反映"
                ;;
esac

