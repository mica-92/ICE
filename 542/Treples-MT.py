import random
from collections import Counter

# Create a random dataset
# Note: Assuming that the data is in chronological order
times = [x for x in range(500)] 
users = [x for x in range(50)]
pages = [x for x in range(5)]
rows = [{"user": random.choice(users), "page": random.choice(pages)} for time in times] 

# Group pages visited by a unique user together
# Keys: user, Values: [page_visited_by_user, ...]
user_dict = {}
for row in rows:
    user, page = row["user"], row["page"]
    if not user in user_dict.keys(): user_dict[user] = []
    user_dict[user].append(page) 

# Create a list of the triples from all users
triplet_list = []
for users_pages in [x for x in user_dict.values() if len(x) > 2]:
    for index, user_page in enumerate(users_pages[:-2]):
        triplet_list.append((user_page, users_pages[index+1], users_pages[index+2]))

# Find the most common triples and how many times they occur
most_common_triplets = Counter(triplet_list).most_common(10)

# Print the solution
for triplet in most_common_triplets:
    print(f'The triple {triplet[0]} occurred {triplet[1]} times')
