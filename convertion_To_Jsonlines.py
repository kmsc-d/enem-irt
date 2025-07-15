import json
import os

# Configurações
input_path = "C:/Users/Kelvin/Desktop/Teste/dados/file.txt"
output_dir = "output_separado_2"
os.makedirs(output_dir, exist_ok=True)

# Arquivos de saída
output_paths = {
    "MT": os.path.join(output_dir, "1 - respostas_MT.jsonl"),
    "CN": os.path.join(output_dir, "2 - respostas_CN.jsonl"),
    "CH": os.path.join(output_dir, "3 - respostas_CH.jsonl"),
    "LC": os.path.join(output_dir, "4 - respostas_LC.jsonl"),
    "ES": os.path.join(output_dir, "5 - respostas_ES.jsonl"),
    "IN": os.path.join(output_dir, "6 - respostas_IN.jsonl")
}

# ---- Funções de Processamento ----


def processar_materias_principais(respostas, subject_id):
    """Processa MT, CN, CH, LC (itens 0-169)"""
    areas = {
        "MT": (0, 45),
        "CN": (45, 90),
        "CH": (90, 135),
        "LC": (135, 170)
    }

    for area, (start, end) in areas.items():
        respostas_area = {
            str(i): int(float(respostas[i]))
            for i in range(start, end)
            if i < len(respostas) and respostas[i] in ["0", "1"]
        }
        if respostas_area:
            with open(output_paths[area], 'a') as f_out:
                json.dump({"subject_id": str(subject_id),
                          "responses": respostas_area}, f_out)
                f_out.write('\n')


def processar_linguas(respostas, subject_id):
    """
    Processa os últimos 10 itens (170-179) de um aluno:
    - Se o item 170 for "0" ou "1", salva itens [0] a [4] (170-174) em ES
    - Se o item 170 for "NaN", salva itens [5] a [9] (175-179) em IN
    """
    # Pega os últimos 10 itens (170-179)
    ultimos_10 = respostas[-10:] if len(respostas) >= 10 else []

    item_170 = ultimos_10[0]

    if item_170 in ["0", "1"]:
        # Salva ES (itens 170-174 = índices 0 a 4 nos últimos 10)
        es_respostas = {
            str(i+170): int(ultimos_10[i])
            for i in range(5)
            if ultimos_10[i] in ["0", "1"]
        }

        if es_respostas:
            with open(output_paths['ES'], 'a') as f:
                json.dump({
                    "subject_id": str(subject_id),
                    "responses": es_respostas
                }, f)
                f.write('\n')

    else:
        # Salva IN (itens 175-179 = índices 5 a 9 nos últimos 10)
        in_respostas = {
            str(i + 170): int(ultimos_10[i])
            for i in range(5, 10)
            if ultimos_10[i] in ["0", "1"]
        }

        if in_respostas:
            with open(output_paths['IN'], 'a') as f:
                json.dump({
                    "subject_id": str(subject_id),
                    "responses": in_respostas
                }, f)
                f.write('\n')


def main():
    # limpar_arquivos_anteriores()
    # mostrar_item_170(input_path)

    with open(input_path, 'r') as f_in:
        for subject_id, line in enumerate(f_in):
            respostas = line.strip().split()
            processar_materias_principais(respostas, subject_id)
            processar_linguas(respostas, subject_id)

    print(f"Processamento concluído! Arquivos salvos em: {output_dir}")
    print("Arquivos gerados:")
    for area, path in output_paths.items():
        print(f"- {area}: {path}")


if __name__ == "__main__":
    main()
