class Airplane:
    def __init__(self, code, name, rows_cols):
        self.code = code
        self.name = name
        self.rows_cols = rows_cols
        self.capacity = int(rows_cols.strip().split('/')[0]) * int(rows_cols.strip().split('/')[1])