#Author: truongtn
#Use Findachange.missingfile shows the missing files
#Use Findachange.addedfile shows the added files
#Use Findachange.changedfile shows the changed files
import os
import hashlib
from glob import glob
from os import getcwd
from os.path import join
import ntpath
class Findachange:
	"""Compare 2 documents, that's all meoww"""
	missingfile = []
	addedfile = []
	changedfile = []
	def __init__(self,base_path,target_path):
		self.base_path = os.path.realpath(base_path)
		self.target_path = os.path.realpath(target_path)
		self.base_list = self._listfile(self.base_path)
		self.target_list = self._listfile(self.target_path)
		self.findachange()
	#Convert path list to file name list
	def _getlistfilename(self,_list):
		newlist = []
		for item in _list:
			newlist.append(ntpath.basename(item))
		return newlist
	#List all file in path
	def _listfile(self,path):   
		filelist = glob(join(getcwd(), path, '*'))
		return filelist
	#Make MD5 
	def _filemd5(self,path):
		with open(path) as file_to_check:
			data = file_to_check.read()
			md5_returned = hashlib.md5(data).hexdigest()
		return md5_returned
	def _makelinkdict(self,_list):
		newdict = {}
		for item in _list:
			dic_temp = {ntpath.basename(item):item}
			newdict.update(dic_temp)
		return newdict
	def _checkexits(self,base_path,target_path):
		base_list = self._listfile(os.path.realpath(base_path))
		target_list = self._listfile(os.path.realpath(target_path))
		base_dict = self._makelinkdict(base_list)
		target_dict = self._makelinkdict(target_list)
		#Check missing files
		for filename in base_list:
			if ntpath.basename(filename) not in self._getlistfilename(target_list):
				self.missingfile.append(filename)
			else:
				temp_var = target_dict[ntpath.basename(filename)]
				if os.path.isdir(filename):
					self._checkexits(filename,temp_var)
				else:
					if self._filemd5(filename) != self._filemd5(temp_var):
						self.changedfile.append(filename)
		#Check added files
		for filename in target_list:
			if ntpath.basename(filename) not in self._getlistfilename(base_list):
				self.addedfile.append(filename)
	def findachange(self):
		self._checkexits(self.base_path,self.target_path)
