class BodyAreaNotFoundException(Exception):
    def __init__(self, body_area_id: int):
        super().__init__(f'Body area with id {body_area_id} not found')