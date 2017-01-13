# Just a tester class for quick testing from command line
# To be discarded later

import tailor as tlr
import setup as stp

def auth_tester(query):

	# return tlr.get_mood_songs(query)
	t = stp.basic_credentials()
	return tlr.get_mood_songs(query,t)








# test_mood()
#auth_tester()
