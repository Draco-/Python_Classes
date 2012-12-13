"""
externalProcess_test.py

Unit test suite for the externalProcess class
"""

#==============================================================================================================
# Import section
#==============================================================================================================
from externalProcess import externalProcess
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

class TestCreateexternalProcess(unittest.TestCase):
	def setUp(self):
		print 'Initialisation of externalProcess ...'
		self.dp = None

	def tearDown(self):
		print 'Initialisation of externalProcess done'
		pass

	def runTest(self):
		self.process = externalProcess(com_1, env)
		assert self.process != None, '  Could not initialize external process'

		count = 0
		for line in self.process.execute():
			count += 1
			print count, line

		assert count == 23, '  external process returned wrong number of lines'
 	
#==============================================================================================================
# Organize and start the tests
#==============================================================================================================
def suite():
	print 'Testing DP_basic'
	testSuite=unittest.TestSuite()
	testSuite.addTest(TestCreateexternalProcess())

	return testSuite
    
def main():
	runner = unittest.TextTestRunner()
	runner.run(suite())

    
if __name__ == '__main__':
	main()
