# similarity functions for comparing two strings


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

def bert_cosine(t1,t2):
    """context-aware similarity measure for two strings using bert sentence transformer and cosine similarity"""
    model = SentenceTransformer('sentence-transformers/stsb-mpnet-base-v2')
    sentences = [t1, t2]
    embedding_1= model.encode(sentences[0], convert_to_tensor=True)
    embedding_2 = model.encode(sentences[1], convert_to_tensor=True)
    score = util.pytorch_cos_sim(embedding_1, embedding_2)
    score = score.tolist()
    return score[0][0]

model = SentenceTransformer('sentence-transformers/stsb-mpnet-base-v2')
cache = {}
def bert_cosine_optimized(t1,t2):
    """optimized function of bert_cosine. uses a cache to safe time when calculating duplicate similarities
    reason: for longer inputs bert can be very compute intensive. adding a cache can reduce minutes to seconds"""

    sentences = [t1, t2]
    def encode(value):
        cache_hit = cache.get(value, None)
        if cache_hit is not None:
            return cache_hit
        else:
            embedding = model.encode(value, convert_to_tensor=True)
            cache[value] = embedding
            return embedding

    embedding_1= encode(sentences[0])
    embedding_2 = encode(sentences[1])
    score = util.pytorch_cos_sim(embedding_1, embedding_2)
    score = score.tolist()
    return score[0][0]

def tfid_cosine(text1,text2):
    """context-ignoring similarity measure for two strings using tfid and cosine similarity"""
    corpus = [text1,text2]
    vectorizer = TfidfVectorizer()
    trsfm=vectorizer.fit_transform(corpus)
    cos_sim = cosine_similarity(trsfm[0:1], trsfm)
    cos_sim = cos_sim[0][1]
    return cos_sim