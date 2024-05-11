# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------Реализация с Deap-------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
import random
import matplotlib.pyplot as plt
import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

# константы задачи
ONE_MAX_LENGHT = 100  # длина хромосомы (битовой строки)

# константы генетического алгоритма
POPULATION_SIZE = 200  # количество индивидумов в пооуляции
P_CROSSOVER = 0.9  # вероятность скрещивания
P_MUTATION = 0.1  # вероятность мутации индивида
MAX_GENERATIONS = 50  # максимальное количество поколений (количество итераций)

# Для генерации одинаковой последовательности чисел
RANDOM_SEED = 41
random.seed(RANDOM_SEED)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)


def oneMaxFitness(individual):
    return sum(individual),  # кортеж


toolbox = base.Toolbox()
# Создание хромосомы из 100 элементов (либо 0, либо 1 - рандомно)
toolbox.register("zeroOrOne", random.randint, 0, 1)

# Создаем популяцию хромосом
toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGHT)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

population = toolbox.populationCreator(n=POPULATION_SIZE)
generationCounter = 0

# Для каждого индивида из популяции вызываем функцию oneMaxFitness, чтобы рассчитать приспособленность
fitnessValues = list(map(oneMaxFitness, population))  # Список приспособленности каждой особи

# Итерируемся по списку индивидов (то есть по популяции) и соответствующих им приспособленностей
for individual, fitnessValues in zip(population, fitnessValues):
    individual.fitness.values = fitnessValues  # записываем приспособленность индивиду в класс FitnessMax

# Для хранения статистики
maxFitnessValues = []  # Максимальная приспособленность особей в текущей популяции
meanFitnessValues = []  # Средняя приспособленность всех особей в текущей популяции

# Новый список из отобранных особей
toolbox.register("select", tools.selTournament, tournsize=3)

# Формируем потомков (скрещивание)
toolbox.register("mate", tools.cxOnePoint)

# Функция мутации
toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / ONE_MAX_LENGHT)

toolbox.register("evaluate", oneMaxFitness)

stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("max", np.max)
stats.register("avg", np.mean)
stats.register("values", np.array)

population, logbook = algorithms.eaSimple(population, toolbox,
                                          cxpb=P_CROSSOVER,
                                          mutpb=P_MUTATION,
                                          ngen=MAX_GENERATIONS,
                                          stats=stats,
                                          verbose=True)

maxFitnessValues, meanFitnessValues, vals = logbook.select("max", "avg", "values")

# plt.plot(maxFitnessValues, color='red')
# plt.plot(meanFitnessValues, color='green')
# plt.xlabel('Поколение')
# plt.ylabel('Макс/средняя приспособленность')
# plt.title('Зависимость максимальной и средней приспособленности от поколения')
# plt.show()

import time

plt.ion()
fig, ax = plt.subplots()

line, = ax.plot(vals[0], ' .', markersize=1)
ax.set_ylim(0, 110)

for v in vals:
    line.set_ydata(v)

    plt.draw()
    plt.gcf().canvas.flush_events()

    time.sleep(0.5)

plt.ioff()
plt.show()
