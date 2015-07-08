owls-taunu
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
4. `git@github.com:spiiph/owls-taunu.git`

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
4. `cd ../owls-taunu && pip install -e .`
5. `cd ..`

Try the installation
--------------------

1. Create your contrib directory
    `mkdir owls-taunu/contrib/<user>`
2. Copy the environment file
    `cp owls-taunu/contrib/ohman/environment.py owls-taunu/contrib/<user>`
3. Edit the environment file to your liking
4. Copy a plotting script
    `cp owls-taunu/contrib/ohman/plot-trigger-sf.sh owls-taunu/contrib/<user>`
5. Edit the plotting script to your liking
6. Run the script
    `./owls-taunu/contrib/<user>/plot-trigger-sf.sh`

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
