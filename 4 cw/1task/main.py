from collections import defaultdict


def get_votes():
    votes = []
    total_voters = 0
    print("Введите количество избирателей и их предпочтения в формате: 24 A B C")
    print("Введите пустую строку для завершения ввода.")
    while True:
        entry = input("Введите данные: ")
        if entry == '':
            break
        try:
            parts = entry.split()
            if len(parts) != 4:
                print("Неверный формат. Используйте формат: 24 A B C")
                continue
                
            count = int(parts[0])
            preferences = [p.upper() for p in parts[1:]]
            
            if len(preferences) != 3 or not all(p in ['A', 'B', 'C'] for p in preferences):
                print("Пожалуйста, введите предпочтения для всех трех кандидатов (A, B, C).")
                continue
            
            votes.append((count, preferences))
            total_voters += count
        except ValueError:
            print("Неверный формат числа избирателей. Попробуйте снова.")
        except Exception as e:
            print("Неверный формат ввода. Попробуйте снова.")
    return votes, total_voters

def condorcet_method(votes, candidates):
    print("\nРешение Кондорсе")
    pairwise = defaultdict(int)
    for a in candidates:
        for b in candidates:
            if a != b:
                for count, prefs in votes:
                    if prefs.index(a) < prefs.index(b):
                        pairwise[(a, b)] += count
    print("\nСравниваем кандидатов:")
    results = {}
    for a in candidates:
        for b in candidates:
            if a != b:
                a_beats_b = pairwise[(a, b)]
                b_beats_a = sum(count for count, prefs in votes if prefs.index(b) < prefs.index(a))
                print(f"{a} vs {b}:")
                print(f"{a} лучше {b}: {a_beats_b}")
                print(f"{b} лучше {a}: {b_beats_a}\n")
                if a_beats_b > b_beats_a:
                    results[a] = results.get(a, 0) + 1
                else:
                    results[b] = results.get(b, 0) + 1
    winner = max(results, key=results.get)
    print(f"Ответ: Побеждает кандидат {winner} по методу Кондорсе.\n")
    return winner

def borda_method(votes, candidates):
    print("Решение: Борда\n")
    scores = defaultdict(int)
    num_candidates = len(candidates)
    detailed_scores = {candidate: [] for candidate in candidates}
    
    for count, prefs in votes:
        for i, candidate in enumerate(prefs):
            score = (num_candidates - i) * count
            scores[candidate] += score
            detailed_scores[candidate].append(f"{count}⋅{num_candidates - i}")
    
    for candidate in candidates:
        detailed_calculation = " + ".join(detailed_scores[candidate])
        detailed_sum = " + ".join(str((num_candidates - i) * count) for count, prefs in votes for i, c in enumerate(prefs) if c == candidate)
        total_score = scores[candidate]
        print(f"Кандидат {candidate}:")
        print(f"{detailed_calculation} = {detailed_sum} = {total_score}\n")
    
    winner = max(scores, key=scores.get)
    print(f"Ответ: Побеждает кандидат {winner} по методу Борда.\n")
    return winner

def display_votes(votes, total_voters):
    print("\nРешение:")
    print("Число голосующих и предпочтения:\n")
    print(f"{'Число голосующих':<20}{'Предпочтения'}")
    for count, prefs in votes:
        print(f"{count:<20}{'→'.join(prefs)}")
    print(f"Сумма: {total_voters}\n")

def main():
    candidates = ['A', 'B', 'C']
    votes, total_voters = get_votes()
    if not votes:
        print("Нет введенных голосов. Завершение программы.")
        return
    display_votes(votes, total_voters)
    condorcet_winner = condorcet_method(votes, candidates)
    borda_winner = borda_method(votes, candidates)
    print("Результат:")
    print(f"Победитель по методу Кондорсе: {condorcet_winner}")
    print(f"Победитель по методу Борда: {borda_winner}")

if __name__ == "__main__":
    main()
