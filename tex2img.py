from PIL import Image
import win32clipboard
import io
import subprocess
import sys
import os

TEX_HEADER = r"""
\documentclass{article}
\usepackage[active,tightpage]{preview}
\setlength{\parindent}{0pt}
\pagestyle{empty}
\begin{document}
\begin{preview}
"""

TEX_END =r"""
\end{preview}
\end{document}
"""

def png2clipboard(pngFileName):
  img = Image.open(pngFileName)
  img = img.convert("RGB")

  stream = io.BytesIO()
  img.save(stream, format="DIB")
  dib_data = stream.getvalue()
  
  if os.name == 'nt':  # Windows
    win32clipboard.OpenClipboard()
    try:
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(win32clipboard.CF_DIB, dib_data)
    finally:
        win32clipboard.CloseClipboard()
  else:
    raise NotImplementedError("Platform not supported")

  return

def tex2img(fileName, texContents, clipboard, saveImage):
  texFullContents = TEX_HEADER + texContents + TEX_END
  texFileName = fileName + ".tex"
  dviFileName = fileName + ".dvi"
  logFileName = fileName + ".aux"
  auxFileName = fileName + ".log"
  pngFileName = fileName + ".png"

  filesToRemove = [texFileName, dviFileName, auxFileName, logFileName]
  with open(fileName + ".tex", "x") as texFile:
    texFile.write(texFullContents)

  try:
    subprocess.run(["latex", "-quiet", texFileName], check=True, stderr = subprocess.STDOUT)
    subprocess.run(["dvipng", "-q", "-T", "tight", "-D", "600", 
                    "-o", pngFileName, dviFileName], check=True, stdout = subprocess.DEVNULL)

  except subprocess.CalledProcessError as e:
    print(f"Error: {e}")
    for file in filesToRemove:
      if os.path.exists(file):
        os.remove(file)

    sys.exit(1) 
  
  for file in filesToRemove:
    if os.path.exists(file):
      os.remove(file)
  
  if (clipboard):
    png2clipboard(pngFileName)
  
  if (not saveImage):
    os.remove(pngFileName)

  return

if __name__ == '__main__':
  printUsage = False
  clipboard = False
  saveImage = False
  texContents = None 
  fileName = "temp"

  argc = len(sys.argv)
  
  if (argc < 3):
    print("Error: Not enough arguments passed")
    print("Usage: tex2img.py [-h] [-c] [-s filename] [tex code]")
    sys.exit(1)
  
  argv = sys.argv[1:]

  i = 0
  while (i < argc - 1):
    if (argv[i] in ['-h', '-help', '--help', '/?']):
      printUsage = True
      break
    
    elif (argv[i] == '-c'):
      clipboard = True
    
    elif (argv[i] == '-s'):
      if (i + 1 < argc - 1):
        saveImage = True
        fileName = argv[i + 1]
        i += 1
      else:
        print("Error: -s requires a name for the file")
        printUsage = True
        i += 1
        break
    i += 1

  texContents = argv[i - 1]

  if (printUsage or (not clipboard and not saveImage) or 
      texContents == None or fileName == None):
    print("Usage: tex2img.py [-h] [-c] [-s filename] [tex code]")
    sys.exit(1)

  tex2img(fileName, texContents, clipboard, saveImage)

