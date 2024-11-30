# -*- coding: utf-8 -*-

def decision_analysis():
    # Ввод данных

    # Вариант 1
    variant1 = {
        'E1': [-25, -14, -17],
        'E2': [-16, -25, -27],
        'E3': [-19, -15, -15]
    }
    states1 = ['F1', 'F2', 'F3']

    # Вариант 2
    variant2 = {
        'E1': [-25, -14],
        'E2': [-28, -25],
        'E3': [-29, -15]
    }
    states2 = ['F1', 'F2']

    variants = [
        (1, variant1, states1),
        (2, variant2, states2)
    ]

    for variant_number, data, states in variants:
        print(f"\n=== Вариант {variant_number} ===")

        # Формируем таблицу затрат
        print("\nТаблица затрат:")
        print("       ", end="")
        for state in states:
            print(f"{state:>8}", end="")
        print()
        for decision, losses in data.items():
            print(f"{decision:>5}", end="")
            for loss in losses:
                print(f"{loss:8}", end="")
            print()

        # Критерий минимакса
        print("\n1. Критерий минимакса")
        print("Критерий минимакса фокусируется на минимизации максимальных потерь.")
        max_losses = {}
        for decision, losses in data.items():
            max_loss = max(losses)
            max_losses[decision] = max_loss
            print(f"{decision}: max{losses} = {max_loss}")
        min_of_max_losses = min(max_losses.values())
        best_decisions = [decision for decision, loss in max_losses.items() if loss == min_of_max_losses]
        print(f"\nНаименьшее из максимальных потерь: {min_of_max_losses}")
        print(f"Рекомендуемое решение(я): {', '.join(best_decisions)}")

        # Критерий Байеса-Лапласа
        print("\n2. Критерий Байеса-Лапласа")
        print("Предполагаем равные вероятности для состояний.")
        avg_losses = {}
        num_states = len(states)
        for decision, losses in data.items():
            avg_loss = sum(losses) / num_states
            avg_losses[decision] = avg_loss
            print(f"{decision}: средние потери = ({' + '.join(map(str, losses))}) / {num_states} = {avg_loss:.2f}")
        min_avg_loss = min(avg_losses.values())
        best_decisions_avg = [decision for decision, loss in avg_losses.items() if loss == min_avg_loss]
        print(f"\nНаименьшие средние потери: {min_avg_loss:.2f}")
        print(f"Рекомендуемое решение(я): {', '.join(best_decisions_avg)}")

        # Критерий Сэвиджа
        print("\n3. Критерий Сэвиджа")
        print("Минимизируем максимальное сожаление.")
        # Находим наибольшие потери в каждом состоянии
        max_losses_per_state = []
        for i in range(len(states)):
            state_losses = [losses[i] for losses in data.values()]
            max_loss_state = max(state_losses)
            max_losses_per_state.append(max_loss_state)
            print(f"Максимальные потери в состоянии {states[i]}: max{state_losses} = {max_loss_state}")

        # Строим матрицу сожалений
        print("\nМатрица сожалений:")
        regrets = {}
        for decision, losses in data.items():
            regret_row = []
            for i in range(len(states)):
                regret = max_losses_per_state[i] - losses[i]
                regret_row.append(regret)
            regrets[decision] = regret_row
            print(f"{decision}: {regret_row}")

        # Находим максимальное сожаление для каждого решения
        max_regrets = {}
        for decision, regret_values in regrets.items():
            max_regret = max(regret_values)
            max_regrets[decision] = max_regret
            print(f"{decision}: максимальное сожаление = max{regret_values} = {max_regret}")

        min_of_max_regrets = min(max_regrets.values())
        best_decisions_regret = [decision for decision, regret in max_regrets.items() if regret == min_of_max_regrets]
        print(f"\nНаименьшее из максимальных сожалений: {min_of_max_regrets}")
        print(f"Рекомендуемое решение(я): {', '.join(best_decisions_regret)}")

if __name__ == "__main__":
    decision_analysis()
