# LISM

Frequent Itemset Mining (FISM) finds the large and frequently occurring items from the datasets using Apriori algorithm. The FISM framework does not addresses two major properties that are Mixture-of property(more than one customer intent) and Projection-of property. To overcome the problems of irrelevant and non actionable data and also to address the properties mentioned above, Logical Itemset Mining (LISM) framework is introduced. 

LISM finds logical itemsets from the data which helps in eliminating non actionable data but at the same time keeps data which is logically connected. LISM not only finds logically connected items but aso items which are rarely occurring but logically connected are also discovered. LISM also addresses the Mixture of property and Projection of property which are not very well addressed in FISM. The project deals with applications of graph algorithms to data mining field. We have

considered following applications from data mining field,

• Detection of key phrases in documents/web pages for indexing and classification.

• Product recommendations using e-commerce transactions data.

In each of these applications, the data model is a bag of items where items are physical goods bought on e-commerce site or words in documents. These bag-of-items are generated using the steps in the Algorithm stated in LISM.

Natural issue faced in graph based representations for such problems is that of scale. In realistic applications, the number of nodes in graph representations might even run into millions. To effectively deal with scale issues we have exploited distributed computing methodology of map-reduce/Hadoop paradigm. Origins of these work are in Logical Item set Mining methodology highlighted in

‘Logical Itemset Mining’, applied to product recommendations. Their data model is however generic and it can be applied to other problem domain. LISM treats each item in a bag of items as a mixture-of, projection-of, latent concepts. The data is represented as nodes of a graph and co-occurrence of items is represented by the edge weight of each graph. The algorithms finds groups of conceptually related items.
