from src.dao.outfit_dao import outfit_dao

class OutfitService:
    def add_outfit(self, user_id, name, occasion=None, item_ids=None):
        return outfit_dao.add_outfit(user_id=user_id, name=name, occasion=occasion, item_ids=item_ids)

    def list_outfits(self, user_id):
        return outfit_dao.list_outfits(user_id=user_id, limit=100)

    def search_outfits(self, user_id, keyword):
        return outfit_dao.search_outfits(user_id=user_id, keyword=keyword)

outfit_service = OutfitService()
