import serial
import RPi.GPIO as GPIO
import time
import pygame


#Spilleliste Workout 1
workout1nivaa1 = ["lydfiler/211Rygghev.mp3","lydfiler/212Rygghev.mp3","lydfiler/221Baten.mp3", "lydfiler/222Baten.mp3", "lydfiler/231Utfall.mp3", "lydfiler/232Utfall.mp3", "lydfiler/241Planken.mp3", "lydfiler/242Planken.mp3", "lydfiler/251Sideplanke.mp3", "lydfiler/252Sideplanke.mp3", "lydfiler/253Sideplanke2.mp3", "lydfiler/261Kneboy.mp3", "lydfiler/262Kneboy.mp3", "lydfiler/271Benhev.mp3", "lydfiler/272Benhev.mp3", "lydfiler/281Pushups.mp3", "lydfiler/282Pushups.mp3" ]
workout1nivaa2 = ["lydfiler/111pushups.mp3","lydfiler/112pushups.mp3", "lydfiler/121Kneboy.mp3", "lydfiler/122Kneboy.mp3", "lydfiler/131Planken.mp3", "lydfiler/132Planken.mp3", "lydfiler/141Supermann.mp3", "lydfiler/142Supermann.mp3", "lydfiler/151Benhev.mp3", "lydfiler/152Benhev.mp3", "lydfiler/161Russian twist.mp3", "lydfiler/162Russian twist.mp3", "lydfiler/171Utfall.mp3", "lydfiler/172Utfall.mp3", "lydfiler/181kne.mp3", "lydfiler/182kne.mp3", "lydfiler/191Sideplanke.mp3", "lydfiler/192Sideplanke.mp3", "lydfiler/1101Sideplanke.mp3", "lydfiler/1102Sideplanke.mp3", "lydfiler/1111baten.mp3", "lydfiler/1112baten.mp3"]



# Spilleliste Workout 2
workout2nivaa1 = ["lydfiler/111pushups.mp3","lydfiler/112pushups.mp3", "lydfiler/121Kneboy.mp3", "lydfiler/122Kneboy.mp3", "lydfiler/131Planken.mp3", "lydfiler/132Planken.mp3", "lydfiler/141Supermann.mp3", "lydfiler/142Supermann.mp3", "lydfiler/151Benhev.mp3", "lydfiler/152Benhev.mp3", "lydfiler/161Russian twist.mp3", "lydfiler/162Russian twist.mp3", "lydfiler/171Utfall.mp3", "lydfiler/172Utfall.mp3", "lydfiler/181kne.mp3", "lydfiler/182kne.mp3", "lydfiler/191Sideplanke.mp3", "lydfiler/192Sideplanke.mp3", "lydfiler/1101Sideplanke.mp3", "lydfiler/1102Sideplanke.mp3", "lydfiler/1111baten.mp3", "lydfiler/1112baten.mp3"]
workout2nivaa2 = ["lydfiler/211Rygghev.mp3","lydfiler/212Rygghev.mp3","lydfiler/221Baten.mp3", "lydfiler/222Baten.mp3", "lydfiler/231Utfall.mp3", "lydfiler/232Utfall.mp3", "lydfiler/241Planken.mp3", "lydfiler/242Planken.mp3", "lydfiler/251Sideplanke.mp3", "lydfiler/252Sideplanke.mp3", "lydfiler/253Sideplanke2.mp3", "lydfiler/261Kneboy.mp3", "lydfiler/262Kneboy.mp3", "lydfiler/271Benhev.mp3", "lydfiler/272Benhev.mp3", "lydfiler/281Pushups.mp3", "lydfiler/282Pushups.mp3" ]
workout2nivaa3 = []

#setter opp serial
ser = serial.Serial("/dev/ttyACM0", 115200, timeout=1)
ser.baudrate = 115200

#lager en event som gjør at neste lydspor spilles av automatisk
NEXT = pygame.USEREVENT+1

# holder styr på spillelisten og lydfil som avspilles
currentplaylist = []
currenttrack = 0

def main():
    #initierer pygame
    pygame.init()
    pygame.mixer.init(frequency = 48000)

    while True:
        print("loop")
        read_ser = ser.readline()
        #kaller på metoden som spiller av neste lydfil
        handlePygameEvents()

        #leser meldingener som kommer via serial
        message = read_ser.decode("ASCII")
        if message != "":
            parts = message.strip().split(" ")
            message = ""
            print(parts)

            commando = parts[0]
            workout = parts[1]
            level = parts[2]
            #kaller på funksjonene som tolker meldingen
            commandfraArduino(commando, workout, level)

# funksjonen kaller på en relevant funksjon basert meldingen
def commandfraArduino(commando, workout, level):
    if (commando == "PLAY"):
        playWorkout(commando, workout, level)
    if (commando == "PAUSE"):
        pause()
    if (commando == "RESUME"):
        resume()
    if (commando == "NEXT"):
        playNext()
    if (commando == "PREV"):
        playPrev()



#funksjonen velger ut riktig spilleliste

def playWorkout(commando, workout, level):
    global currentplaylist
    global currenttrack

    if (workout == "1"):
        if (level == "1"):
            currentplaylist = workout1nivaa1
        if (level == "2"):
            currentplaylist = workout1nivaa2
        if (level == "3"):
            currentplaylist = workout1nivaa3

    if (workout == "2"):
        if (level == "1"):
            currentplaylist = workout2nivaa1
        if (level == "2"):
            currentplaylist = workou21nivaa2
        if (level == "3"):
            currentplaylist = workou21nivaa3

    currenttrack = 0
    spillWorkout()

#funksjonen spiller av liste

def spillWorkout():
    if len(currentplaylist) > 0 and  currenttrack < len(currentplaylist):
        pygame.mixer.music.load(currentplaylist[currenttrack])
        pygame.mixer.music.play()
        if playlistNotEmpty():
            pygame.mixer.music.set_endevent(NEXT)

# sjekker om listen er tom
def playlistNotEmpty():
    return currenttrack < len(currentplaylist)-1
#sjekker om lydfilen er starten på spilleliste
def notFirstTrack():
    return len(currentplaylist) - currenttrack <= len(currentplaylist)

#funksjonen spiller av neste lydfil automatisk
def handlePygameEvents():
    global currenttrack
    for event in pygame.event.get():
        if event.type == NEXT:
            print("Pygame event: NEXT")
            currenttrack = (currenttrack + 1)
            spillWorkout()

#funksjonen spiller av neste lydfil dersom bruker hopper frem i spillelisten
def playNext():
    global currenttrack
    if playlistNotEmpty():
        currenttrack = (currenttrack + 1)
        spillWorkout()
#funksjonen spiller av forrige lydfil dersom bruker hopper tilbake i spillelisten
def playPrev():
    global currenttrack
    if notFirstTrack():
        currenttrack = (currenttrack - 1)
        spillWorkout()
#funksjonen pauser avspilling
def pause():
    #if pygame.mixer.music.get_busy():
        pygame.mixer.music.pause()
        print("paused")
#funskjonen resumer avspilling
def resume():
    pygame.mixer.music.unpause()
    print("resume")



main()
GPIO.cleanup()