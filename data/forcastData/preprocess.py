import pandas as pd
import os
def readIndelOutcome():
    dir = "test"
    cell = "K562"
    dpi = "DPI7"
    coverage = "800x"
    targetFolder = []
    targetSubFolder = []
    fileList = []
    labelDic = {}
    

    for folder in os.listdir(dir):
        containsAll = True
        folderItems = folder.split("_")
        for item in [cell, dpi, coverage]:
            if item not in folderItems:
                containsAll = False
                break
        if "Old" in folderItems:
            containsAll = False
        if containsAll :
            targetFolder.append(folder)
  
    for x in os.listdir(dir):
        if x == ".DS_Store":
            continue
        path = os.path.join(dir, x)
        for y in os.listdir(path):
            subpath = os.path.join(path, y)
            targetSubFolder.append(subpath)
    
    for x in targetSubFolder:
        if os.path.isdir(x):
            for p in os.listdir(x):
                if p.endswith("_processedindels.txt"):
                    file_path = os.path.join(x, p)
                    fileList.append(file_path)
    
    for file in fileList:
        with open(file, 'r') as f:
            id = ''
            for line in f:
                if("@@@" in line):
                    line = line.strip()
                    id = line[3:]
                    continue
                else:
                    newline = line.split("\t")
                    count = int(newline[1])
                    type = newline[0]

                    if id not in labelDic:
                        labelDic[id] = {}

                    if type not in labelDic[id]:
                        labelDic[id][type] = 0

                    labelDic[id][type] += count

    return labelDic

def switchForecast(df):
    df['center'] = ""
    for i in range(df.shape[0]):
        targetSeq = df["TargetSequence"][i]
        index = df["PAM Index"][i],
        strand = df["Strand"][i]
        seq = getSequenceFragments(targetSeq, index, strand)
        df.at[i,"newSeq"] = seq
    
    seqDic = {}
    for index, row in df.iterrows():
        seqDic[row["ID"]] = row["newSeq"]

    return seqDic      
        
def getSequenceFragments(targetSeq, index, strand):
    targetLen = 60  # 设置输出长度为60
    index = index[0]
    lFragments = ""
    RFragments = ""
    if strand == "FORWARD":
        left = [index -3 -30, index -3]
        right = [index - 3, index - 3 + 30]
        lFragments = targetSeq[left[0] : left[1]]
        RFragments = targetSeq[right[0]: right[1]]
        if(len(RFragments) == 26):
            RFragments = RFragments + "AGCT"
    else:
        left = [index + 3 -30, index  + 3]
        right = [index  + 3, index  + 3 + 30]
        lFragments = targetSeq[left[0] : left[1]][::-1]
        RFragments = targetSeq[right[0]: right[1]][::-1]
        if(len(RFragments) == 27):
            RFragments = RFragments + "AGC"
    
    result = lFragments + RFragments

    if strand == "REVERSE":
        complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
        reverse_seq = result[::-1]
        complement_seq = ''.join([complement.get(base, base) for base in reverse_seq])
        result = complement_seq

    return result

def getIndelFeq(indel, valid):
    resultTimes = []
    result = []
    for id in valid:
        deletion = 0
        insertion = 0
        onebpDeletion = 0
        onebpIns = 0
        total = 0
        for record in indel[id]:
            first = record.split("_")[0][0]
            second = record.split("_")[0][1:] 
            if first == "D":
                deletion = deletion + indel[id][record]
                total = total + indel[id][record]
                if(second == "1"):
                    onebpDeletion = onebpDeletion + indel[id][record]
            elif first == "I":
                insertion = insertion + indel[id][record]
                total = total + indel[id][record]
                if(second == "1"):
                    onebpIns = onebpIns + indel[id][record]
        one = dict()
        one["data"] = [round(deletion / (insertion + deletion), 5), 
                       round(onebpDeletion / total, 5), 
                       round(onebpIns / total, 5)]
        one["id"] = id
        result.append(one)
    return result
                 
def oneHot(seqs):
    dna_dict = {'A': [1, 0, 0, 0], 'C': [0, 1, 0, 0], 'G': [0, 0, 1, 0], 'T': [0, 0, 0, 1],' ': [0,0,0,0]}
    e  = []
    res = []
    for index, one in enumerate(seqs):
        encoded_sequence = []
        newOne = dict()
        for i, base in enumerate(one["seq"]):
            encoded_base = []
            encoded_base.extend(dna_dict[base])
            encoded_sequence.append(encoded_base)
        e.append(encoded_sequence) 
        newOne["encoded"]  = e
        newOne["id"] = one["id"]
        newOne["seq"] = one["seq"]
        res.append(newOne)
    return res

def main():
    forecast = pd.read_csv("test.txt", sep="\t")
    seqDic = switchForecast(forecast)
    indel = readIndelOutcome()
    
    
    valid = []
    for k in indel:
        if k in seqDic:
            valid.append(k)
            
    result = getIndelFeq(indel, valid)

    seqs = []
    for seq in seqDic:
        one = dict()
        one["seq"] = seqDic[seq]
        one["id"] = seq
        seqs.append(one)
    
    codedSeqs = oneHot(seqs)
    final = []
    seqs = []
    delF = []
    oneI = []
    oneD = []
    embedding = []
    count = 0
    for record in result:
        for seq in codedSeqs:
            if record["id"] == seq["id"]:
                delF.append(record["data"][0])
                oneD.append(record["data"][1])
                oneI.append(record["data"][2])
                seqs.append(seq["seq"])
                embedding.append(seq["encoded"])
                count = count + 1

    
    data = {"embedding": embedding, "deletion": delF, "oneDeletion":oneD, "oneInsertion":oneI}
    df = pd.DataFrame(data)
    df.to_csv("forecast.csv", index=False)

main()