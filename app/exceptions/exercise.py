class ExerciseNotFoundException(Exception):
    def __init__(self, exercise_id: int):
        super().__init__(f'Exercise with id {exercise_id} not found')