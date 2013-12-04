#!/usr/bin/env python
# Copyright (C) 2013 mindmac <mindmac.hu@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
from zipfile import ZipFile, ZipInfo

class ApkFile(ZipFile):
	def compress(self, member, src_apk):
		if not isinstance(member, ZipInfo):
			member = self.getinfo(member)
		try:
			data_obj = src_apk.open(member, 'r')
			data = data_obj.read()
		except RuntimeError, e:
			print e
			return
		member.flag_bits |= 1
		self.writestr(member, data)
		print 'compressing %s' % member.filename
				
	def compressall(self, src_apk=None):
		map(lambda entry: self.compress(entry, src_apk), src_apk.filelist)
				
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Add the encrypted flag to an APK. \
	src_apk specifies the apk file you want to add encrypted flag, dst_apk is the output apk file.')
	parser.add_argument('src_apk', type=str)
	parser.add_argument('dst_apk', type=str)
	args = parser.parse_args()
	src_apk = ApkFile(args.src_apk, 'r')
	dst_apk = ApkFile(args.dst_apk, 'w')
	dst_apk.compressall(src_apk=src_apk)
