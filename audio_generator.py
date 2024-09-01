import os
import argparse
from PIL import Image, ImageDraw, ImageFont
import glob
import hashlib
import PyPDF2

# parser = argparse.ArgumentParser(description='Lektion nummer?')
# parser.add_argument("Lektion_Nummer", help="Lektion?")
# nummer = parser.parse_args().Lektion_Nummer 

def gen_tex_file(sentences_de, sentences_eng):
    latex = r"""
        \documentclass[
        fontsize=15pt,
        parskip=half
    ]{scrartcl}

        \usepackage[utf8]{inputenc}
        \usepackage{hyperref}
        \usepackage{dictsym}
        \usepackage{bbding}
        \usepackage{hieroglf}
         
        \usepackage[a4paper, top=0.5in, bottom=0.25in, left=0.5in, right=0.5in]{geometry} % Adjust the margins here

        \begin{document}
        \SixteenStarLight \SnowflakeChevron \SnowflakeChevronBold 
        \SnowflakeChevron \SnowflakeChevronBold  \SnowflakeChevron 
        \SnowflakeChevron \SnowflakeChevronBold \SnowflakeChevron  
        \SixteenStarLight  \\ 
        \SunshineOpenCircled \hspace{0.2cm}  Remember ... \\ 
        \SunshineOpenCircled \hspace{0.2cm}  Your are improving! \\ 
        \SixteenStarLight \SnowflakeChevron \SnowflakeChevronBold 
        \SnowflakeChevron \SnowflakeChevronBold  \SnowflakeChevron 
        \SnowflakeChevron \SnowflakeChevronBold \SnowflakeChevron  \SixteenStarLight 

        \section{\dsliterary \hspace{0.2cm}  Deutsch \hspace{0.2cm} \dsliterary} 
        """ + sentences_de + r"""
        \footnote{© 2024 \href{https://github.com/NimaMajidi1997/Deutsch_lernen}{https://github.com/NimaMajidi1997/Deutsch\_lernen} . All rights reserved.}
        \newpage
        \section{\dsliterary \hspace{0.2cm} Englisch \hspace{0.2cm} \dsliterary} 
        """ + sentences_eng + r"""
        \footnote{© 2024 \href{https://github.com/NimaMajidi1997/Deutsch_lernen}{https://github.com/NimaMajidi1997/Deutsch\_lernen} . All rights reserved.}

        \end{document}
        """
    return latex

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
    with open('L22/L22_Sentence.txt', 'r') as file:
        total_number.append(len(file.readlines()))     
    return total_number

def delete_unnecessary():
        log_files = glob.glob("Review/*.log")
        aux_files = glob.glob("Review/*.aux")
        tex_files = glob.glob("Review/*.tex")
        out_files = glob.glob("Review/*.out")
        files_to_delete = log_files + aux_files + tex_files+ out_files
        # Delete each file
        for file in files_to_delete:
            os.remove(file)
            print(f"Deleted: {file}")

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def compare_pdfs(new_file, old_file):
    text1 = extract_text_from_pdf(new_file)
    text2 = extract_text_from_pdf(old_file)
    
    if text1 == text2:
        print(f"{old_file} are identical in content.")
        os.remove(new_file)
        return True
    else:
        return False
    
def read_and_cluster(lesson_number, audio_gen, lines_per_group=20):
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
    elif lesson_number == 22:
        j = sentences_number[0]+sentences_number[1]+sentences_number[2]+1

    lines_txt_eng = [line.split('#')[1] for line in lines] # separate Deutsch and English
    lines_txt_eng = [f'{j+i}: ' + line for i, line in enumerate(lines_txt_eng)] # add number for each sentence
    lines_txt_de = [line.split('#')[0].strip() for line in lines]
    lines_txt_de = [f'{j+i}: ' + line for i, line in enumerate(lines_txt_de)] # add number for each sentence

    clusters_txt_eng = [''.join(lines_txt_eng[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]
    clusters_txt_de = [''.join(lines_txt_de[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]

    clusters_txt_eng = [cluster.replace('(', '') for cluster in clusters_txt_eng]
    clusters_txt_eng = [cluster.replace(')', '') for cluster in clusters_txt_eng]
    clusters_txt_eng = [cluster.replace('\n', '\\\\') for cluster in clusters_txt_eng]
    #print(clusters_txt_eng)
    clusters_txt_flash = [cluster.replace('.', '. \n') for cluster in clusters_txt_de]
    clusters_txt_de = [cluster.replace('.', '. \\\\') for cluster in clusters_txt_de]
    #print(clusters_txt_de)

    lines = [line.split('#')[0].strip() for line in lines]
    clusters = [''.join(lines[i:i + lines_per_group]) for i in range(0, len(lines), lines_per_group)]
    cluster_audio = [cluster.replace('.', '. ') for cluster in clusters]

    for i, cluster in enumerate(clusters_txt_de):
        print(f"Group {i + 1}:")
        #print(cluster)
        latex = gen_tex_file(sentences_de=cluster, sentences_eng=clusters_txt_eng[i])
        #print(latex)
        with open('Review/main.tex', 'w', encoding='utf-8') as file:
            file.write(latex)
        #command_tex = f'pdflatex -jobname=Review/L{lesson_number}_{i+1} Review/main.tex'
        command_tex = f'pdflatex -jobname=Review/temp Review/main.tex'
        os.system(command_tex)

        if os.path.exists(f'Review/L{lesson_number}_{i+1}.pdf'):
            
            identical = compare_pdfs('Review/temp.pdf', f'Review/L{lesson_number}_{i+1}.pdf')

            if identical == False:
                os.rename('Review/temp.pdf', f'Review/L{lesson_number}_{i+1}.pdf')
                print('renamed the gile')

        create_flashcard(clusters_txt_flash[i], f'Flashcards/L{lesson_number}_{i+1}.png')

    if audio_gen == 'yes':
        for i, cluster in enumerate(cluster_audio):
            command = f'tts --text "{cluster}" --model_name "tts_models/de/thorsten/vits" --out_path "Review/L{lesson_number}_{i+1}.wav"'
            os.system(command)
            print(f'---- \nL{lesson_number}_{i+1}.wav generated ! \n')

if __name__ == "__main__":
    number = int(input("Enter the lesson number: (e.g. 19) \n"))
    audio_gen = str(input("Do you want audio generation? (yes or no) \n"))
    read_and_cluster(number, audio_gen, lines_per_group=20)
    delete_unnecessary()
