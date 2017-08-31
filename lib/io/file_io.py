# Copyright 2017 The Vispek Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==========================================================================
""" File IO methods.
"""

import glob
import numpy as np
import pandas as pd
import os
import re

class FileIO(object):
    """ FileIO class that exoises methods to read from preprocessed csv
    files.
    """

    def __init__(self, in_path, **kwargs):
        """
        :type in_path: absolute path that contains input files
        :type debug: bool, print info to help debug
        :rtype: None
        """
        self.in_path = in_path
        self.debug = kwargs.get('debug', True)

    def load_data(self, **kwargs):
        """
        load all csv files in self.in_path
        :rtype: ndarray, with shape (n, i, j)
            where n is the number of csv files in the path
            i is the number of wavelength, and j is the number of channels
        """
        all_csv_files = glob.glob(os.path.join(self.in_path, '*.csv'))
        self.cols = kwargs.get('columns',
            ['Wavelength', 'Absorbance', 'Reference Signal',
            'Sample Signal'])

        if self.debug:
            print('find %d csv files in path %r' %
                  (len(all_csv_files), self.in_path))
            print('Load data')
        if not len(all_csv_files):
            raise ValueError('There are no csv files')

        num_csv = len(all_csv_files)
        df = pd.read_csv(all_csv_files[0])
        for col in self.cols:
            if col not in df.columns:
                print(df.columns)
                raise KeyError('column %s not in the file' % col)

        self.data = np.empty([num_csv, df.shape[0], df.shape[1]])

        for i, csv_file in enumerate(all_csv_files):
            # load pandas data frame
            data = pd.read_csv(csv_file, index_col=0)
            self.data[i] = df[self.cols].values

        return self.data
