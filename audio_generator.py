import os
import argparse

# parser = argparse.ArgumentParser(description='Lektion nummer?')
# parser.add_argument("Lektion_Nummer", help="Lektion?")
# nummer = parser.parse_args().Lektion_Nummer 

def read_and_cluster(file_number, lines_per_group=20):
    filename = f"L{file_number}_Sentence.txt"
    
    # Check if file exists
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    lines = [line.replace('\n', '') for line in lines]

    # Cluster lines
    clusters = [lines[i:i + lines_per_group] for i in range(0, len(lines), lines_per_group)]

    clusters = [''.join(lines[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]

    # Print clusters (or you can process them as needed)
    for i, cluster in enumerate(clusters):
        print(f"Group {i + 1}:")
        print(cluster)
        print("\n---\n")
        command = f'tts --text "{cluster}" --model_name "tts_models/de/thorsten/vits" --out_path "Group_{i+1}.wav"'
        os.system(command)

if __name__ == "__main__":
    number = int(input("Enter the lesson number: (e.g. 19) "))
    read_and_cluster(number)

