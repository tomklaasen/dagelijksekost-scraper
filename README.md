# dagelijksekost-scraper

Reads the full recipe instructions from a [Dagelijkse Kost](https://dagelijksekost.vrt.be) page.

That page's JSON-LD only lists the first **two** `HowToStep` items, so any scraper relying on it
ends up with a two-step recipe. All steps do sit in the page, in the streamed Next.js RSC payload
under `"recipeParts"`. [recipe-scrapers](https://github.com/hhursev/recipe-scrapers) has a fallback
for exactly this, but it still expects the site's older `{"0": "...", "1": "..."}` format instead of
today's step objects, so it silently returns the two-step version.

## Usage

```python
from dagelijksekost import directions

steps = directions(html)   # one step per line, or None if the payload isn't there
```

A step's tip, when it has one, follows it on its own `Tip: ...` line. What to do when the payload is
missing is left to the caller — falling back to `recipe_scrapers` is usually the right move.

No runtime dependencies; pass in the page's HTML yourself.

## Install

```
pip install "dagelijksekost-scraper @ git+https://github.com/tomklaasen/dagelijksekost-scraper.git"
```

## Tests

```
python -m unittest discover tests
```

They run against a saved copy of a recipe page in `tests/fixtures/`, so no network access is needed.
