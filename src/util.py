class Sentence():

	"""Summary
	
	Attributes:
	    fnames (list(, or string)): A list of files contain sentences.
	"""
	
	def __init__(self, fname):
		"""Summary
		
		Args:
		    fname (list(, or string)): A list of files contain sentences.
		"""
		if type(fname) == type('abc'):
			fname = [fname]
		self.fnames = fname

	def __iter__(self):
		"""Summary
		
		Yields:
		    list: A splitted sentence.
		"""
		from sys import exit
		for fname in self.fnames:
			cnt = 0
			try:
				with open(fname, 'r') as fin:
					line = fin.readline().strip().split('\t')
					while line != ['']:
						if len(line) == 1 and line[0].startswith('<'):
							line_res = []
							line = fin.readline().strip().split('\t')
							for word in line:
								for char in word:
									if not char.isalpha():
										break
								else:
									line_res.append(word)
							yield line_res
							cnt += 1
							
							while line != None:
								line = fin.readline().strip().split()
								if len(line) == 1 and line[0].startswith('</'):
									break
						line = fin.readline().strip().split('\t')
			except:
				print 'invalid file path: ' + fname
				exit(1)

	def vec_sum(self, model):
		"""Summary
		
		Args:
		    model (gensim module's): Description
		
		Returns:
		    numpy array: A numpy array of sentence-wise averaged vectors
		"""
		import numpy as np
		key_error = 0
		res = []
		for stc in self:
			cnt = 0
			avg_vec = np.zeros(model['is'].size)
			for word in stc:
				try:
					cnt += 1
					avg_vec += model[word]
				except:
					key_error += 1
			avg_vec / cnt
			res.append(avg_vec)
		return np.asarray(res)

def cos_sim_mat(vec_from, vec_to):
	"""Summary
	
	Args:
	    vec_from (numpy array): A list of extracted vectors from a document.
	    vec_to (numpy array): A list of extracted vectors from a document.
	
	Returns:
	    numpy matrix: A numpy matrix of pairwise cosine similarity.
	"""
	from sklearn.metrics.pairwise import cosine_similarity
	return cosine_similarity(vec_from, vec_to)