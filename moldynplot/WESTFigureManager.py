#!/usr/bin/python
# -*- coding: utf-8 -*-
#   moldynplot.TimeSeriesFigureManager.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Generates one or more time series figures to specifications in a YAML
file.
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
if __name__ == "__main__":
    __package__ = str("moldynplot")
    import moldynplot
from .myplotspec.FigureManager import FigureManager
from .myplotspec.manage_defaults_presets import manage_defaults_presets
from .myplotspec.manage_kwargs import manage_kwargs
################################### CLASSES ###################################
class WESTFigureManager(FigureManager):
    """
    Manages the generation of time series figures.

    .. image:: _static/p53/rmsd.png
    """

    defaults = """
        draw_figure:
          subplot_kw:
            autoscale_on: False
            axisbg: none
          multi_tick_params:
            left: on
            right: off
            bottom: on
            top: off
          shared_legend: True
          shared_legend_kw:
            spines: False
            handle_kw:
              ls: none
              marker: s
              mec: black
            legend_kw:
              frameon: False
              loc: 9
              numpoints: 1
              handletextpad: 0
              borderaxespad: 0
        draw_subplot:
          title_kw:
            verticalalignment: bottom
          xlabel: Time
          tick_params:
            direction: out
            left: on
            right: off
            bottom: on
            top: off
          grid: True
          grid_kw:
            b: True
            color: [0.8,0.8,0.8]
            linestyle: '-'
          label_kw:
            zorder: 10
            horizontalalignment: left
            verticalalignment: top
        draw_dataset:
          dataset_kw:
            cls: moldynplot.Dataset.WESTEfficiencyDataset
          partner_kw:
            position: right
            y2label_kw:
              rotation: 270
              verticalalignment: bottom
            tick_params:
              direction: out
              bottom: on
              top: off
              right: off
              left: off
            grid: True
            grid_kw:
              b: True
              color: [0.8,0.8,0.8]
              linestyle: '-'
            xticks:
            tick_params:
              direction: out
              bottom: on
              top: off
              right: off
              left: off
          plot_kw:
            zorder: 10
          fill_between_kw:
            color: [0.7, 0.7, 0.7]
            lw: 0
          handle_kw:
            ls: none
            marker: s
            mec: black
          mean_kw:
            ls: none
            marker: o
            mec: black
            zorder: 11
    """

    available_presets = """
      natcon:
        class: content
        help: "% Native contacts vs. time"
        draw_subplot:
          ylabel: "% Native Contacts"
          yticks:      [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
          yticklabels: [0,10,20,30,40,50,60,70,80,90,100]
        draw_dataset:
          column: percent_native_contacts
          dataset_kw:
            cls: moldynplot.Dataset.NatConTimeSeriesDataset
            downsample_mode: mean
          partner_kw:
            yticks: [0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0]
          plot_kw:
            drawstyle: steps
      rmsd:
        class: content
        help: Root Mean Standard Deviation (RMSD)
        draw_subplot:
          ylabel: RMSD (Å)
          yticks: [0,2,4,6,8,10]
        draw_dataset:
          column: rmsd
          partner_kw:
            yticks: [0,2,4,6,8,10]
          dataset_kw:
            cls: moldynplot.Dataset.TimeSeriesDataset
            calc_pdist: True
            pdist_kw:
              bandwidth: 0.1
              grid: !!python/object/apply:numpy.linspace [0,10,1000]
            read_csv_kw:
              header: 0
              names: [frame, rmsd]
      rg:
        class: content
        help: Radius of gyration (Rg)
        draw_figure:
          multi_yticklabels: [0,5,10,15,20,25,30]
        draw_subplot:
          ylabel: $R_g$ (Å)
          yticks: [0,5,10,15,20,25,30]
        draw_dataset:
          column: rg
          partner_kw:
            yticks: [0,5,10,15,20,25,30]
          dataset_kw:
            cls: moldynplot.Dataset.TimeSeriesDataset
            calc_pdist: True
            pdist_kw:
              bandwidth: 0.1
              grid: !!python/object/apply:numpy.linspace [0,30,1000]
            read_csv_kw:
              delim_whitespace: True
              header: 0
              names: [frame, rg, rgmax]
      rotdif:
        class: content
        help: Rotational correlatio time (τc)
        draw_subplot:
          ylabel: $τ_c$ (ns)
          yticks: [0,5,10,15]
        draw_dataset:
          column: rotdif
          partner_kw:
            yticks: [0,5,10,15]
          dataset_kw:
            cls: moldynplot.Dataset.TimeSeriesDataset
            calc_pdist: True
            pdist_kw:
              bandwidth:
                rotdif: 0.2
      presentation:
        class: target
        inherits: presentation
        draw_figure:
          left:       1.20
          sub_width:  7.00
          bottom:     3.10
          sub_height: 3.00
          shared_legend: True
          shared_legend_kw:
            left:       1.20
            sub_width:  7.00
            bottom:     1.90
            sub_height: 0.50
            legend_kw:
              labelspacing: 0.0
              ncol: 5
        draw_dataset:
          partner_kw:
            sub_width: 1.2
            title_fp: 18r
            xlabel_kw:
              labelpad: 20
            label_fp: 18r
            tick_fp: 14r
            xticks:
            lw: 2
            tick_params:
              length: 3
              pad: 6
              width: 2
          handle_kw:
            ms: 12
            mew: 2
      manuscript:
        class: target
        inherits: manuscript
        draw_figure:
          left:       0.50
          sub_width:  4.40
          wspace:     0.10
          right:      0.20
          bottom:     0.70
          sub_height: 1.80
          hspace:     0.10
          top:        0.25
          title_kw:
            top: -0.1
          shared_legend_kw:
            left:       0.50
            sub_width:  4.40
            bottom:     0.00
            sub_height: 0.30
            handle_kw:
              ms: 5
            legend_kw:
              labelspacing: 0.5
              legend_fp: 7r
              ncol: 6
        draw_subplot:
          xlabel_kw:
            labelpad: 3
          ylabel_kw:
            labelpad: 6
          draw_label: True
          label_kw:
            border_lw: 1
            xabs:  0.020
            yabs: -0.025
        draw_dataset:
          partner_kw:
            wspace:    0.10
            sub_width: 0.80
            title_fp: 8b
            xlabel_kw:
              labelpad: 8.5
            label_fp: 8b
            tick_fp: 6r
            tick_params:
              length: 2
              pad: 3
              width: 1
          plot_kw:
            lw: 1
          handle_kw:
            ms: 6
            mew: 1
          mean_kw:
            ms: 2
      notebook:
        class: target
        inherits: notebook
        draw_figure:
          left:       0.60
          sub_width:  4.40
          right:      0.20
          bottom:     1.00
          sub_height: 1.80
          top:        0.30
          shared_legend: True
          shared_legend_kw:
            left:       0.60
            sub_width:  4.40
            right:      0.20
            bottom:     0.00
            sub_height: 0.50
            legend_kw:
              labelspacing: 0.5
              legend_fp: 8r
              ncol: 2
        draw_dataset:
          plot_kw:
            lw: 1.0
          partner_kw:
            sub_width: 0.8
            title_fp: 10b
            xlabel_kw:
              labelpad:  12.5
            label_fp: 10b
            tick_fp: 8r
            xticks:
            tick_params:
              length: 2
              pad: 6
              width: 1
      presentation_three:
        draw_figure:
         ncols:      3
         fig_width:  10.00
         left:        1.00
         sub_width:   2.50
         wspace:      0.50
         right:       0.50
         fig_height:  7.50
         bottom:      3.00
         sub_height:  2.50
         top:         2.00
         shared_legend: True
         shared_legend_kw:
           left:       7.00
           sub_width:  3.00
           sub_height: 2.00
           bottom:     0.00
           #spines:     True
           legend_kw:
             frameon:      False
             labelspacing: 0.5
             loc:          lower right
             #mode:         expand
             ncol:         3
             fontsize:     10
    """

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_dataset(self, subplot, label=None, column=None, handles=None,
        draw_fill_between=False, draw_mean=False,
        draw_plot=True, **kwargs):
        """
        Draws a dataset on a subplot.

        Loaded dataset should have attribute `westefficiency_df`

        Arguments:
          subplot (Axes): :class:`Axes<matplotlib.axes.Axes>` on
            which to draw
          dataset_kw (dict): Keyword arguments passed to
            :meth:`load_dataset
            <myplotspec.FigureManager.FigureManager.load_dataset>`
          plot_kw (dict): Keyword arguments passed to methods of
            :class:`Axes<matplotlib.axes.Axes>`
          draw_plot (bool): Draw plot
          draw_pdist (bool): Draw probability distribution
          draw_fill_between (bool): Fill between specified region for this
            dataset
          draw_mean (bool): Draw point at mean value value of
            probability distribution
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments
        """
        from warnings import warn
        import numpy as np
        from .myplotspec import get_colors, multi_get_copy

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        dataset_kw = multi_get_copy("dataset_kw", kwargs, {})
        #if "infile" in kwargs:
        #    dataset_kw["infile"] = kwargs["infile"]
        dataset = self.load_dataset(verbose=verbose, **dataset_kw)
        if dataset is not None and hasattr(dataset, "westefficiency_df"):
            westefficiency = dataset.westefficiency_df
            print(westefficiency)
        else:
            westefficiency = None

        # Configure plot settings
        plot_kw = multi_get_copy("plot_kw", kwargs, {})
        get_colors(plot_kw, kwargs)

        if "lw" in kwargs:
            #kwargs['lw'] = 0
            plot_kw['lw'] = kwargs['lw']
        if 'hatch' in kwargs:
            plot_kw['hatch'] = kwargs['hatch']
        if 'edgecolor' in kwargs:
            plot_kw['edgecolor'] = str(kwargs['edgecolor'])

        # Draw plot
        if draw_plot:
            #if verbose >= 2:
            #    print("mean  {0}: {1:6.3f}".format(column,
            #      timeseries[column].mean()))
            #    print("stdev {0}: {1:6.3f}".format(column,
            #      timeseries[column].std()))
            print(kwargs['index'], [westefficiency])
            #plot = subplot.bar(int(kwargs['index']), [westefficiency], width=0.8, align='center', **plot_kw)
            plot = subplot.bar(int(kwargs['index']), [westefficiency], width=0.8, align='center', **plot_kw)
            #subplot.set_xlim(kwargs['xbound'])
            #subplot.set_ylim(kwargs['ybound'])
            handle_kw = multi_get_copy("handle_kw", kwargs, {})
            #handle_kw["mfc"] = plot.get_color()
            handle = subplot.plot([-10, -10], [-10, -10], **handle_kw)[0]
            if handles is not None and label is not None:
                handles[label] = handle

#################################### MAIN #####################################
if __name__ == "__main__":
    WESTFigureManager().main()
