import multiprocessing as mp
import subprocess
import os
import sys


def movtomp3(filepath):
    fname = os.path.basename(filepath)
    print(f'begin: {fname}')
    dstname = os.path.splitext(filepath)[0] + '.mp3'
    
    rc = subprocess.run([
        'ffmpeg',
        '-i',
        filepath,
        '-loglevel',
        'fatal',
        '-y',
        dstname ]
    )
    if rc.returncode != 0:
        print(f'failed: {fname}')
    else:
        print(f'success: {fname}')

def main():
    paths = []
    print(sys.argv[1:])
    for arg in sys.argv[1:]:
        if os.path.isfile(arg):
            paths.append(os.path.abspath(arg))
    process_num = max(mp.cpu_count() // 8, 1)
    print(f'processes: {process_num} len:{len(paths)}')
    with mp.Pool(processes=process_num) as p:
        imap = p.imap_unordered(movtomp3, paths)
        result = list(imap) # TODO: research why this line mustn't remove

if __name__ == '__main__':
    main()