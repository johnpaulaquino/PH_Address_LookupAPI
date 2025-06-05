
class DataCleanerUtils:

    @staticmethod
    def validate_dictionary_key(key: str, dictionary : dict):
        if key not in dictionary.keys():
            raise Exception('Key Not found in the given Dictionary!')
