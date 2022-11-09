class V3(object):
    def __init__(self, x, y, z = 0):
        #Recibiendo una lista de 3 elementos; z puede ser opcional.
        self.x = x
        self.y = y
        self.z = z

    def round(self):
       self.x = round(self.x)
       self.y = round(self.y)
       self.z = round(self.z)


    #Overload de la suma. Este recibe un V3 y el otro vector a operar.
    def __add__(self, other): #Este usa +.
        
        return V3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z
        )

    #Ovoerload de la resta.
    def __sub__(self, other): #Este usa -. Este recibe un V3 y el otro vector a operar.

        return V3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.y
        )

    #Si el producto punto es 1, entonces los dos vectores tienen la misma dirección.
    #Si el producto punto es 0, los dos vectores son perpendiculares.
    #Si el producto punto -1, entonces los dos vectores tienen direcciones opuestas.

    def __matmul__(self, other): #Overload para el producto punto de vectores. Este usa @.
        return self.x * other.x + self.y * other.y + self.z * other.z 

    #Overload de la multiplicación. Este usa * y tiene también el producto cruz.
    def __mul__(self, other): #Este usa *.
        
        if(type(other) == int or type(other) == float): #Si el otro argumento es un entero o un float.
            
            return V3(
                self.x * other,
                self.y * other,
                self.z * other
            )

        #Producto cruz entre dos vectores. Este funciona en vectores de tres dimensiones. Funciona solamente si hay dos vectores usando el *.
        return (
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def len(self): #Calcula la longitud del vector.
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def normalice(self):#Normaliza el vector.

        try: #Si el vector no es cero, entonces normaliza.
            return self * (1 / self.len())
        except: #Si el vector es cero, entonces devuelve un vector cero.
            return V3(-1, -1, -1)

    def __repr__(self): #Overloading de la funcion __repr__
        #Devuelve una cadena que representa el objeto.
        return("V3(%s, %s, %s)" % (self.x, self.y, self.z))