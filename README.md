# ML

## Jupyter lab installation on macos

- install miniconda on https://docs.conda.io/en/latest/miniconda.html

- To get rid of the annoying prefix (base) in your terminal:

```
conda config --set auto_activate_base False
```

- Install your dependencies with conda:
```
conda install -c conda-forge jupyterlab matplotlib scikit-learn pandas
```
- export /home/\<user\>/opt/miniconda/bin in path

- Run `jupyter lab --ip=<your host>`
