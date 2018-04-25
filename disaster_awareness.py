from EMTerms import load_emterms
import json

def gen_em_ldc_mapping(map_filename):
    # generate mapping json from text file, e.g. {'T10', {'relief ongoing': 1, 'exp. need': 1, 'imp. need': 1}}
    EM_LDC_mapping = {}
    with open(map_filename) as f:
        for line in f:
            EM = line[:3]
            idx = line.index("-")
            labels_str = line[idx + 2:]
            labels = labels_str.split(",")

            temp_obj = {}
            for tuple in labels:
                tuple = tuple.strip(" ").rstrip("\n")
                kv = tuple.split(":")
                key = kv[0]
                value = int(kv[1])
                temp_obj[key] = value

            EM_LDC_mapping[EM] = temp_obj

    return EM_LDC_mapping

def map_EM_2_LDC(EM_list, mapping_rule, threshold=-1):
    """
    Map a list of EMTerms to a list of LDC labels.
    :param EM_list:
    :param threshold:
    :return:
    """
    counter = {}
    for em in EM_list: # each EMTerm
        mapped_dict = mapping_rule[em]
        for ldc, weight in mapped_dict.items(): # each ldc label corr. EMTerm
            if ldc not in counter:
                counter[ldc] = weight
            else:
                counter[ldc] += weight

    if threshold == -1:
        counter = list(counter.items())
        counter.sort(key=lambda x: x[1], reverse=True)
        return counter
    else:
        ret = []
        for ldc, cnt in counter.items():
            if cnt >= threshold:
                ret.append(ldc)
        return ret

def gen_list_mapping_n_score(source, mapping_rule, mapping_func):
    """
    map a list of list of source items to a list of items and confidence score
    :param source: A list of list
    :param mapping_func: Function, can either be map_EM_2_LDC or map_LDC_2_EM
    :return:
    """

    pred_full = []

    for slist in source:
        mapped = mapping_func(slist, mapping_rule)
        pred_full.append(mapped)

    return pred_full

config_directory = "disaster_awareness_config.json"

config = json.loads(open(config_directory).read())
data_directory = config["data_directory"]
mode = config["mode"]
k = config["k"]
threshold = config["threshold"]
result_filename = config["result_filename"]

emt = load_emterms()
EM_list = []
with open(data_directory) as f:
    for doc in f:
        EM_list.append(emt.findall(doc))

mapping = gen_em_ldc_mapping("map_scale3.txt")
mapped = gen_list_mapping_n_score(EM_list, mapping, map_EM_2_LDC)

with open(result_filename, "w") as f:
    if mode == "topk":
        for line in mapped:
            if not line:
                f.write("\n")
                continue
            temp_str = []
            for idx in range(k):
                try:
                    temp_str.append(line[idx][0])
                except:
                    break
            temp_str = ",".join(temp_str)
            f.write(temp_str)
            f.write("\n")
    elif mode == "threshold":
        for line in mapped:
            if not line:
                f.write("\n")
                continue
            temp_str = []
            for label, score in line:
                if score >= threshold:
                    temp_str.append(label)
                else:
                    break
            temp_str = ",".join(temp_str)
            f.write(temp_str)
            f.write("\n")