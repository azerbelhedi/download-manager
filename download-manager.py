#!/bin/sh

import os
from pathlib import Path
import PyPDF2
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import shutil
import sys

from config import target_folders, classification_threshold, source_path, archive_target_folder, pictures_target_folder


def setup():
    for folder in target_folders:
        folder_path = folder["path"]
        print(f"path:  {folder_path}\t {os.path.exists(folder_path)}")
        if not os.path.exists(folder_path):
            path = Path(folder_path)
            path.mkdir(parents=True, exist_ok=True)


def pdf_to_array(pdf_path):
    text_array = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pages = pdf_reader.pages

        for page in pages:
            text = page.extract_text()
            text_array.extend(text.split())

    return text_array


def top_occurrences(array, top_start, top_end, min_len):
    array = [item for item in array if len(item) >= min_len]
    word_counts = Counter(array)
    top_words = word_counts.most_common(top_end)
    return top_words[top_start-1:]


def save_words_to_file(words, file_path):
    with open(file_path, "w") as file:
        for word in words:
            file.write(word + "\n")        


def populate(source_pdf_file, target_text_file):
    words = pdf_to_array(source_pdf_file)
    # print(f"total words: {len(words)}")
    top_words_with_freq= top_occurrences(words, 1, 100, 5)
    # print(f"top words: {top_words_with_freq}")
    top_words = [word[0] for word in top_words_with_freq]
    save_words_to_file(top_words, target_text_file)
    

def populate_all_target_folders():
    for target in target_folders:
        populate(target["row_data"], target["keywords"])


def calculate_similarity(string1, string2):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([string1, string2])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    return similarity

 
def classify_by_keyword(file_path, targets_with_keywords):
    classes_from_targets = []
    similarities = []
    
    for target in targets_with_keywords:
        keywords_array = []
        with open(target, "r") as file:
            for line in file:
                keywords_array.append(line.strip())
        classes_from_targets.append(" ".join(keywords_array))
    
    # print(classes_from_targets)
    
    source_keywords_array = pdf_to_array(file_path)
    source_keywords_string = "".join(source_keywords_array)
    
    for class_string in classes_from_targets:
        similarity = calculate_similarity(class_string, source_keywords_string)
        similarities.append(similarity)
        
    # print(f"similarities: {similarities}")
    
    best_index = np.array(similarities).argmax()
    if similarities[best_index] >= classification_threshold:
        return targets_with_keywords[best_index], similarities, best_index
    else:
        return None, similarities, None


def get_all_files(path):
    files = []
    for entry in os.listdir(path):
        full_path = os.path.join(path, entry)
        if not os.path.isdir(full_path):
            files.append(full_path)
    
    return files


def move_file(source_path, target_path):
    shutil.move(source_path, target_path)


def arrange_pdf(path):
    targets_keyword = [target["keywords"] for target in target_folders if target["keywords"] != ""]
    targets_path = [target["path"] for target in target_folders if target["keywords"] != ""]
    target, similarities, index = classify_by_keyword(path, targets_keyword)
    print(f"similarities: {similarities}, index: {index}")
    
    if index is not None:
        print(f"[1] will move {path} to {targets_path[index]}\n")
        move_file(path, targets_path[index])
    else:
        print(f"[0] can't move {path}\n")


def arrange_archive(path):
    move_file(path, archive_target_folder)
    print(f"[1] will move {path} to {archive_target_folder}\n")


def arrange_picture(path):
    move_file(path, pictures_target_folder)
    print(f"[1] will move {path} to {pictures_target_folder}\n")


def arrangeFiles(path):
    source_files = get_all_files(path)
    for file in source_files:
        format = Path(file).suffix        
        if format == ".pdf" : arrange_pdf(file)
        if format in [".tar", ".zip", ".xz"]: arrange_archive(file)
        if format in [".svg", ".png", ".jpeg"]: arrange_picture(file)
        

def cli(arguments):
    if len(arguments) <= 1:
        print("download-manager: too few arguemnts")
        return None
    command = arguments[1]
    
    if command == "setup": setup()
    elif command == "populate": populate_all_target_folders()
    elif command == "run": arrangeFiles(source_path)
    else: print(f"download-manager: command '{command}' is unknown")


def main():
    cli(sys.argv)
    
    
main()
