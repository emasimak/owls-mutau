owls-mutau
==========

OWLS implementations of the charged Higgs to tau+nu analyses

Requirements
============

* Python 2.7
* Virtualenv
* Pip

Virtualenv and Pip are Python modules that can usually be found via the
operating system package manager.

Instructions
============

Create working directory
------------------------

Create a working directory for OWLS and change to it. E.g.

  `mkdir ~/owls && cd ~/owls`

Clone components from GitHub
----------------------------

1. `git@github.com:spiiph/owls-cache.git`
2. `git@github.com:spiiph/owls-parallel.git`
3. `git@github.com:spiiph/owls-hep.git`
4. `git@github.com:spiiph/owls-mutau.git`

Create a `virtualenv`
---------------------

1. `virtualenv env --system-site-packages`
2. `source env/bin/activate`

Your prompt should now read something like

  `(env)~/owls $`

Install the OWLS python modules
-------------------------------

1. `cd owls-cache && pip install -e .`
2. `cd ../owls-parallel && pip install -e .`
3. `cd ../owls-hep && pip install -e .`
4. `cd ../owls-mutau && pip install -e .`

Try the installation
--------------------

1. Edit the environment file to your liking
    `scripts/environment.py`
2. Inspect a plotting script and edit it to your liking
    `scripts/plot-mutau-taupt.sh`
   (It might be necessary to reduce the number of regions selected for
   plotting, and also to turn off — by commenting out — plotting with
   systematic uncertainties.)
5. Inspect the model and region files in `definitions`, e.g.
    `definitions/models-2016-05-31.py`
    `definitions/regions-2016-05-31.py`
6. Run the script
    `./scripts/plot-mutau-taupt.sh`

Starting the `virtualenv` in a new shell
----------------------------------------

If you have logged out or just started a new shell in which you wish to run
OWLS, you should issue the following command to initialize the `virtualenv`

   `source env/bin/activate`

Histogram cacheing
==================

Much of the benefit of using OLWS comes from the efficient cacheing of
histograms. Once the `TTree.Draw()` function is called for a specific
expression, selection, and binning, that histogram is stored in a cache. The next time
`TTree.Draw()` would be called with the same parameters, the histogram is
instead fetched from the cache. The cacheing identifies histograms by
selection, expression, or binning, so that any change to these parameters
will result in a new histogram being drawn and cached.
