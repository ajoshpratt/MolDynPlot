#!/usr/bin/python
# -*- coding: utf-8 -*-
#   moldynplot.HSQCFigureManager.py
#
#   Copyright (C) 2015 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Generates one or more HSQC figures to specifications provided in a YAML
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
class HSQCFigureManager(FigureManager):
    """
    Manages the generation of HSQC figures.
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
        draw_subplot:
          title_kw:
            verticalalignment: bottom
          xlabel: $^{1}H$ (ppm)
          xlabel_kw:
            horizontalalignment: center
            verticalalignment: center
          ylabel: $^{15}N$ (ppm)
          ylabel_kw:
            horizontalalignment: center
            verticalalignment: center
          xticks: [5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5]
          yticks: [100,105,110,115,120,125,130,135]
          tick_params:
            direction: out
            bottom: on
            top: off
            right: off
            left: on
          grid: True
          grid_kw:
            b: True
            color: [0.8,0.8,0.8]
            linestyle: '-'
          label_kw:
            zorder: 10
            horizontalalignment: left
            verticalalignment: top
          legend_kw:
            loc: 2
            handletextpad: 0.0
            numpoints: 1
            frameon: True
        draw_dataset:
          dataset_kw:
            cls: moldynplot.Dataset.HSQCDataset
          cutoff: 0.970
          plot_kw:
            zorder: 10
          handle_kw:
            ls: none
            marker: s
            mec: black
    """
    available_presets = """
      letter:
        class: target
        inherits: letter
        draw_figure:
          left:       0.9
          sub_width:  7.8
          bottom:     0.7
          sub_height: 5.4
        draw_subplot:
          xticklabels: [5.0,'',6.0,'',7.0,'',8.0,'',9.0,'',10.0,'',11.0]
          legend: True
        draw_dataset:
          contour_kw:
            linewidths: 0.75
          handle_kw:
            ms: 8
      manuscript:
        class: target
        inherits: manuscript
        draw_figure:
          left:       0.50
          sub_width:  3.80
          right:      0.20
          bottom:     0.45
          sub_height: 2.65
          top:        0.20
        draw_subplot:
          xticklabels: [5.0,'',6.0,'',7.0,'',8.0,'',9.0,'',10.0,'',11.0]
          xlabel_kw:
            labelpad: 10
          ylabel_kw:
            labelpad: 10
        draw_dataset:
          contour_kw:
            linewidths: 0.5
          handle_kw:
            ms: 5
      presentation:
        class: target
        inherits: presentation
        draw_figure:
          left:       2.12
          sub_width:  6.00
          sub_height: 4.00
          bottom:     2.10
        draw_subplot:
          xticks: [6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0]
          xticklabels: [6,'',7,'',8,'',9,'',10]
          yticks: [105,110,115,120,125,130]
          yticklabels: [105,110,115,120,125,130]
          legend: False
        draw_dataset:
          plot_kw:
            linewidths: 1
    """

    @staticmethod
    def get_slice(collection, lower_bound, upper_bound):
        import numpy as np

        try:
            min_index = np.where(collection < lower_bound)[0][0] + 1
        except IndexError:
            min_index = collection.size
        try:
            max_index = max(np.where(collection > upper_bound)[0][-1],0)
        except IndexError:
            max_index = 0
        return slice(max_index, min_index, 1)

    def get_contour_levels(self, I, cutoff=0.9875, n_levels=10, min_level=None,
        max_level=None, **kwargs):
        """
        Generates contour levels.

        Arguments:
          I (ndarray): Intensity
          cutoff (float): Proportion of Intensity below minimum level
          n_levels (int): Number of contour levels
          min_level (float): Minimum contour level
          max_level (float): Maximum contour level; default = max(I)

        Returns:
          (ndarray): levels

        .. todo::
            - Support negative contour levels
            - Write partner function to analyze amino acid sequence,
              estimate number of peaks, and choose appropriate cutoff
        """
        import numpy as np

        I_flat    = np.sort(I.flatten())
        if min_level is None:
            min_level = I_flat[int(I_flat.size * cutoff)]
        if max_level is None:
            max_level = I_flat[-1]
        exp_int = ((max_level ** (1 / (n_levels - 1))) /
                   (min_level ** (1 / (n_levels - 1))))
        levels = np.array([min_level * exp_int ** a
                      for a in range(0, n_levels, 1)][:-1], dtype = np.int)
        return levels

    @manage_defaults_presets()
    @manage_kwargs()
    def draw_dataset(self, subplot, draw_contour=True, label=None,
        handles=None, **kwargs):
        """
        Draws a dataset on a subplot.

        Arguments:
          subplot (Axes): Axes on which to draw
          draw_pdist (bool): Draw contour
          draw_fill_between (bool): Fill between specified region for this
            dataset
          draw_mean (bool): Draw point at mean value of this dataset
          dataset_kw (dict): Keyword arguments used to passed to
            :meth:`load_dataset`
          plot_kw (dict): Keyword arguments used to configure plot
          fill_between_kw (dict): Keyword arguments used to configure
            fill_between
          pdist_kw (dict): Keyword arguments using to configure probability
            distribution
          verbose (int): Level of verbose output
          kwargs (dict): Additional keyword arguments
        """
        import numpy as np
#        from . import get_cmap
        from .myplotspec import get_cmap, get_colors, multi_get_copy

        # Cheap way to invert axes without overriding draw_subplot
        if not subplot.xaxis_inverted():
            subplot.invert_xaxis()
        if not subplot.yaxis_inverted():
            subplot.invert_yaxis()

        # Process arguments
        verbose = kwargs.get("verbose", 1)
        dataset_kw = multi_get_copy("dataset_kw", kwargs, {})
        if "infile" in kwargs:
            dataset_kw["infile"] = kwargs["infile"]
        dataset = self.load_dataset(verbose=verbose, **dataset_kw)
        if dataset is not None and hasattr(dataset, "hsqc_df"):
            hsqc = dataset.hsqc_df
        else:
            hsqc = None

        # Configure plot settings
        plot_kw = multi_get_copy("plot_kw", kwargs, {})
        get_colors(plot_kw, kwargs)

        # Plot contour
        if draw_contour:
            contour_kw = plot_kw.copy()
            contour_kw.update(kwargs.get("contour_kw", {}))
            get_colors(contour_kw)
            hsqc.index.levels[0].size
            ct_H = hsqc.index.levels[0]
            ct_N = hsqc.index.levels[1]
            ct_I = hsqc.values.reshape((hsqc.index.levels[0].size,
                     hsqc.index.levels[1].size)).T
            if "levels" not in contour_kw:
                contour_kw["levels"] = self.get_contour_levels(ct_I,
                  **kwargs)
            if "cmap" not in contour_kw:
                if "color"in contour_kw:
                    contour_kw["cmap"] = get_cmap(contour_kw.pop("color"))
            draw_contour_fill = contour_kw.pop("fill", False)
            if draw_contour_fill:
                contour = subplot.contourf(ct_H, ct_N, ct_I, **contour_kw)
            else:
                contour = subplot.contour(ct_H, ct_N, ct_I, **contour_kw)

                # Close bottom of contours
                for collection in contour.collections:
                    for path in collection.get_paths():
                        if np.all(path.vertices[0] == path.vertices[-1]):
                            try:
                                path.vertices = np.append(path.vertices,
                                  [path.vertices[1]], axis=0)
                            except IndexError:
                                continue

        # Draw handle
        if handles is not None and label is not None:
            handle_kw = plot_kw.copy()
            handle_kw.update(kwargs.get("handle_kw", {}))
            handles[label] = subplot.plot([0,0], [0,0], **handle_kw)[0]

#################################### MAIN #####################################
if __name__ == "__main__":
    HSQCFigureManager().main()
