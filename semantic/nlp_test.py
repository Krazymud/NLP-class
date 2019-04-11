import spacy
nlp = spacy.load('en')

# Add neural coref to SpaCy's pipe
import neuralcoref
neuralcoref.add_to_pipe(nlp)

sentences = ['My sister has a dog. She loves him.',
             'Some like to play football, others are fond of basketball.',
             'The more a man knows, the more he feels his ignorance.']

for s in sentences:
    n = nlp(s)
    print('Sentence:', s)
    if n._.has_coref:
        print('The sentence has coref.')
        print('The coref clusters:')
        print(n._.coref_clusters, '\n')
    else:
        print('The sentence has no coref.\n')
    
    

