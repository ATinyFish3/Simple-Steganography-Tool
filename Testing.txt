Enter invalid input at menu - returns to menu

Enter Q at menu - program exits

Enter E at menu - takes to encoding part of code, asks for text
	
	Enter no text - asks user to enter non null text, gets input again
	Enter endStatement (!STOP!) - says cannot enter that, gets input again
	Enter text - succeeds, asks user if they want to encrypt, no encrypt or cancel
		
		Enter C - returns to menu
		Enter E - text is encrypted, user asked to select image
		Enter U - text not encrypted, user asked to selcet image
			
			Select image - no errors, user is asked to save image
				User cancels - given choice to cancel or select location again
					Press enter - Asked for location to save to again
					Enter C - Taken back to menu

			Select non-image file - asks user to select image file 
					Press enter - Asked for location to save to again
					Enter C - Taken back to menu
				
			Cancel - given choice to cancel or select location again
					Press enter - Asked for location to save to again
					Enter C - Taken back to menu

				Enter invalid filename - says cannot name file that and asks again
					Cancel - given choice to cancel or select location again
						Press enter - Asked for location to save to again
						Enter C - Taken back to menu

Enter D at menu - takes to decoding part of code, asks user to select file

	Cancel - given choice to cancel or select location again
		Press enter - Asked for location to save to again
		Enter C - Taken back to menu

	Select non-image file - asks user to select image file 
		Press enter - Asked for location to save to again
		Enter C - Taken back to menu


	Select image file

		Image contains message - outputs message

		Image has no message - says no message found


Enter C at menu - asks user to select image

	Cancel - given choice to cancel or select location again
		Press enter - Asked for location to save to again
		Enter C - Taken back to menu

	Select non-image file - asks user to select image file 
		Press enter - Asked for location to save to again
		Enter C - Taken back to menu


	Select image file - outputs all data
