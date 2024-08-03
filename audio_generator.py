import os
import argparse

# parser = argparse.ArgumentParser(description='Lektion nummer?')
# parser.add_argument("Lektion_Nummer", help="Lektion?")
# nummer = parser.parse_args().Lektion_Nummer 

def read_and_cluster(lesson_number, lines_per_group=20):
    filename = f"L{lesson_number}/L{lesson_number}_Sentence.txt"
    
    # Check if file exists
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    lines = [line.split('#')[0].strip() for line in lines]

    clusters = [''.join(lines[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]
    cluster_txt = [cluster.replace('.', '. \n') for cluster in clusters]
    cluster_audio = [cluster.replace('.', '. ') for cluster in clusters]

    for i, cluster in enumerate(cluster_txt):
        print(f"Group {i + 1}:")
        print(cluster)
        print("---")
        with open( f'Review/L{lesson_number}_{i+1}.txt', 'w', encoding='utf-8') as file:
                file.write(cluster)

    for i, cluster in enumerate(cluster_audio):

        command = f'tts --text "{cluster}" --model_name "tts_models/de/thorsten/vits" --out_path "Review/L{lesson_number}_{i+1}.wav"'
        os.system(command)
        print(f'---- \nL{lesson_number}_{i+1}.wav generated ! \n')

if __name__ == "__main__":
    number = int(input("Enter the lesson number: (e.g. 19) \n"))
    read_and_cluster(number)

