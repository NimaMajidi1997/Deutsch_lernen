import os
import argparse
from PIL import Image, ImageDraw, ImageFont

# parser = argparse.ArgumentParser(description='Lektion nummer?')
# parser.add_argument("Lektion_Nummer", help="Lektion?")
# nummer = parser.parse_args().Lektion_Nummer 

def create_flashcard(front, filename):
    # Create a larger blank image with white background
    img = Image.new('RGB', (1550, 600), color=(255, 255, 255))  # Increased resolution
    d = ImageDraw.Draw(img)
    
    # Load a TTF font with a larger size
    try:
        #fnt = ImageFont.truetype("arial.ttf", 30)  # for windows
        fnt = ImageFont.truetype("DejaVuSerif.ttf", 25) # for wsl/Ubuntu
    except IOError:
        fnt = ImageFont.load_default()
        print('Default font used!')

    d.text((30, 20), front, font=fnt, fill=(0, 0, 0))
    img.save(filename)

def num_sentences():
    total_number = []
    with open('L19/L19_Sentence.txt', 'r') as file:
        total_number.append(len(file.readlines()))
    with open('L20/L20_Sentence.txt', 'r') as file:
        total_number.append(len(file.readlines()))
    return total_number

def read_and_cluster(lesson_number, lines_per_group=20):
    filename = f"L{lesson_number}/L{lesson_number}_Sentence.txt"
    
    # Check if file exists
    if not os.path.isfile(filename):
        print(f"File {filename} does not exist.")
        return

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    sentences_number = num_sentences()
    if lesson_number == 19:
        j = 1
    elif lesson_number == 20:
        j = sentences_number[0]+1

    lines_txt = [f'{j+i}: ' + line for i, line in enumerate(lines)]
    lines_txt = [line.split('#')[0].strip() for line in lines_txt]
    clusters_txt = [''.join(lines_txt[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]
    cluster_txt = [cluster.replace('.', '. \n') for cluster in clusters_txt]

    lines = [line.split('#')[0].strip() for line in lines]
    clusters = [''.join(lines[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]
    cluster_audio = [cluster.replace('.', '. ') for cluster in clusters]

    for i, cluster in enumerate(cluster_txt):
        print(f"Group {i + 1}:")
        print(cluster)
        create_flashcard(cluster, f'Flashcards/L{lesson_number}_{i+1}.png')
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
    
