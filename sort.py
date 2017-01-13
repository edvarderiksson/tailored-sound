# contains the sorting algorithms for the playlist searches



# Quicksort

# Need to implement quicksort 

# 50 most popular

def get_fifty(all_songs):
	top_songs = []
	v=list(all_songs.values())
	k=list(all_songs.keys())
	i = 0
	while(i < 50):
		top_songs.append (k[v.pop(v.index(max(v)))])

	return top_songs