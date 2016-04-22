# -*- coding: utf-8 -*-
#   moldynplot.ExperimentDataset.py
#
#   Copyright (C) 2015-2016 Karl T Debiec
#   All rights reserved.
#
#   This software may be modified and distributed under the terms of the
#   BSD license. See the LICENSE file for details.
"""
Manages cpptraj datasets
"""
################################### MODULES ###################################
from __future__ import absolute_import,division,print_function,unicode_literals
from .myplotspec.Dataset import Dataset
################################### CLASSES ###################################
class CorrDataset(Dataset):

    @classmethod
    def get_cache_key(cls, *args, **kwargs):
        """
        Generates tuple of arguments to be used as key for dataset
        cache.
        """
        import six
        from .myplotspec import multi_get_copy

        x_kw = multi_get_copy(["x", "x_kw"], kwargs, {})
        x_cls = x_kw.get("cls", Dataset)
        if isinstance(x_cls, six.string_types):
            mod_name = ".".join(x_cls.split(".")[:-1])
            x_cls_name   = x_cls.split(".")[-1]
            mod = __import__(mod_name, fromlist=[x_cls_name])
            x_cls = getattr(mod, x_cls_name)

        y_kw = multi_get_copy(["y", "y_kw"], kwargs, {})
        y_cls = y_kw.get("cls", Dataset)
        if isinstance(y_cls, six.string_types):
            mod_name = ".".join(y_cls.split(".")[:-1])
            y_cls_name   = y_cls.split(".")[-1]
            mod = __import__(mod_name, fromlist=[y_cls_name])
            y_cls = getattr(mod, y_cls_name)

        return (cls, x_cls.get_cache_key(**x_kw), y_cls.get_cache_key(**y_kw))

    def __init__(self,
        verbose=1, debug=0, **kwargs):
        import numpy as np
        import pandas as pd
        from .myplotspec import multi_get_copy
        pd.set_option('display.width', 1000)

        # Load
        x_kw = multi_get_copy(["x", "x_kw"], kwargs, {})
        x_dataset = self.load_dataset(verbose=verbose, debug=debug, **x_kw)
        x_df = x_dataset.dataframe

        y_kw = multi_get_copy(["y", "y_kw"], kwargs, {})
        y_dataset = self.load_dataset(verbose=verbose, debug=debug, **y_kw)
        y_df = y_dataset.dataframe

        overlap_index = x_df.index.intersection(y_df.index)
        corr_cols = [c for c in y_df.columns.values
                      if not c.endswith("_se")
                      and c in x_df.columns.values]
        corr_se_cols = [c + "_se" for c in corr_cols
                       if  c + "_se" in y_df.columns.values
                       and c + "_se" in x_df.columns.values]
        overlap_columns = [x for t in zip(corr_cols, corr_se_cols) for x in t]

        corr = pd.DataFrame(0, index=overlap_index,
          columns=pd.MultiIndex.from_product([overlap_columns, ["x", "y"]]))
        corr.iloc[:, corr.columns.get_level_values(1)=="x"] = x_df[
          overlap_columns].loc[overlap_index].values
        corr.iloc[:, corr.columns.get_level_values(1)=="y"] = y_df[
          overlap_columns].loc[overlap_index].values

        self.dataframe = corr
        print(corr)
