import pandas as pd
import os
def getFileList(data):
    genes = data["genename"]
    id = data["id_ending"]
    fileList = []
    count = 0
    for gene in genes:
        name = "counts-"
        fullname = name + gene + id[count].split("'")[1]+'.txt'
        count = count +1
        fileList.append(fullname)
    return fileList

def forFiles(list, id):
    res = []
    index = 0
    for name in list:
        with open("/Users/sk/Desktop/Kmodel/data/sprout/counts/"+ name, 'r') as f:
            times = 0
            oneIns = 0
            oneDel = 0
            dele = 0
            ins = 0
            total = 0
            one = dict()
            for line in f:
                times =  times + 1
                if("SNV" not in line and "no variant" not in line and times != 1 and "Other" not in line) :
                    groups = line.split(",")
                    groups = [group.strip("'\"") for group in groups]
                    count = groups[-2:][0]
                    groups.pop()
                    groups.pop()
                    type = groups
                    for sub in type:
                        if "1D" in sub:
                            oneDel = oneDel + int(count)
                        if "1I" in sub:
                            oneIns = oneIns + int(count)
                        if "D" in sub:
                            total = total + int(count)
                            dele = dele + int(count)
                        if "I" in sub:
                            total = total + int(count)
                            ins = ins + int(count)
        if(dele == 0 and ins == 0):
                dele = 0
                oneIns = 0
                oneDel = 0
                one["data"] = [dele, oneIns, oneDel]
                one["name"] = id[index]
                res.append(one)
        else:
                dele = round(dele / (dele + ins), 5)
                oneIns = round(oneIns / total, 5)
                oneDel = round(oneDel / total, 5)
                one["data"] = [dele, oneIns, oneDel]
                one["name"] = id[index]
                res.append(one)
        index = index + 1
    return res


def oneHot(data):
    dna_dict = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1],' ': [0,0,0,0]}
    e  = []
    res=  []
    count = 0 
    for one in enumerate(data["refseq"]):
        newone = dict()
        encoded_sequence = []

        for base in one[1]:
                encoded_base = []
                encoded_base.extend(dna_dict[base])
                encoded_sequence.append(encoded_base)
        e.append(encoded_sequence) 
        newone["embedding"] = e
        newone["name"] = one[0]
        newone['seq'] = one[1]
        
    res.append(newone)
    return res


def main():
    data = pd.read_csv("key.csv")
    fileList = getFileList(data)
    res = forFiles(fileList, data["index"])
    dele = []
    oneDel = []
    oneIns = []
    seqs = []
    embedding = []

    
    count = 0
    e = oneHot(data)
    for record in res:
        for seq in e:
            if record["name"] == seq["name"]:
                dele.append(record["data"][0])
                oneDel.append(record["data"][1])
                oneIns.append(record["data"][2])
                embedding.append(seq["embedding"])
                seqs.append(seq["seq"])
                
                count = count + 1

    data = {"embedding": embedding, "deletion": dele, "oneDeletion": oneDel, "oneInsertion": oneIns}
    df = pd.DataFrame(data, columns=["embedding", "deletion", "oneDeletion", "oneInsertion"])
    df.to_csv("sprout.csv", index=False)

    
    
    
main()