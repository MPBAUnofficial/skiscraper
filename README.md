SkiScraper
=========
Retrieve info about Ski Centers in Trentino

Usage
-----
First of all, install SkiScraper

`python setup.py install`

Then, import desired modules

`from skiscraper import Cermis, Latemar, Pinzolo, SanMartino`

Now have fun

```py
cermis = Cermis()

print cermis.slopes[1].name

is_open = cermis.get_slope_by_name('Lagorai').open

print 'Lagorai is {}'.format('open' if is_open else 'closed')

if cermis.weather.temperature <= 0:
    print "Brrr, I'm freezing!"
```
