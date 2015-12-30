# Class Position for project 5
# Jansen Yan 12658454

# We need to do some conversions to go from
# row and column indices --> (x1, y1, x2, y2) coordinates

class Position(object):
    def __init__(self, rowIndex: int, columnIndex: int):
        
        # initializes the coordinates
        
        self.rowIndex = rowIndex
        self.columnIndex = columnIndex

    def convert(self, canvasWidth: int, canvasHeight: int, columnNum: int, rowNum: int) -> (float, float, float, float):
        
        # takes the indexes and converts them into x and y coordinates

        self.x1 = self.columnIndex * (canvasWidth/columnNum)
        self.y1 = self.rowIndex * (canvasHeight/rowNum)
        self.x2 = (self.columnIndex + 1) * (canvasWidth/columnNum)
        self.y2 = (self.rowIndex + 1) * (canvasHeight/rowNum)

        return (self.x1, self.y1, self.x2, self.y2)

    def handle(self, x: float, y: float):
        
        # Handles click event in a separate module, if user clicks within the
        # boundaries of a canvas, return True
        
        if self.x1 < x < self.x2 and self.y1 < y < self.y2:
            return True

class Point(object):
    def __init__(self, x: float, y: float):

        # From point to position

        self.x = x
        self.y = y
        
    def convert(self, canvasWidth: int, canvasHeight: int, columnNum: int, rowNum: int):

        # From point (where user clicked) to column and row index

        self.columnIndex = self.x * (columnNum/canvasWidth)
        self.rowIndex = self.y * (rowNum/canvasHeight)

        return int(self.columnIndex), int(self.rowIndex)



        
