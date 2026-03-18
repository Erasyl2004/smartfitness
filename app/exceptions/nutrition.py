
class UnprocessableNutritionException(Exception):
    def __init__(self,):
        super().__init__("Couldn't identify the food or estimate its nutritional values from this image")