import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import glob

# parser = argparse.ArgumentParser(description='Lektion nummer?')
# parser.add_argument("Lektion_Nummer", help="Lektion?")
# nummer = parser.parse_args().Lektion_Nummer 

latex_sample = """
\documentclass[
    fontsize=16pt,        
    paper=a4,              
    parskip=half 
]§article
\\usepackage§Package1
\\usepackage§Package2
\\begin§document  \SixteenStarLight Your are improving ... \SixteenStarLight  \\\\ \SixteenStarLight  \SixteenStarLight \SixteenStarLight \SixteenStarLight \SixteenStarLight  \SixteenStarLight \SixteenStarLight \SixteenStarLight \SixteenStarLight  \SixteenStarLight \SixteenStarLight \SixteenStarLight
\section§Deutsch {sentences_de} \\newpage
\section§Englisch {sentences_eng}
\end§document"""

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
    with open('L21/L21_Sentence.txt', 'r') as file:
        total_number.append(len(file.readlines()))   
    return total_number


def delete_unnecessary():
        log_files = glob.glob("Review/*.log")
        aux_files = glob.glob("Review/*.aux")
        tex_files = glob.glob("Review/*.tex")
        files_to_delete = log_files + aux_files + tex_files
        # Delete each file
        for file in files_to_delete:
            os.remove(file)
            print(f"Deleted: {file}")


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
    elif lesson_number == 21:
        j = sentences_number[0]+sentences_number[1]+1
        
    #lines_txt = [f'{j+i}: ' + line for i, line in enumerate(lines)] # add number for each sentence

    lines_txt_eng = [line.split('#')[1] for line in lines] # separate Deutsch and English
    lines_txt_eng = [f'{j+i}: ' + line for i, line in enumerate(lines_txt_eng)] # add number for each sentence
    lines_txt_de = [line.split('#')[0].strip() for line in lines]
    lines_txt_de = [f'{j+i}: ' + line for i, line in enumerate(lines_txt_de)] # add number for each sentence

    clusters_txt_eng = [''.join(lines_txt_eng[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]
    clusters_txt_de = [''.join(lines_txt_de[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]


    clusters_txt_eng = [cluster.replace('(', '') for cluster in clusters_txt_eng]
    clusters_txt_eng = [cluster.replace(')', '') for cluster in clusters_txt_eng]
    clusters_txt_eng = [cluster.replace('\n', '\\\\') for cluster in clusters_txt_eng]
    print(clusters_txt_eng)

    clusters_txt_de = [cluster.replace('.', '. \\\\') for cluster in clusters_txt_de]
    print(clusters_txt_de)


    lines = [line.split('#')[0].strip() for line in lines]
    clusters = [''.join(lines[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]
    cluster_audio = [cluster.replace('.', '. ') for cluster in clusters]

    for i, cluster in enumerate(clusters_txt_de):
        print(f"Group {i + 1}:")
        #print(cluster)
        latex = latex_sample.format(sentences_de=cluster,sentences_eng=clusters_txt_eng[i] )
        latex = latex.replace('§article', '{scrartcl}')
        latex = latex.replace('§Deutsch', '{\dsliterary Deutsch\dsliterary}')
        latex = latex.replace('§Englisch', '{\dsliterary Englisch\dsliterary}')
        latex = latex.replace('§document', '{document}')
        latex = latex.replace('§Package1', '{dictsym}')
        latex = latex.replace('§Package2', '{bbding}')
        #latex = latex.replace('§verticalSpace', '{1cm}') \hspace§verticalSpace 
         
        print(latex)
        with open('Review/main.tex', 'w', encoding='utf-8') as file:
            file.write(latex)
        command_tex = f'pdflatex -jobname=Review/L{lesson_number}_{i+1} Review/main.tex'
        os.system(command_tex)
        

        create_flashcard(cluster, f'Flashcards/L{lesson_number}_{i+1}.png')

    for i, cluster in enumerate(cluster_audio):
        command = f'tts --text "{cluster}" --model_name "tts_models/de/thorsten/vits" --out_path "Review/L{lesson_number}_{i+1}.wav"'
        os.system(command)
        print(f'---- \nL{lesson_number}_{i+1}.wav generated ! \n')



if __name__ == "__main__":
    number = int(input("Enter the lesson number: (e.g. 19) \n"))
    read_and_cluster(number, lines_per_group=20)
    delete_unnecessary()
