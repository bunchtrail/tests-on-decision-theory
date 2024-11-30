import json

import matplotlib.pyplot as plt
import networkx as nx


def parse_input():
    print("\n=== Упрощённый ввод данных сети Петри ===")
    print("\nФормат ввода:")
    print("1. Количество мест: одно число, например: 6")
    print("   (будет преобразовано в p1 p2 p3 p4 p5 p6)")
    print("2. Количество переходов: одно число, например: 4")
    print("   (будет преобразовано в t1 t2 t3 t4)")
    print("3. Входные дуги: для каждого перехода вводите номера мест через пробел или в формате 'количество*место', например: '1 2' или '3*5'")
    print("   (например, '3*5' означает p5 p5 p5)")
    print("4. Выходные дуги: аналогично входным")
    print("5. Начальная маркировка: одно число без пробелов для каждого места, например: 201120")
    print("6. Переходы для запуска: номера переходов через пробел, например: 1 3\n")

    try:
        print("\n--- Ввод мест ---")
        num_places = int(input("Введите количество мест: "))
        places = [f"p{p}" for p in range(1, num_places + 1)]
        
        print("\n--- Ввод переходов ---")
        num_transitions = int(input("Введите количество переходов: "))
        transitions = [f"t{t}" for t in range(1, num_transitions + 1)]

        print("\n--- Ввод входных дуг ---")
        input_arcs = {}
        for t in transitions:
            user_input = input(f"{t}: ").strip().split()
            input_arcs[t] = []
            for item in user_input:
                if '*' in item:
                    count, place = item.split('*')
                    input_arcs[t].extend([f"p{place}"] * int(count))
                else:
                    input_arcs[t].append(f"p{item}")
        
        print("\n--- Ввод выходных дуг ---")
        output_arcs = {}
        for t in transitions:
            user_input = input(f"{t}: ").strip().split()
            output_arcs[t] = []
            for item in user_input:
                if '*' in item:
                    count, place = item.split('*')
                    output_arcs[t].extend([f"p{place}"] * int(count))
                else:
                    output_arcs[t].append(f"p{item}")

        print("\n--- Ввод начальной маркировки ---")
        print(f"Введите {len(places)} чисел без пробелов:")
        marking_input = input("Маркировка: ").strip()
        if len(marking_input) != len(places):
            raise ValueError("Количество токенов не соответствует количеству мест.")
        initial_marking_values = [int(char) for char in marking_input]
        initial_marking = dict(zip(places, initial_marking_values))

        print("\n--- Ввод переходов для запуска ---")
        print("Введите номера переходов через пробел:")
        fired_transitions = [f"t{t}" for t in input("Запуск: ").strip().split()]
        if not fired_transitions:
            fired_transitions = [transitions[0]]

        return {
            'places': places,
            'transitions': transitions,
            'input_arcs': input_arcs,
            'output_arcs': output_arcs,
            'initial_marking': initial_marking,
            'fired_transitions': fired_transitions
        }

    except Exception as e:
        print(f"\nОшибка при вводе данных: {str(e)}")
        print("Будут использованы данные по умолчанию.")
        return {
            'places': ['p1', 'p2', 'p3'],
            'transitions': ['t1', 't2'],
            'input_arcs': {'t1': ['p1'], 't2': ['p2']},
            'output_arcs': {'t1': ['p2'], 't2': ['p3']},
            'initial_marking': {'p1': 1, 'p2': 0, 'p3': 0},
            'fired_transitions': ['t1']
        }

class PetriNet:
    def __init__(self, data):
        self.places = data['places']
        self.transitions = data['transitions']
        self.input_arcs = data['input_arcs']
        self.output_arcs = data['output_arcs']
        self.marking = data['initial_marking']
        self.graph = nx.DiGraph()
        self.build_graph()
        print("Инициализация сети Петри...")
        print(f"Начальная маркировка: {self.marking}")

    def build_graph(self):
        # Build the Petri net graph
        for t in self.transitions:
            inputs = self.input_arcs.get(t, [])
            outputs = self.output_arcs.get(t, [])
            for p in inputs:
                self.graph.add_edge(p, t)
            for p in outputs:
                self.graph.add_edge(t, p)

    def is_transition_enabled(self, transition):
        inputs = self.input_arcs.get(transition, [])
        enabled = all(self.marking.get(p, 0) >= inputs.count(p) for p in set(inputs))
        status = "доступен" if enabled else "недоступен"
        print(f"Проверка доступности перехода {transition}: {status}.")
        return enabled

    def fire_transition(self, transition):
        if self.is_transition_enabled(transition):
            print(f"\nЗапуск перехода {transition}...")
            inputs = self.input_arcs.get(transition, [])
            outputs = self.output_arcs.get(transition, [])
            print(f"Маркировка перед переходом {transition}: {self.marking}")
            for p in inputs:
                self.marking[p] -= 1
            for p in outputs:
                if p[-1].isdigit():
                    count = int(p[-1])
                    place = p[:-1]
                    self.marking[place] = self.marking.get(place, 0) + count
                else:
                    self.marking[p] = self.marking.get(p, 0) + 1
            print(f"Новая маркировка после перехода {transition}: {self.marking}")
            return True
        else:
            unavailable_places = [p for p in self.input_arcs[transition] if self.marking.get(p, 0) < self.input_arcs[transition].count(p)]
            unavailable_str = " или ".join(unavailable_places)
            print(f"\nПереход {transition} недоступен, так как недостаточно токенов в {unavailable_str}.")
            return False

    def run_transitions(self, transitions):
        results = {}
        for t in transitions:
            if self.fire_transition(t):
                marking_list = ''.join(str(self.marking.get(p, 0)) for p in self.places)
                results[t] = marking_list
            else:
                results[t] = "НЕТ ЗАПУСКА"
        return results

    def visualize(self):
        # Create a complete graph first
        for p in self.places:
            self.graph.add_node(p)
        for t in self.transitions:
            self.graph.add_node(t)
            
        pos = nx.spring_layout(self.graph, k=1, iterations=50)  # Adjust layout parameters
        labels = {}
        for node in self.graph.nodes():
            if node in self.places:
                labels[node] = f"{node}\n{self.marking.get(node, 0)}"
            else:
                labels[node] = node
                
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.places, 
                             node_shape='o', node_color='lightblue', 
                             node_size=700)
        nx.draw_networkx_nodes(self.graph, pos, nodelist=self.transitions, 
                             node_shape='s', node_color='lightgreen', 
                             node_size=500)
        nx.draw_networkx_labels(self.graph, pos, labels=labels)
        nx.draw_networkx_edges(self.graph, pos, arrows=True)
        plt.axis('off')
        plt.show()
def main():
    data = parse_input()
    petri_net = PetriNet(data)
    
    results = petri_net.run_transitions(data['fired_transitions'])
    
    print("\nГраф сети Петри:")
    petri_net.visualize()
    
    print("\nПоследовательные расчёты маркировок:")
    initial_marking_str = ''.join(str(data['initial_marking'][p]) for p in data['places'])
    print(f"M = {initial_marking_str}")
    for t, result in results.items():
        print(f"M{t[-1]} = {result}")

    print(f"\nИтоговая маркировка: {petri_net.marking}")

if __name__ == "__main__":
    main()
