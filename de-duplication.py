import recordlinkage
import pandas as pd
path = "C:/Users/DELL/Desktop/Data-de-duplication/Deduplication Problem - Sample Dataset.csv"
df = pd.read_csv(path)

print (df)

indexer = recordlinkage.FullIndex()
pairs = indexer.index(df)

print (len(df), len(pairs))
print (pairs)

indexer = recordlinkage.BlockIndex(on=['dob','gn'])
pairs = indexer.index(df)

print (len(pairs))
# (1000*1000-1000)/2 = 499500

# This cell can take some time to compute.
compare_cl = recordlinkage.Compare()

compare_cl.string('ln', 'ln', label='last_name')
compare_cl.string('fn', 'fn', method='jarowinkler', threshold=0.85, label='first_name')
compare_cl.exact('dob', 'dob', label='date_of_birth')
compare_cl.exact('gn', 'gn', label='gender')



features = compare_cl.compute(pairs, df)
print (features)
print ("length of features",len(features))
print (features.describe())

# Sum the comparison results.
a=features.sum(axis=1).value_counts()
print (a)

matches = features[features.sum(axis=1) > 3]
print ("---------------------------")
print(matches)
print  (len(matches))


