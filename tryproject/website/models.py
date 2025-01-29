from . import mongo

class Risk:
    @staticmethod
    def create(data):
        return mongo.db.risks.insert_one(data)

    @staticmethod
    def get_all():
        return list(mongo.db.risks.find())

class Asset:
    @staticmethod
    def create(data):
        return mongo.db.assets.insert_one(data)

    @staticmethod
    def get_all():
        return list(mongo.db.assets.find())
