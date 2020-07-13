import sqlite3

conn = sqlite3.connect('spider.sqlite')
cur = conn.cursor()

#get all the distinct from_id from the Links Table
cur.execute('SELECT DISTINCT from_id FROM Links')
from_ids = list()
for row in cur:
    from_ids.append(row[0])


to_ids = list()
links = list()
#get a distinct combination of from_id and to_id from the Links Table
cur.execute('SELECT DISTINCT from_id, to_id FROM Links')
for row in cur:
    from_id = row[0]
    to_id = row[1]
    #to make sure the pages don't point to themselves
    if from_id == to_id:
        continue
    if from_id not in from_ids:
        continue
    '''to make sure that every to_id is a from_id for another page,
    #i.e. to make sure that the pages are connected to each other.
    '''
    if to_id not in from_ids: 
        continue
    links.append(row)
    if to_id not in to_ids:
        to_ids.append(to_id)

'''
from the from_id, we are accessing the data of Pages Table
here we set the new_rank of the Page as the old_rank of the page
'''
prev_ranks = dict()
for node in from_ids:
    cur.execute('''SELECT new_rank FROM Pages WHERE id = ?''', (node, ))
    row = cur.fetchone()
    prev_ranks[node] = row[0]

sval = input('How many iterations: ')
many = 1
if len(sval) > 0:
    many = int(sval)

if len(prev_ranks) < 1:
    print('Nothing to page rank. Check Data')
    quit()


for i in range(many):
    next_ranks = dict()
    total = 0.0
    for (node, old_rank) in list(prev_ranks.items()):
        total = total + old_rank
        next_ranks[node] = 0.0

    for (node, old_rank) in list(prev_ranks.items()):
        #HERE NODE IS THE from_id
        #give_id stores the id of the pages which are attached with this node
        give_ids = list()

        #here we traverse from all the links we have and find the one
        #with the same from_id as node.
        #we also find out the number of pages linked to this page.
        for(from_id, to_id) in links:
            if from_id != node:
                continue
            
            if to_id not in to_ids:
                continue
            
            give_ids.append(to_id)

        if len(give_ids) < 1:
            continue
        
        amount = old_rank/len(give_ids)

        '''
        We will update the rank of the pages to which this page is connected as well.
        '''
        for id in give_ids:
            next_ranks[id] = next_ranks[id] + amount

    newtotal = 0

    for (node, next_rank) in list(next_ranks.items()):
        newtotal += next_rank

    #finding out the average of the difference between the total of old ranks and new ranks.
    evap = (total - newtotal)/len(next_ranks)

    for node in next_ranks:
        next_ranks[node] = next_ranks[node] + evap

    newtotal = 0
    for (node, next_rank) in list(next_ranks.items()):
        newtotal = newtotal + next_rank
    
    '''
    Just to check the convergence of the algorithm
    '''
    totaldiff = 0
    for (node, old_rank) in list(prev_ranks.items()):
        new_rank = next_ranks[node]
        diff = abs(old_rank - new_rank)
        totaldiff = totaldiff + diff

    average_diff = totaldiff/len(prev_ranks)
    print(i+1, average_diff)

    #rotate after each iteration
    prev_ranks = next_ranks

print(list(next_ranks.items())[:5])
cur.execute('''
    UPDATE Pages SET old_rank = new_rank
''')
for (id, new_rank) in list(next_ranks.items()):
    cur.execute('''
        UPDATE Pages SET new_rank = ? WHERE id = ?
    ''', (new_rank, id))
conn.commit()
cur.close()

            
