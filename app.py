import re

def is_valid_card_number(card_number):
    """
    Verifica se o número do cartão de crédito é válido usando o Algoritmo de Luhn.

    Args:
        card_number (str): O número do cartão de crédito.

    Returns:
        bool: True se for válido, False caso contrário.
    """
    card_number = card_number.replace(" ", "")  # Remove espaços
    if not card_number.isdigit():
        return False
    
    total = 0
    reverse_digits = card_number[::-1]
    for i, digit in enumerate(reverse_digits):
        n = int(digit)
        if i % 2 == 1:  # Dobra os dígitos nas posições pares (a partir do fim)
            n *= 2
            if n > 9:
                n -= 9
        total += n
    return total % 10 == 0

def detect_fraud(card_number, document_info):
    """
    Analisa possíveis fraudes com base em padrões.

    Args:
        card_number (str): O número do cartão de crédito.
        document_info (dict): Informações do documento, como nome, CPF, etc.

    Returns:
        list: Lista de alertas de possíveis fraudes.
    """
    alerts = []

    # Validação do número do cartão
    if not is_valid_card_number(card_number):
        alerts.append("Número do cartão inválido.")

    # Validação do CPF
    cpf = document_info.get("cpf", "")
    if not re.match(r"^\d{11}$", cpf):
        alerts.append("CPF inválido. Deve conter 11 dígitos.")

    # Regras de negócio (exemplo simples)
    # Regra 1: Cartão e CPF com padrões suspeitos (mesmos dígitos repetidos)
    if re.match(r"^(\d)\1+$", card_number):
        alerts.append("Número do cartão suspeito (mesmo dígito repetido).")
    if re.match(r"^(\d)\1+$", cpf):
        alerts.append("CPF suspeito (mesmo dígito repetido).")

    # Regra 2: Nome muito curto ou vazio
    name = document_info.get("name", "").strip()
    if len(name) < 3:
        alerts.append("Nome inválido ou muito curto.")

    # Regra 3: Limite de idade (caso tenha um campo de idade)
    age = document_info.get("age", 0)
    if age < 18 or age > 120:
        alerts.append("Idade fora do intervalo permitido (18-120 anos).")

    return alerts

def main():
    print("=== Análise Básica de Antifraude ===")
    card_number = input("Digite o número do cartão de crédito: ").strip()
    name = input("Digite o nome completo: ").strip()
    cpf = input("Digite o CPF (somente números): ").strip()
    age = int(input("Digite a idade: ").strip())

    document_info = {"name": name, "cpf": cpf, "age": age}
    alerts = detect_fraud(card_number, document_info)

    if alerts:
        print("\n⚠️ Alertas de possíveis fraudes encontrados:")
        for alert in alerts:
            print(f"- {alert}")
    else:
        print("\n✅ Nenhum alerta de fraude encontrado.")

if __name__ == "__main__":
    main()
