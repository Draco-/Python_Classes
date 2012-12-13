"""
inputMediafile.py

A class, that represents the media input for ffmpeg or other programms
"""

#==============================================================================================================
# Import section
#==============================================================================================================
from externalProcess import externalProcess
import os.path

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
# class inputMediaFile
#==============================================================================================================
class inputMediafile:
	"""
	This class represents an input media file, that is used for ffmpeg as well
	as other media file manipulation
	"""
	def __init__(self, name):
		"""
		Initialize the media file and get the media info for that file
		"""
		# Using a path in front of the filename is not yet supported
		(self.path, self.name) = os.path.split(name)
		self.path += '/'
		#print self.path, self.name
		#self.name = name
		
		# we use the external program MediaInfo to get all information about the media file
		self.full_info = self._parseMediaInfo()
		
	def _parseMediaInfo(self):
		"""
		Invoke the external program MediaInfo and parse its output
		to a dictionary
		"""
		# the program path to MediaInfo should be set otherwise
		env = {'path': env_mediainfo_dir}
		# the command for MediaInfo is a fixed command
		com = [com_mediainfo, '-f', self.name]
		# invoke the external program
		proc = externalProcess(com, env)
		# read the programs output line by line and parse the output to a dictionary, obtaining all information
		info = {}
		state = 'start'
		stream = 0
		for line in proc.execute():
			list = line.split(":")
			# recognize the sections ('General','Video','Audio','Text')
			if len(list) == 1 and list[0] != '':
				state = str(list[0].lstrip().rstrip())
				# print "New state: ", state
			elif len(list) >= 2 and list[0] != '' and list[1] != '':
				# recognize several stream identifier
				if str(list[0].lstrip().rstrip()) == 'Stream identifier':
					stream = int(str(list[1].lstrip().rstrip()))
					continue
				# save the information to the dictionary
				key = state + "_" + str(stream) + "_" + str(list[0].lstrip().rstrip())
				while key in info.keys():
					key += "_"
				info[key] = str(list[1].lstrip().rstrip())
		return info

	# Method depreciated, use 'getMediaInfo()'instead
	def getMediaInfo_1(self, type='dict'):
		if type == 'dict':
			result = {}
			result['General'] = {}
			result['General'][0] = {}
			for key in ['General_0_Count of video streams','General_0_Count of audio streams','General_0_Duration','General_0_File size']:
				if key in self.full_info.keys():
					try:
						result['General'][0][key[10:]] = float(self.full_info[key])
					except ValueError:
						result['General'][0][key[10:]] = self.full_info[key]
						
			result['Video'] = {}
			for i in range(int(result['General'][0]['Count of video streams'])):
				result['Video'][i] = {}
				for key in ['Video_'+str(i)+'_Format','Video_'+str(i)+'_Format profile','Video_'+str(i)+'_Codec ID','Video_'+str(i)+'_Duration',
							'Video_'+str(i)+'_Bit rate','Video_'+str(i)+'_Width','Video_'+str(i)+'_Height','Video_'+str(i)+'_Frame rate',
							'Video_'+str(i)+'_Frame count','Video_'+str(i)+'_Stream size']:
					if key in self.full_info.keys():
						try:
							result['Video'][0][key[8:]] = float(self.full_info[key])
						except ValueError:
							result['Video'][0][key[8:]] = self.full_info[key]
			
			result['Audio'] = {}
			for i in range(int(result['General'][0]['Count of audio streams'])):
				result['Audio'][i] = {}
				for key in ['Audio_'+str(i)+'_Format','Audio_'+str(i)+'_Codec ID/Info','Audio_'+str(i)+'_Duration','Audio_'+str(i)+'_Bit rate',
							'Audio_'+str(i)+'_Sampling rate','Audio_'+str(i)+'_Samples count','Audio_'+str(i)+'_Stream size']:
					if key in self.full_info.keys():
						try:
							result['Audio'][0][key[8:]] = float(self.full_info[key])
						except ValueError:
							result['Audio'][0][key[8:]] = self.full_info[key]
			return result
			
			
	def getMediaInfo(self, type='dict'):
		"""
		Use the full_info to prepare a condensed info package for the media file, containing only
		the necessary information
		"""
		# define the content lists for sections 'General','Video','Audio'
		cont_general = ['Count of video streams','Count of audio streams','Duration','File size']
		cont_video = ['Format','Format profile','Codec ID','Duration','Bit rate','Width','Height','Frame rate','Frame count','Stream size']
		cont_audio = ['Format','Codec ID/Info','Duration','Bit rate','Sampling rate','Samples count','Stream size']
		
		# the type parameter is used to provide the information in several formats
		if type == 'dict': # Info is provided as python dictionary
			# prepare dictionary
			result = {}
			# prepare section 'General'
			result['General'] = {}
			# fill section 'General' with its information
			result = self._fill_section_dict(result, 'General',cont_general)
			
			# prepare and fill section 'Video' with its information
			if 'Count of video streams' in result['General'][0].keys():
				result['Video'] = {}
				result = self._fill_section_dict(result,'Video',cont_video, result['General'][0]['Count of video streams'])
			else:
				result['Video'] = 'No stream'
			
			# prepare and fill section 'Audio' with its information
			if 'Count of audio streams' in result['General'][0].keys():
				result['Audio'] = {}
				result = self._fill_section_dict(result,'Audio',cont_audio, result['General'][0]['Count of audio streams'])
			else:
				result['Audio'] = 'No stream'
			
			return result
			
			# I'm not sure, if a section 'Text' as mentioned in the MediaInfo documentation is needed here
			
		elif type == 'json': # Info is provided as json string
			# start json string
			result = '{'
			# prepare section 'General'
			result += '\'General\':'
			# fill section 'General' with its information
			result = self._fill_section_json(result, 'General', cont_general)
			
			# prepare section 'Video'
			result += '\'Video\':'
			if 'General_0_Count of video streams' in self.full_info.keys():
				result = self._fill_section_json(result, 'Video', cont_video,int(self.full_info['General_0_Count of video streams']))
			else:
				result += '\'No stream\''
						
			# prepare section 'Audio'
			result += '\'Audio\''
			if 'General_0_Count of audio streams' in self.full_info.keys():
				result = self._fill_section_json(result, 'Audio', cont_audio,int(self.full_info['General_0_Count of audio streams']))
			else:
				result += '\'No stream\''
		
			# end result
			result += '}'
		return result
			
			
			
	def _fill_section_dict(self, dictionary, section, keys=[], streams=1):
		"""
		Fills a dictionary with the selected information form full_info
		dictionary:		the dictionary to fill
		section:		as string naming the section to fill; the given dictionary
						must already contain a key 'section' with an empty dictionary
		keys:			a list of keys required
		streams:		the number of streams to process
		
		returns the modified dictionary
		"""
		# if there is no stream, we just place a note in the dictionary
		if streams == 0:
			dictionary[section] = 'No stream'
			return dictionary

		# otherwise we have to fill one subdictionary per stream		
		for i in range(streams):
			dictionary[section][i] = {}
			# lookup the information for every key requested and fill the dictionary accordingly
			for key in keys:
				if (section + '_' + str(i) + '_' + key) in self.full_info.keys():
					try:
						dictionary[section][i][key] = int(self.full_info[section + '_' + str(i) + '_' + key])
					except ValueError:
						try:
							dictionary[section][i][key] = float(self.full_info[section + '_' + str(i) + '_' + key])
						except ValueError:
							dictionary[section][i][key] = self.full_info[section + '_' + str(i) + '_' + key]
		
		return dictionary
		
	def _fill_section_json(self, collector, section, keys=[], streams=1):
		"""
		Fills the collector string with the selected information from full_info
		collector:		the string, that collects the output
		section:		a string naming the section to fill; the collector must already
						contain the key for the section
		keys:			a list of keys required
		streams:		the number of streams to process
		
		returns the modified collector
		"""
		# if there is no stream, we just place a note in the json
		if streams == 0:
			collector += '\'No stream\''
			return collector
		
		# otherwise we have to fill a json segment with the requested information
		collector += '{'
		for i in range(streams):
			collector += '\'' + str(i) + '\':{'
			for key in keys:
				if (section + '_' + str(i) + '_' + key) in self.full_info.keys():
					collector += '\'' + key + '\':'
					try:
						float(self.full_info[section + '_' + str(i) + '_' + key])
						collector += self.full_info[section + '_' + str(i) + '_' + key]
					except ValueError:
						collector += '\'' + self.full_info[section + '_' + str(i) + '_' + key] + '\''
				collector += ','	

			collector = collector[0:len(collector)-1] + '}'
		collector += '}'
		return collector
						
		
	
	
	
				