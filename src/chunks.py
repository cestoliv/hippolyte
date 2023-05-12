from src.type import Model, Source


def create_chunks(
		question: str,
		sources: list[Source],
		model: Model,
	)-> list[Source]:

	# Split every sources in chunks of X characters
	chunk_max_length = model["context_size"] - len(model['extractor_prompt'](question, ''))
	# TODO: overlap

	chunks: list[Source] = []
	for source in sources:
		for i in range(0, len(source['content']), chunk_max_length):
			chunks.append({
				'content': source['content'][i:i+chunk_max_length],
				'document_id': source['document_id'],
				'similarity': source['similarity'],
				'path': source['path'],
			})
	return chunks
