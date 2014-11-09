"""
recupero todas las paginas
de todas las paginas recupero todos los links a mas info
de cada link recupero toda la info tabulada
agrego esa info a un csv
lo saco por la salida estandar
"""
import urllib
import re
import csv
import sys
from optparse import OptionParser

from lxml import etree


def unicode_csv_reader(unicode_csv_data, dialect=csv.excel, **kwargs):
    # csv.py doesn't do Unicode; encode temporarily as UTF-8:
    csv_reader = csv.reader(utf_8_encoder(unicode_csv_data),
                            dialect=dialect, **kwargs)
    for row in csv_reader:
        # decode UTF-8 back to Unicode, cell by cell:
        yield [unicode(cell, 'utf-8') for cell in row]


def utf_8_encoder(line):
    if (line is None):
        return line
    else:
        return line.encode('utf-8')


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-l", "--location", dest="locality",
                      help="The city name you will be searching in.")
    parser.add_option("-k", "--keyword",
                      help="The keyword you are searching for.")

    (options, args) = parser.parse_args()

    if not (options.locality and options.keyword):
        parser.error("locality and keyword arguments are required."
                     " -h for help.")

    baseurl = 'http://pamovil.com.ar/'
    opts = {
        'locality': "Bahia Blanca",
        'keyword': "Farmacia",
        'id': 'quebuscas',
        'x': '00445',
        'btAceptar': 'Buscar'
    }

    getparams = urllib.urlencode(opts)

    url = baseurl + "?" + getparams
    linksempresas = []
    while (url is not None):
        actualpage = etree.HTML(urllib.urlopen(url).read())
        linksempresas.extend(actualpage.xpath('//a[text()="+info"]/@href'))
        urlssiguiente = actualpage.xpath('//a[text()="Siguiente"]/@href')
        if (len(urlssiguiente) > 0):
            url = baseurl + urlssiguiente[0]
        else:
            url = None
    emailregex = re.compile('([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)')
    salida = csv.writer(sys.stdout)
    for linkempresa in linksempresas:
        try:
            actualpagetext = urllib.urlopen(baseurl + linkempresa).read()
            actualpage = etree.HTML(actualpagetext)
            divempresa = actualpage.xpath('/html/body/div')
            if len(divempresa) > 0:
                divempresa = divempresa[0]
                stringdivempresa = etree.tostring(divempresa)
                nombre = divempresa.xpath('b/text()')
                if (len(nombre) > 0):
                    nombre = nombre[0].strip()
                else:
                    nombre = None
                domicilio = divempresa.xpath('small/text()')
                if (len(domicilio) > 0):
                    domicilio = domicilio[0].strip()[11:]
                else:
                    domicilio = None
                telefono = divempresa.xpath('a[1]/@href')
                if (len(telefono) > 0):
                    telefono = telefono[0][13:]
                else:
                    telefono = None
                web = divempresa.xpath('small/text()')
                if (len(web) >= 3):
                    web = web[2].strip()
                else:
                    web = None
                email = emailregex.findall(stringdivempresa)
                if len(email) > 0:
                    email = email[0][0]
                else:
                    email = None
                googlemaps = divempresa.xpath('a[2]/@href')
                if (len(googlemaps) > 0):
                    try:
                        googlemaps = googlemaps[0]
                        firstindex = googlemaps.index('=')
                        lastindex = googlemaps.index('+')
                        lat, lon = googlemaps[
                            firstindex+1:lastindex].split(',')
                    except ValueError as e:
                        lat, lon = None, None
                else:
                    googlemaps = None
                    lat, lon = None, None

                row = [utf_8_encoder(cell) for cell in
                       [nombre, domicilio, telefono, web, email, lat, lon]]
                salida.writerow(row)
        except urllib.URLError as e:
            pass
