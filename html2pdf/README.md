# convert html to PDF
> convert existing HTML page to PDF document
> all examples can be used for pre-step: https://github.com/cherkavi/cheat-sheet/blob/master/jekyll.md#docker-container-start
## [Pandoc](https://pandoc.org/MANUAL.html)
```sh
## https://hub.docker.com/u/pandoc
# DOCKER_PANDOC=pandoc/core
DOCKER_PANDOC=pandoc/latex

# converter for csv, jira, json, latex, man, markdown, odt, rtf, twiki, vimwiki
FORMAT_SRC=html 
FORMAT_DEST=pdf
docker run --rm --link $DOCKER_JEKYLL:destination --volume "$(pwd):/data" --user $(id -u):$(id -g) $DOCKER_PANDOC --read $FORMAT_SRC --write $FORMAT_DEST --request-header User-Agent:"Mozilla/5.0" http://destination:4000 --output cv.pdf

```

## [WKTHML](https://wkhtmltopdf.org/usage/wkhtmltopdf.txt)
### local installation
```sh
sudo apt-get -y install weasyprint
```
### docker installation
```sh
## https://hub.docker.com/r/surnet/alpine-wkhtmltopdf/tags
DOCKER_WKHTML=surnet/alpine-wkhtmltopdf:3.17.0-0.12.6-full
# --disable-smart-shrinking --custom-header User-Agent Mozilla/5.0 --page-size A4 
docker run --rm --link $DOCKER_JEKYLL:destination --volume "$(pwd):/data" --user $(id -u):$(id -g) $DOCKER_WKHTML http://destination:4000 /data/output.pdf
```

## Python converter
```sh
# weasyprint is an option. A possible drawback is that you'll need python on your machine.

pip install weasyprint
weasyprint in.html out.pdf
```

## [ebook-converter](https://manual.calibre-ebook.com/generated/en/ebook-convert.html)
## [unoconv](https://linux.die.net/man/1/unoconv)