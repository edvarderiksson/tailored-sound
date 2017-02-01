# contains the sorting algorithms for the playlist searches

# 50 most popular

def get_fifty(d):
	songs = sorted(d, key=d.get)
	top_songs = []

	i = 0
	# add lenght methods for dictionaries shorter than 50
	while(i < 50):
		top_songs.append(songs[i])
		i+=1

	return top_songs