class Item:
    def __init__(self, x_coordinate, y_coordinate, speed, image, type):
            self.__speed = speed
            self.__x_coordinate = x_coordinate
            self.__y_coordinate = y_coordinate
            self.__type = type
            self.__image = image


    def setXpos(self, x):
        self.__x_coordinate = x

    def getXpos(self):
        return self.__x_coordinate

    def setType(self, type):
        self.__type = type

    def setYpos(self, y):
        self.__y_coordinate = y

    def getYpos(self):
        return self.__y_coordinate

    def setSpeed(self, speed):
        self.__speed = speed

    def getSpeed(self):
        return self.__speed

    def addSpeed(self, speed):
        self.__speed += speed

    def getType(self):
        return self.__type

    def setImage(self, image):
      self.__image = image

    def getImage(self):
      return self.__image
