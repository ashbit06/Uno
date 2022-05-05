def getKeysFromValue(d, val):
	# https://github.com/nkmk/python-snippets/blob/3c58602bfb74f604a9d33ecac5a0ae6a8002fb63/notebook/dict_get_key_from_value.py#L31-L36
    return [k for k, v in d.items() if v == val]
