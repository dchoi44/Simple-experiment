if __name__ == '__main__':
	import warnings, util
	import numpy as np
	warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
	#  Dealing with windows warnings
	import gensim

	from sys import argv, exit

	training = None
	train_file = []
	testing = None
	test_file = []
	test_out = None
	i = 1
	while i < len(argv):
		if argv[i] == '-training':
			training = True
			fn = argv[i + 1]
			for j in range(int(fn)):
				train_file.append(argv[i + j + 2])
			i += 2 + int(fn)

		elif argv[i] == '-testing':
			testing = True
			test_file.append(argv[i + 1])
			test_file.append(argv[i + 2])
			test_out = argv[i + 3]
			i += 4

		else:
			print 'check the arguments again'
			exit(0)

	model = None
	if training:
		print 'training the model...'
		sentences = util.Sentence(train_file)
		model = gensim.models.Word2Vec(sentences, min_count=0)
	else:
		trained = '../dat/GoogleNews-vectors-negative300.bin.gz'
		print 'loading pretrained data at: ' + trained
		# model = gensim.models.Word2Vec.load_word2vec_format(trained, binary=True)
		model = gensim.models.KeyedVectors.load_word2vec_format(trained, binary=True)
	if testing:
		print 'testing the model...'
		test_from, test_to = test_file

		cos_mat = util.cos_sim_mat(util.Sentence(test_from).vec_sum(model), 
				  		  		   util.Sentence(test_to).vec_sum(model))
		
		harsh_cnt = 0
		easy_cnt = 0
		for i in range(cos_mat.shape[0]):
			if np.argmax(cos_mat[i]) == i:
				harsh_cnt += 1
				easy_cnt += 1
			elif i in cos_mat[i].argsort()[-5:][::-1]:
				easy_cnt += 1

		print 'testing is done with accuracy of %f%% with harsh criteria, of %f%% with easy criteria'\
				%(harsh_cnt * 100 / float(cos_mat.shape[0]), easy_cnt * 100 / float(cos_mat.shape[0]))
		np.savetxt(test_out, cos_mat, delimiter='\t')