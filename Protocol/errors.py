class SlotErrorNotification(Exception):
    """
    One of the following situations may raise this error:
    	1. Slot not operational yet
    	2. Multiple slots with the same ID
    	3. Slot not reserved yet
    	4. Slot not assigned to the invoking user
    """

class RemoteClientNotification(Exception):
	"""
    One of the following situations may raise this error:
    	1. Remote user not connected yet
    	2. Remote user and invoking user coincide 
    	   (i.e. MCC and GSS are the same)
    """