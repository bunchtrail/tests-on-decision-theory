# -*- coding: utf-8 -*-
# Программа для моделирования сети Петри

import math

import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch


class PetriNet:
    def __init__(self):
        self.places = {}  # имя места -> количество токенов
        self.transitions = {}  # имя перехода -> {'input': {место: кратность}, 'output': {место: кратность}}

    def add_place(self, place_name, tokens=0):
        self.places[place_name] = tokens

    def add_transition(self, transition_name):
        self.transitions[transition_name] = {'input': {}, 'output': {}}

    def add_input_arc(self, transition_name, place_name, weight=1):
        if place_name in self.transitions[transition_name]['input']:
            self.transitions[transition_name]['input'][place_name] += weight
        else:
            self.transitions[transition_name]['input'][place_name] = weight

    def add_output_arc(self, transition_name, place_name, weight=1):
        if place_name in self.transitions[transition_name]['output']:
            self.transitions[transition_name]['output'][place_name] += weight
        else:
            self.transitions[transition_name]['output'][place_name] = weight

    def is_enabled(self, transition_name):
        input_places = self.transitions[transition_name]['input']
        missing_places = []
        for place, required_tokens in input_places.items():
            if self.places.get(place, 0) < required_tokens:
                missing_places.append(place)
        if missing_places:
            return False, missing_places
        else:
            return True, []

    def fire_transition(self, transition_name):
        enabled, _ = self.is_enabled(transition_name)
        if not enabled:
            return False
        input_places = self.transitions[transition_name]['input']
        output_places = self.transitions[transition_name]['output']
        # Снимаем токены с входных мест
        for place, tokens in input_places.items():
            self.places[place] -= tokens
        # Добавляем токены на выходные места
        for place, tokens in output_places.items():
            self.places[place] += tokens
        return True

    def get_marking(self):
        return [self.places[place] for place in sorted(self.places.keys(), key=lambda x: int(x[1:]))]

    def display_net(self):
        G = nx.DiGraph()
        for place in self.places:
            G.add_node(place, node_type='place', label=place + f' ({self.places[place]})')
        for transition in self.transitions:
            G.add_node(transition, node_type='transition', label=transition)
            # Добавляем дуги от мест к переходам
            for place, multiplicity in self.transitions[transition]['input'].items():
                G.add_edge(place, transition, weight=multiplicity)
            # Добавляем дуги от переходов к местам
            for place, multiplicity in self.transitions[transition]['output'].items():
                G.add_edge(transition, place, weight=multiplicity)

        # Используем kamada_kawai_layout для минимизации пересечений стрелок
        pos = nx.kamada_kawai_layout(G)

        plt.figure(figsize=(14, 10))
        ax = plt.gca()

        # Размеры узлов
        place_size = 2000
        transition_size = 1500

        # Рисуем места (круги)
        place_nodes = [n for n, attr in G.nodes(data=True) if attr['node_type'] == 'place']
        nx.draw_networkx_nodes(G, pos, nodelist=place_nodes, node_shape='o', node_color='skyblue',
                            edgecolors='black', node_size=place_size, ax=ax)

        # Рисуем переходы (прямоугольники)
        transition_nodes = [n for n, attr in G.nodes(data=True) if attr['node_type'] == 'transition']
        nx.draw_networkx_nodes(G, pos, nodelist=transition_nodes, node_shape='s', node_color='lightgreen',
                            edgecolors='black', node_size=transition_size, ax=ax)

        # Рисуем метки узлов
        labels = nx.get_node_attributes(G, 'label')
        nx.draw_networkx_labels(G, pos, labels, font_size=12, font_weight='bold', ax=ax)

        # Рисуем ребра со стрелками
        nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle='-|>', arrowsize=50, edge_color='gray', width=1.5, ax=ax)

        # Добавляем подписи для ребер с весом больше 1
        edge_labels = {(u, v): str(d['weight']) for u, v, d in G.edges(data=True) if d['weight'] > 1}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_color='red', ax=ax)

        plt.axis('equal')
        plt.axis('off')
        plt.title("Сеть Петри", fontsize=16)
        plt.tight_layout()
        plt.show()

def parse_places_input_with_weights(input_str):
    elements = input_str.split()
    place_counts = {}
    for elem in elements:
        if '*' in elem:
            times, place_num = elem.split('*')
            times = int(times)
            place_name = 'p' + place_num
            if place_name in place_counts:
                place_counts[place_name] += times
            else:
                place_counts[place_name] = times
        else:
            place_name = 'p' + elem
            if place_name in place_counts:
                place_counts[place_name] += 1
            else:
                place_counts[place_name] = 1
    return place_counts

def get_test_data():
    return {
        'places': '6',
        'transitions': '4',
        'input_arcs': {
            't1': '1',
            't2': '3',
            't3': '2 3',
            't4': '5 5 5'
        },
        'output_arcs': {
            't1': '2 2 5 5 5',
            't2': '3',
            't3': '4 4 4',
            't4': '3 5 5 5'
        },
        'initial_marking': '201120',
        'transitions_to_fire': '1 2'
    }

def main():
    print("\nПрограмма моделирования сети Петри")
    print("1. Использовать тестовые данные")
    print("2. Ввести данные вручную")

    while True:
        choice = input("\nВыберите режим работы (1/2): ").strip()
        if choice in ['1', '2']:
            break
        print("Пожалуйста, введите 1 или 2")

    test_mode = (choice == '1')

    if test_mode:
        print("\nИспользуются тестовые данные:")
        test_data = get_test_data()
        print(f"Места (P): {test_data['places']}")
        print(f"Переходы (T): {test_data['transitions']}")
        print("Входные дуги (I):")
        for t, arcs in test_data['input_arcs'].items():
            print(f"  {t}: {arcs}")
        print("Выходные дуги (O):")
        for t, arcs in test_data['output_arcs'].items():
            print(f"  {t}: {arcs}")
        print(f"Начальная маркировка (M0): {test_data['initial_marking']}")
        print(f"Переходы для запуска: {test_data['transitions_to_fire']}")

        proceed = input("\nПродолжить? (y/n): ").strip().lower()
        if proceed != 'y':
            print("Программа завершена.")
            return

    net = PetriNet()

    if test_mode:
        test_data = get_test_data()
        places_input = test_data['places']
        transitions_input = test_data['transitions']
    else:
        places_input = input("Места (P): ").strip()
        transitions_input = input("Переходы (T): ").strip()

    place_numbers = places_input.split()
    if len(place_numbers) == 1 and place_numbers[0].isdigit():
        total_places = int(place_numbers[0])
        place_numbers = [str(i) for i in range(1, total_places + 1)]
    for num in place_numbers:
        place_name = 'p' + num
        net.add_place(place_name)
    # Ввод переходов
    transition_numbers = transitions_input.split()
    if len(transition_numbers) == 1 and transition_numbers[0].isdigit():
        total_transitions = int(transition_numbers[0])
        transition_numbers = [str(i) for i in range(1, total_transitions + 1)]
    for num in transition_numbers:
        transition_name = 't' + num
        net.add_transition(transition_name)

    # Ввод входных дуг
    print("Входные дуги (I):")
    for transition_name in net.transitions:
        if test_mode:
            input_str = test_data['input_arcs'][transition_name]
        else:
            input_str = input(f"  {transition_name}: ").strip()
        input_places = parse_places_input_with_weights(input_str)
        for place_name, weight in input_places.items():
            net.add_input_arc(transition_name, place_name, weight)

    # Ввод выходных дуг
    print("Выходные дуги (O):")
    for transition_name in net.transitions:
        if test_mode:
            output_str = test_data['output_arcs'][transition_name]
        else:
            output_str = input(f"  {transition_name}: ").strip()
        output_places = parse_places_input_with_weights(output_str)
        for place_name, weight in output_places.items():
            net.add_output_arc(transition_name, place_name, weight)

    # Ввод начальной маркировки
    if test_mode:
        marking_input = test_data['initial_marking']
    else:
        marking_input = input("Начальная маркировка (M0): ").strip()
    if len(marking_input) != len(net.places):
        print("Ошибка: количество токенов не соответствует количеству мест.")
        return
    sorted_places = sorted(net.places.keys(), key=lambda x: int(x[1:]))
    for i, place_name in enumerate(sorted_places):
        net.places[place_name] = int(marking_input[i])
    # Вывод начальной маркировки
    initial_marking = net.get_marking()
    print("\nНачальная маркировка:")
    print(f"M0 = {initial_marking}")
    # Ввод переходов для запуска
    if test_mode:
        transitions_to_fire_input = test_data['transitions_to_fire']
    else:
        transitions_to_fire_input = input("Переходы для запуска: ").strip()
    transitions_to_fire_numbers = transitions_to_fire_input.split()
    transitions_to_fire = ['t' + num for num in transitions_to_fire_numbers]
    # Моделирование сети
    print("\nПоследовательные расчёты маркировок:")
    for transition_name in transitions_to_fire:
        print(f"M({transition_name}):")
        if transition_name not in net.transitions:
            print(f"Переход {transition_name} не существует.\n")
            continue
        enabled, missing_places = net.is_enabled(transition_name)
        if enabled:
            net.fire_transition(transition_name)
            new_marking = net.get_marking()
            print(f"Маркировка после запуска {transition_name}:")
            print(f"M = {new_marking}\n")
        else:
            missing_places_str = ' или '.join(missing_places)
            print(f"Переход {transition_name} недоступен, так как недостаточно токенов в {missing_places_str}.\n")
    # Отображение сети
    net.display_net()

if __name__ == "__main__":
    main()
