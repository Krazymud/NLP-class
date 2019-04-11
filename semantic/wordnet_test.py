from nltk.corpus import wordnet as wn
from itertools import product
# First task
print('First task:\n')
print('Synsets of dog:\n')
for w in wn.synsets('dog'):
    print(w, ':', w.definition())
    print('Example :', w.examples())
    print('')
print('\nSynsets of apple:\n')
for w in wn.synsets('apple'):
    print(w, ':', w.definition())
    print('Example :', w.examples())
    print('')
print('\nSynsets of fly:\n')
for w in wn.synsets('fly'):
    print(w, ':', w.definition())
    print('Example :', w.examples())
    print('')

# Second task
print('\n\nSecond task:\n')
sims = []
list1 = ['good', 'good', 'dog']
list2 = ['beautiful', 'bad', 'cat']
for i in range(0, 3):
    syns1 = set(ss for ss in wn.synsets(list1[i]))
    syns2 = set(ss for ss in wn.synsets(list2[i]))
    best = max((wn.path_similarity(s1, s2) or 0, s1, s2) for s1, s2 in 
        product(syns1, syns2))
    sims.append(best)

print('Similarity between good and beautiful:', sims[0])
print('Similarity between good and bad:', sims[1])
print('Similarity between dog and cat:', sims[2])

# Third task
print('\n\nThird task:\n')
wordlist = ['walk', 'supply', 'hot']
for i in range(0, 3):
    print('Entailments of', wordlist[i], ':')
    flag = True
    for ss in wn.synsets(wordlist[i]):
        if len(ss.entailments()):
            print(ss.entailments())
            flag = False
    if flag is True:
        print('None')
    print('Antonyms of', wordlist[i], ':')
    for ss in wn.synsets(wordlist[i]):
        for s in ss.lemmas():
            if len(s.antonyms()):
                print(s.antonyms())
    print('')




 
  