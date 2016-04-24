##### mp3 player
##### by Jansen Yan 3/23/16, library functions from pygame module mixer
__author__ = 'Jansen Yan'

from pygame import mixer

def credit():
    
    print("###################################################")
    print("###### Title: MP3 Program Author: Jansen Yan ######")
    print("###################################################\n")
    print("## Credits: PyGame Mixer Module provided most library functions ##")
    print("## Beta: 3/23/16 ##")
    
def import_queue(filename: str):
    # filename should be a .txt file
    infile = open(filename, 'r')
    content = infile.readlines()
    q = []
    for i in range(len(content)):
        content[i] = content[i].strip('\n')
        q.append(content[i])
    
    
def queue():
    q = []
    while True:
        filename = input("Please enter playlist item as filename, or enter C to end process: ")
        if filename == "C":
            break
        else:
            q.append(filename)
    return q

def get_filename():

    print("##########################")
    print("Welcome to the mp3 Program")
    print("##########################\n")
    
    filename = input("Please enter name of the file, enter P to create playlist, or enter C to quit: ")
    if 'C' == filename:
        return filename
    if 'P' == filename:
        return queue()
    else:
        assert ".mp3" in filename[-4:]
        return filename
    
def how_many_times():
    
    print("## entering -1 will loop the song infinitely ##")
    number_of_times = int(input("How many times would you like to repeat each song? "))
    return number_of_times

def load_and_play(filename: str, number_of_times = 0):
    try:
        mixer.music.load(filename)
        mixer.music.play(number_of_times)
    except :
        print("File could not be opened")
    
def menu():
    
    if mixer.music.get_busy():
        print("#####################################")
        print("###### Your song is playing!!! ######")
        print("#####################################\n")
        
        print("#####################################")        
        print("Enter 2 to stop the music")
        print("Enter 3 to pause, 33 to unpause")
        print("Enter 5 to raise volume")
        print("Enter 4 to lower volume")
        print("Enter 6 to rewind from the beginning")
        print("If you are in a playlist, press enter in the commands")
        print("######################################\n")

        while mixer.music.get_busy():
            command = input("Please enter any commands: ")
            if command == "5" or command == "4":
                change_volume(command)
            if command == "3" or command == "33":
                change_play(command)
            if command == "2":
                mixer.music.stop()
                break
            if command == "6":
                mixer.music.rewind()
            if command == "":
                break

    else:
        print('''Your song is not playing for one of three reasons:
                #1 filename was not found
                #2 filetype is not supported
                #3 pygame mixer glitch
                -- in any case, please try again
                ''')
            

def change_play(cmd: str):
    if cmd == "3":
        mixer.music.pause()
    if cmd == "33":
        mixer.music.unpause()

def change_volume(cmd: str):
    increment = .1
    volume = mixer.music.get_volume()
    if 0 <= volume <= 1:
        if cmd == '5':
            volume += increment
            if volume == 1:
                print("You are at max volume")
        elif cmd == '4':
            volume -= increment
            if volume == 0:
                print("You are at min volume")
    return mixer.music.set_volume(volume)

def main():
    mixer.init()
    while True:
        filename = get_filename()
        if filename == 'C':
            break
        else:
            number_of_times = how_many_times()
            if type(filename) == list:
                playlist = filename
                for item in playlist:
                    load_and_play(item, number_of_times)
                    menu()

                    
                                      
            else:
                load_and_play(filename, number_of_times)
                menu()
            

        
    

if __name__ == "__main__":
    credit()
    main()
