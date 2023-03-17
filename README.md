jupyter_playground
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

NB: the notebooks used within create their own modules with
[nbdev.fast.ai](https://nbdev.fast.ai)

This includes:

1.  [00_core.ipynb](00_core.ipynb) - some core utility and setup.
2.  Northern Power Grids data
3.  [10_npg_data.ipynb](10_npg_data.ipynb) for etl.
4.  [11_npg.ipynb](11_npg.ipynb) for some plots of the resulting
    dataset.

## Install

After cloning:

``` sh
pip install -e jupyter_playground
```

## How to use

Some features:

``` python
import jupyter_playground.core as core

print(core.IncrementalPipeline.__doc__)
```


            A class whose instances can dynamically store functions.
            When used as a callable passes each stages return as args into each successive function.
        

``` python
print(core.DownloadContent.__doc__)
```


            Masks the repr with it's hash to avoid serialising the content.
            This stops libraries like joblib serialising large strings in input reprs
        
