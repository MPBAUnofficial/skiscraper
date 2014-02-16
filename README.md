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
c = Cermis()

c.slopes[1].name

is_open = c.get_slope_by_name('Lagorai')

print 'Lagorai is {}'.format('open' if is_open else 'closed')
```
