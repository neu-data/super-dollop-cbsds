"""Quarto pre-render step: copy the course materials into website/downloads/.

The website lives in website/, but the materials it offers for download live in the
repository root (slides/, workbook/, reference/, ...). Quarto can only publish files
inside its project folder, so this script copies them in before each render and builds
a participant pack (a zip without the instructor folder).
downloads/ is git-ignored; it is recreated on every render.
"""
import os
import shutil
import zipfile

SITE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SITE)
OUT = os.path.join(SITE, "downloads")

COPY = {
    "slides": ["Day1_Understanding_data_and_comparisons.pdf", "Day1_Understanding_data_and_comparisons.pptx",
               "Day2_Regression_and_data_science.pdf", "Day2_Regression_and_data_science.pptx"],
    "workbook": ["Participant_workbook.pdf", "Participant_workbook.docx",
                 "Final_exercise.pdf", "Final_exercise.docx"],
    "course": ["Course_overview_and_timetable.pdf", "Course_overview_and_timetable.docx"],
    "reference": ["cheat_sheet.pdf", "decision_diagrams.pdf", "method_selection_guide.pdf"],
    "data": ["hearts_raw.csv", "hearts.csv", "data_dictionary.csv"],
}

# Participant pack: everything needed to follow the course, without the instructor folder
PACK_NAME = "Concepts-of-Biostatistics-and-Data-Science"
PACK = ["Concepts-of-Biostatistics-and-Data-Science.Rproj", "R", "data",
        "workbook", "reference/cheat_sheet.pdf", "reference/decision_diagrams.pdf",
        "reference/method_selection_guide.pdf", "course/Course_overview_and_timetable.pdf"]
SKIP = {"__pycache__", ".Rproj.user"}


def main():
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    for folder, files in COPY.items():
        os.makedirs(os.path.join(OUT, folder), exist_ok=True)
        for f in files:
            shutil.copy2(os.path.join(ROOT, folder, f), os.path.join(OUT, folder, f))
    # Course figures used on the session pages
    shutil.copytree(os.path.join(ROOT, "figures"), os.path.join(OUT, "figures"))
    # Diagram images for the Resources page
    os.makedirs(os.path.join(OUT, "diagrams"), exist_ok=True)
    diag = os.path.join(ROOT, "reference", "diagrams")
    for f in sorted(os.listdir(diag)):
        if f.startswith("D") and f.endswith(".png"):
            shutil.copy2(os.path.join(diag, f), os.path.join(OUT, "diagrams", f))

    zpath = os.path.join(OUT, f"{PACK_NAME}-participant-pack.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for item in PACK:
            src = os.path.join(ROOT, item)
            if os.path.isfile(src):
                z.write(src, os.path.join(PACK_NAME, item))
                continue
            for dirpath, dirnames, filenames in os.walk(src):
                dirnames[:] = [d for d in dirnames if d not in SKIP]
                for fn in filenames:
                    full = os.path.join(dirpath, fn)
                    z.write(full, os.path.join(PACK_NAME, os.path.relpath(full, ROOT)))
    print(f"prepare_downloads: materials copied to {OUT}")


if __name__ == "__main__":
    main()
