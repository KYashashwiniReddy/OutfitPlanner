from src.dao.plan_dao import plan_dao

class PlanService:
    def add_plan(self, user_id, outfit_id, plan_date):
        return plan_dao.add_plan(user_id, outfit_id, plan_date)

    def list_plans(self, user_id, limit=100):
        return plan_dao.list_plans(user_id, limit)

    def search_plans(self, user_id, keyword):
        return plan_dao.search_plans(user_id, keyword)


plan_service = PlanService()
