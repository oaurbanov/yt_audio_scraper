# Tests

```
> py.test test_audio_analyser.py

# test_scraper is not automated
> python test_scraper.py
```

## Useful

```
# To match funcs with method1 substring on its name
> py.test -k method1 -v


@pytest.mark.myOne
def test_method():
	assert ...
> py.test -m myOne 


@pytest fixture
def inputs():
    return [0,1,2]
def test_method(inputs):
	assert ...
> py.test test_file.py
```


## Deps:

```
conda create --name scraper37 python=3.7
conda activate scraper37

conda install -c conda-forge youtube-dl
conda install -c conda-forge librosa

conda install -c anaconda pytest

conda install -c conda-forge pydub
conda install -c anaconda scipy
```

## Refs:

- https://gist.github.com/kwmiebach/3fd49612ef7a52b5ce3a
