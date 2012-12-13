"""
inputMediafile_test.py

Unit test suite for the inputMediafile class
"""

#==============================================================================================================
# Import section
#==============================================================================================================
from inputMediafile import inputMediafile
import unittest

#==============================================================================================================
# Common information for all tests
#==============================================================================================================
# Environment
env_ffmpeg_dir = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Eigene Programme/ffmpeg/bin/'
env_mediainfo_dir = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Eigene Programme/MediaInfo/'
env_infile_dir = 'c:/Dokumente und Einstellungen/BaumeiJu01/Eigene Dateien/Eigene Programme/ffmpeg/video/'

# external Programms
com_ffmpeg = "ffmpeg.exe"
com_mediainfo = "MediaInfo_cli.exe"

# Variables for in- outfiles
video_in_file = 'test.wmv'

# Commandlines for the test
com_1 = [com_ffmpeg, "-i", video_in_file]
com_2 = [com_mediainfo, "-f", video_in_file]
com_3 = [com_ffmpeg, "-i", video_in_file, "-vf", "scale=600:400", "-t", "5", "test.mp4"]

# Environment
env = {'path':env_ffmpeg_dir + ";" + env_mediainfo_dir + ";" + env_infile_dir,
		'in_dir':env_infile_dir}

#==============================================================================================================
# Unit test classes
#==============================================================================================================
class TestCreate_inputMediafile(unittest.TestCase):
	def setUp(self):
		print 'Initialisation of inputMediafile ...'
		self.dp = None

	def tearDown(self):
		print 'Initialisation of inputMediafile done'
		pass

	def runTest(self):
		for filename in ['test.wmv','test_1.wmv','test_2.wmv','test_3.mp4','test_4.mp4','test_5.avi']:
			print '\n\n  File: ' + filename
			self.file = inputMediafile(filename)
			assert self.file != None, '  Could not initialize inputMediafile'
		
			count = 0
			for key in self.file.full_info:
				print count, '...', key, '...........................................', self.file.full_info[key]
				count += 1
			
			print '  Creating info dictionary for media file'
		
			info = self.file.getMediaInfo()
			print '\n\n  Info for the media file'
			print info
		
			info = None
			info = self.file.getMediaInfo_1()
			print '\n\n  Info, using depreciated method getMediaInfo_1()'
			print info
		
			info = None
			print '\n\n  Info, in json format'
			info = self.file.getMediaInfo('json')
			print info

 	
#==============================================================================================================
# Organize and start the tests
#==============================================================================================================
def suite():
	print 'Testing DP_basic'
	testSuite=unittest.TestSuite()
	testSuite.addTest(TestCreate_inputMediafile())

	return testSuite
    
def main():
	runner = unittest.TextTestRunner()
	runner.run(suite())

    
if __name__ == '__main__':
	main()
