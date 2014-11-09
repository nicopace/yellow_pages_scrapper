yellow_pages_scrapper
=====================

This script scraps the local yellow pages site to get the business data of a specific category

To use it, you need to first install the dependencies:
```
sudo apt-get install `cat requirements.apt`
pip install -r requirements.pip
```

Get help with:
```
python script.py -h
```

To use the script:
```
python script.py -l <city> -k <keyword>
```

If the city name has spaces, remember to scape them using a backslash `\`
