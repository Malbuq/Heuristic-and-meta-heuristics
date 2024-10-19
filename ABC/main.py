from abc import ABC, abstractmethod
import copy
import random

class Solution():
    def __init__(self, leftDomainBound, rightDomainBound, dimensionSize):
        self.position = [random.randint(leftDomainBound, rightDomainBound) for _ in range(dimensionSize)]
        self.fitness = 0
        self.improveAttemptCount = 0
