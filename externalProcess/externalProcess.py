"""
externalProcess.py

A class to run external processes in windows from a python script
"""

#==============================================================================================================
# Import section
#==============================================================================================================
from subprocess import Popen, PIPE, STDOUT
from threading import Thread
try:
	from Queue import Queue, Empty
except ImportError:
	from queue import Queue, Empty
from time import sleep

#==============================================================================================================
# class externalProcess
#==============================================================================================================
class externalProcess:
	"""
	The class to run an external process
	"""
	
	def __init__(self,command=[], environment=None):
		"""
		Initialize the external process class with a command
		and optional an environment
		"""
		# handle enviroment setting
		if environment != None and environment != {} and isinstance(environment, dict):
			self.environment = environment
		
		# handle command setting
		if isinstance(command, list):
			self.command = command
			self.status = "ready"
		elif isinstance(command, string):
			self.command = command
			self.status = "ready"
		else:
			self.status = "No command"
			
		# handle communication
		self.queue = Queue()
		self.process = None
		
	def __iter__(self):
		"""
		Return self as an iterator
		this is included to implement the iterator interface
		"""
		return self
		
	def next(self):
		"""
		Return the next line from the process output
		"""
		try:
			line = self.queue.get(timeout=1.5)
			line = line.rstrip('\r\n ')
			line = line.lstrip('\r\n\t ')
			return line
		except Empty:
			raise StopIteration
			
	def execute(self):
		"""
		Restart the process and return an iterator for the output
		"""
		self.process = None
		return self.run()
		
	def run(self, daemon=True):
		"""
		Executes the command. A thread will be started to collect
		the outputs (stderr and stdout) from that command.
		The outputs will be written to the queue.
		"""
		# Start the external process
		if self.status == "ready":
			self.process = Popen(self.command, bufsize=1, shell=True, env=self.environment,
								stdin=PIPE, stdout=PIPE, stderr=STDOUT)
			# Prepare and start a thread to continiously read the output from the process
			thread = Thread(target=self._queue_output,
							args=(self.process.stdout, self.queue))
			thread.deamon = daemon
			thread.start()
		# Return self as the iterator object
		return self
		
	def _queue_output(self, out, queue):
		"""
		Read the output from the command bytewise. On every newline
		the line is put to the queue.
		"""
		# perpare line to output
		line = ''
		# Continiously read the out stream of the process
		while True:
			chunk = out.read(1).decode('utf-8')
			# If there is no output, but the process is still running, wait for new output
			while (chunk == '') and (self.process.poll() is None):
				sleep(0.1)
				chunk = out.read(1).decode('utf-8')
			# If the process is no longer running, and there is still no output, then break
			if chunk == '':
				queue.put(line) # if line has not been completed before break, put this also to queue
				break
			# When line is completed, put it to queue otherwise go on collecting
			#line += chunk
			if chunk in ('\n', '\r') and len(line) != 0:
				queue.put(line)
				line = ''
			else:
				line += chunk

		# Close out stream and finish
		out.close()
