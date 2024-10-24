import pandas as pd

df = pd.read_csv('FAVA_rels.csv')
# Group by subject, object, and relationship, and count occurrences (weight)
df_grouped = df.groupby(['subj', 'obj', 'rel']).size().reset_index(name='weight')

# Save the processed data to a new CSV
df_grouped.to_csv('knowledge_graph_data.csv', index=False)
print("Data has been processed and saved to 'knowledge_graph_data.csv'")