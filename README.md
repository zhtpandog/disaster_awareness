# disaster_awareness #
The Python script __disaster_awareness.py__ can classify input documents into the following 13 natural disaster awareness labels:  
```
'exp. need'
'imp. need'
'delivered/arrived'
'response'
'fact/statem'
'opinion'
'update'
'offer'
'happen'
'casualties/aftermath'
'relief ongoing'
'finished'
'precaution'
```
This repo belongs to the THOR project (http://usc-isi-i2.github.io/thor/).  

## Dependencies ##
Python 3 envoironment  
EMTerm classifier (https://github.com/guyao/EMTerms)  

## Usage ##
1. Clone this repo  
2. Install the EMClassifier  
3. Make configurations in disaster_awareness_config.json and prepare your input   
4. Run command  
```
python disaster_awareness.py
```
5. Retrieve result (file named as __"result.txt"__ by default)  

## Configuration ##
In the __disaster_awareness_config.json__ file, there are several fields can be configured:  
1. __data_directory__: the location and file name of the input document you wish to be classified  
2. __mapping_directory__: the location and file name of the mapping rule file  
3. __result_filename__: the file name of the final result  
6. __mode__: "topk" or "threshold"  
7. __k__: number of themes per document you want to retrieve in the final result, and this field only useful when __mode__ is "topk"  
8. __threshold__: what is the threshold to define a trustworthy classified theme, and this field only useful when __mode__ is "threshold"  

## Input format ##
Input should be a text file that has each line being a document. Different documents are separated by line break (\n). If your source document has multiple lines, please first preprocess it into a single-line document by concatenating paragraphs using space.  

## Output format ##
Classified labels, one set of labels per line, corresponding to the sequence of input documents.  

## Mapping rule ##
The mapping rule can be customized in a text file. The default one is __map.scale3.txt__. You can customize your own rule according to this format. Basically, each EMTerm (like "T01") is mapped with a set of disaster awareness labels, and each mapped label is associated with a confidence score. You can set any confidence score range you want.  
The output disaster awareness labels are obtained according to the accumulated confidence score, either by "topk" rule or by "threshold" rule.  