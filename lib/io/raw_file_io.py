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
""" RawFile IO methods.
"""

import glob
import pandas as pd
import os
import re

class RawFileIO(object):
    """ RawFileIO class that exoises methods to read / write to / from
    raw csv files. The output csv files will remove all header
    information.
    """

    def __init__(self, in_path, out_path, **kwargs):
        """
        :type in_path: absolute path that contains input files
        :type out_path: absolute path that files output to
        :type debug: bool, print info to help debug
        :header_info: int, first header_info rows that contain extra
                      information in each csv files
        :rtype: None
        """
        self.in_path = in_path
        self.out_path = out_path
        self.debug = kwargs.get('debug', True)
        self.header_info = kwargs.get('header_info', None)
        self.load_data()
        self.write_data()

    def load_data(self):
        """
        load all csv files in self.in_path
        :type self.data: dict,
            key: file_name
            values: dict
        """
        self.data = {}
        all_csv_files = glob.glob(os.path.join(self.in_path, '*.csv'))

        if self.debug:
            print('find %d csv files in path %r' %
                  (len(all_csv_files), self.in_path))
            print('Load data')

        with open(all_csv_files[0]) as cur_file:
            for line_counter, cur_line in enumerate(cur_file):
                if self.header_info is None:
                    if cur_line.startswith('Wavelength'):
                        self.header_info = line_counter
                else:
                    break

        for csv_file in all_csv_files:
            self.data[csv_file] = {}
            with open(csv_file) as cur_file:
                # load extra information
                for line_num in range(self.header_info):
                    cur_line = next(cur_file).split(':', 1)
                    self.data[csv_file][cur_line[0]] = \
                        cur_line[1].split(',', 1)[1].split(',,')[0]

            # load pandas data frame
            data = pd.read_csv(csv_file, header=self.header_info)
            if 'Unnamed: 0' in data.columns:
                data = data.drop('Unnamed: 0', 1)
            data.columns = [i.split(' (')[0] for i in data.columns]
            self.data[csv_file]['data'] = data

    def write_data(self):
        """
        write self.data into self.out_path
        currently does not save extra information but pandas data frame
        in self.out_path, will create directories based on csv file names
        """
        lookup = set()
        for key, value in self.data.items():
            temp = key.split('/',-1)[-1].split('.csv')
            file_name = temp[0]
            
            # FIXME: class name should read from the image
            #class_name = re.split('(\d+)', temp[0])[0]
            class_name = 'Apple'

            class_path = os.path.join(self.out_path, class_name)
            os.makedirs(class_path, exist_ok=True)
            file_name = os.path.join(class_path, file_name)
            value['data'].to_csv(file_name+'.csv', index=False)
            lookup.add(class_name)
        if self.debug:
            print('find %d classes in %r' % (len(lookup), self.in_path))
