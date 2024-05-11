# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------Реализация без Deap-----------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
import random
import matplotlib.pyplot as plt

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


class FitnessMax():
    def __init__(self):
        self.values = [0]  # Создаем свойство, содержащее приспособленность особи


class Individual(list):
    def __init__(self, *args):
        super().__init__(*args)
        self.fitness = FitnessMax()  # Создаем в конструкторе дополнительный класс для хранения приспособленности


def oneMaxFitness(individual):
    return sum(individual),  # кортеж


# Создание хромосомы из 100 элементов (либо 0, либо 1 - рандомно)
# Вызывает класс индивида
def individualCreator():
    return Individual([random.randint(0, 1) for i in range(ONE_MAX_LENGHT)])


# Создаем популяцию хромосом
def populationCreator(n=0):
    return list([individualCreator() for i in range(n)])


population = populationCreator(n=POPULATION_SIZE)
generationCounter = 0

# Для каждого индивида из популяции вызываем функцию oneMaxFitness, чтобы рассчитать приспособленность
fitnessValues = list(map(oneMaxFitness, population))  # Список приспособленности каждой особи

# Итерируемся по списку индивидов (то есть по популяции) и соответствующих им приспособленностей
for individual, fitnessValues in zip(population, fitnessValues):
    individual.fitness.values = fitnessValues  # записываем приспособленность индивиду в класс FitnessMax

# Для хранения статистики
maxFitnessValues = []  # Максимальная приспособленность особей в текущей популяции
meanFitnessValues = []  # Средняя приспособленность всех особей в текущей популяции


# Функция клонирования отдельного индивидуума. Нужна для того, чтобы после отбора, нужно будет проклонировать
# каждого индивидуума. Потому что в процессе отбора может быть отобран один и тот же индивидуум дважды и тогда
# в популяции будет две ссылки на один и тот же список. Каждый индивидуум должен представлен отдельным списком, поэтому
# используем клонирование.
def clone(value):
    ind = Individual(value[:])
    ind.fitness.values[0] = value.fitness.values[0]
    return ind


# Новый список из отобранных особей
def selTournament(population, p_len):
    offspring = []
    # Цикл по популяции
    for n in range(p_len):
        i1 = i2 = i3 = 0
        # Случайным оборазом отбираем 3 особи
        while i1 == i2 or i1 == i3 or i2 == i3:
            i1, i2, i3 = random.randint(0, p_len - 1), random.randint(0, p_len - 1), random.randint(0, p_len - 1)
        # Выбираем особь с максимальной приспособленностью (по key)
        offspring.append(max([population[i1], population[i2], population[i3]], key=lambda ind: ind.fitness.values[0]))
    return offspring


# Формируем потомков
def cxOnePoint(child1, child2):
    s = random.randint(2, len(child1) - 3)  # точка разреза хромосомы
    child1[s:], child2[s:] = child2[s:], child1[s:]


# Функция мутации
def mutFlipBit(mutant, indpb=0.01):
    for indx in range(len(mutant)):
        if random.random() < indpb:
            mutant[indx] = 0 if mutant[indx] == 1 else 1


# Коллекция значений приспособленности данной популяции
fitnessValues = [individual.fitness.values[0] for individual in population]

# Цикл генетического алгоритма
# max(fitnessValues) < ONE_MAX_LENGHT - условие нахождение лучшего решения, то есть когда сумма членов хромосомы = 100
# generationCounter < MAX_GENERATIONS - условие ограничения по количеству поколений
while max(fitnessValues) < ONE_MAX_LENGHT and generationCounter < MAX_GENERATIONS:
    generationCounter += 1  # Подсчет числа поколений
    offspring = selTournament(population, len(population))  # Отбор лучших особей
    offspring = list(map(clone, offspring))  # Клонирование лучших особей для нового списка

    # Скрещивание
    # Берем четные и нечетные по порядку элементы
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < P_CROSSOVER:
            cxOnePoint(child1, child2)

    # Мутация
    for mutant in offspring:
        if random.random() < P_MUTATION:
            mutFlipBit(mutant, indpb=1.0/ONE_MAX_LENGHT)

    # Расчет приспособленностей всех индивидов популяции
    freshFitnessValue = list(map(oneMaxFitness, offspring))
    for individual, fitnessValue in zip(offspring, freshFitnessValue):
        individual.fitness.values = fitnessValue

    # Обновляем список популяции
    population[:] = offspring

    # Обновляем список приспособленности популяции
    fitnessValues = [ind.fitness.values[0] for ind in population]

    # Определяем максимальную и среднюю приспособленности
    maxFitness = max(fitnessValues)
    meanFitness = sum(fitnessValues) / len(population)
    maxFitnessValues.append(maxFitness)
    meanFitnessValues.append(meanFitness)

    print(f"Поколение {generationCounter}: Макс. приспособ. = {maxFitness}, Средняя приспособ. = {meanFitness}")

    best_index = fitnessValues.index(max(fitnessValues))

    print("Лучший индивид = ", *population[best_index], "\n")

plt.plot(maxFitnessValues, color='red')
plt.plot(meanFitnessValues, color='green')
plt.xlabel('Поколение')
plt.ylabel('Макс/средняя приспособленность')
plt.title('Зависимость максимальной и средней приспособленности от поколения')
plt.show()