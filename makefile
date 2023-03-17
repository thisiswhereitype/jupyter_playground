.PHONY: environment.yml

conda_lock.yml: environment.yml
	mamba env update --prune
	mamba list -e > conda_lock.yml