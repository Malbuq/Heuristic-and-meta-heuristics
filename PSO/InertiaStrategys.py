from abc import ABC, abstractmethod

class IntertiaStrategy(ABC):
    @abstractmethod
    def calculate_intertia(self):
        pass

class ConstantIntertia(IntertiaStrategy):
    def __init__(self, constantInertia):
        self.constantIntertiaValue = constantInertia

    def calculate_intertia(self, total_iterations):
        return self.constantIntertiaValue
    
class LinearDescentInertia(IntertiaStrategy):
    def __init__(self, wMin, wMax, total_iterations):
        self.wMax = wMax
        self.wMin = wMin
        self.total_iterations = total_iterations

    def calculate_intertia(self, current_index_iteration):
        return (self.wMax - self.wMin)*((self.total_iterations - current_index_iteration)/self.total_iterations) + self.wMin
