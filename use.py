import tensorflow as tf

def parseToOneHot(dna):
    e  = []
    dna_dict = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1],'N': [0,0,0,0]}
    encoded_sequence = []
    for i, base in enumerate(dna):
            #### one hot
            encoded_base = []
            encoded_base.extend(dna_dict[base])
            encoded_sequence.append(encoded_base)
    e.append(encoded_sequence)
    print(len(e), len(e[0]))
    return e
        
        
def predict(dna):
    model = tf.keras.models.load_model('./model/best.h5')
    dna = parseToOneHot(dna)
    res = model.predict(dna)
    res = dict({
        "dele":res[0][0],
        'oneIns': res[0][1],
        "oneDele":res[0][2]
    })
    for key, value in res.items():
        print("{}: {:.2f}".format(key, value))
    return res


dna_sequence = 'AGGTGGACGGGGGCGGCCTTACCCTTCCATATAAGGTGTGCAATAGCGAGTGGCCAGTCC'


predict(dna_sequence)