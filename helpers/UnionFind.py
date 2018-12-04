class UnionFind():
    '''
    'lazy' implementation of the Union Find data structure with path compression using rank

    This data structure does not actually touch the underling data. It just effeciently keeps track of groups.

    The ids that it uses are the ids in some external dataset
    '''

    def __init__(self,num_items):
        '''
        initialize the datastructure. 
        num_items: the number of items that we are working with
        '''
        self.num_items = num_items
        self.parent = [idx for idx in range(num_items+1)] # each item's parent starts out as itself
        self.num_groups = num_items
        self.rank = [0 for x in range(num_items+1)] # number of children each id has

    def find(self,id):
        '''
        Given an id of an item, return the name of the group it belongs to.
        Does this by following parents
        This modifies the parent data structure as it goes, doing path compression
        '''
        parent_id = self.parent[id]
        parent_parent_id = self.parent[parent_id]
        if parent_id != parent_parent_id:
            self.parent[id] = self.find(parent_id)
        return self.parent[id]

    def union(self,id1,id2):
        '''
        Merge items id1 and id2 by their rank
        '''
        if self.rank[id1] > self.rank[id2]:
            self.parent[id2] = id1
        elif self.rank[id1] < self.rank[id2]:
            self.parent[id1] = id2
        else:
            self.parent[id2] = id1
            self.rank[id1] += 1

        self.num_groups -= 1

    def union_if_unique(self,id1,id2):
        '''
        If id1 and id2 are not already in the same group, merge them
        '''
        parent1 = self.find(id1)
        parent2 = self.find(id2)
        if not self.same_parents(id1,id2):
            self.union(parent1,parent2)

    def same_parents(self,id1,id2):
        '''
        Return True if id1 and id2 have the same parents/are in same cluster.
        Otherwise return False
        '''
        parent1 = self.find(id1)
        parent2 = self.find(id2)
        if parent1 == parent2:
            return True
        else:
            return False