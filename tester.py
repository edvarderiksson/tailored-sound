# Just a tester class for quick testing from command line
# To be discarded later

import tailor as tlr
import setup as stp

def test_mood():
	query = input("Please enter your mood in one word: \n")
	# songs = tlr.get_mood_songs(query)

	print("so far so good" + query)

	# just hardcoded limit for testing
	LIMIT = 50
	i = 0

	# prints the first 50 songs
	while(i < LIMIT):
		for song in songs:
			print(song)
			i+=1




def auth_tester(query):
	t = stp.main()
	return tlr.get_mood_songs(query,t)







# test_mood()
#auth_tester()