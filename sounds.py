import pygame as pg
from config import GameConfig
from input import Input
import wave

class Sounds:

    def init() -> None :
        Sounds.path : str = "assets/sounds"

        Sounds.__audios : dict[str, tuple(str, int)] = {
            "title": ("Track_6.wav", 1),
            "theme": ("night_theme_2.wav", 0),
            "victory": ("Fanfare_3.wav", 1),
            "failure": ("Game_Over_3.wav", 1),
            # "new_object": ("Fanfare_1.wav", 1),
            "jump" : ("jump_2.wav", 2),
            "button": ("button_pressed.wav", 2),
            "damage": ("damage.wav", 2)
            # "walk": ("walk_2.wav", 2),
            #"land": ("...", ...),
        }

        pg.mixer.init()

        for audio in Sounds.__audios:
            pg.mixer.music.load(Sounds.path + "/" + Sounds.__audios[audio][0])

        Sounds.audios_preparation()


    def audios_preparation():
        Sounds.play_audio("title", -1).pause()
        Sounds.play_audio("theme", -1).pause() # à changer plus tard pour mettre dans constructeur de world


    def play_audio(audio, loop: int = 0) -> pg.mixer.Channel:
        channel_id: int = Sounds.__audios[audio][1]
        pg.mixer.Channel(channel_id).play(pg.mixer.Sound(Sounds.path + "/" + Sounds.__audios[audio][0]), loop)
        pg.mixer.Channel(channel_id).set_volume(getattr(GameConfig.Volume,audio))
        return pg.mixer.Channel(channel_id)


    def stop_audio(audio):
        audio_channel = Sounds.__audios[audio][1]
        pg.mixer.Channel(audio_channel).stop()


    def pause_audio(audio):
        audio_channel = Sounds.__audios[audio][1]
        pg.mixer.Channel(audio_channel).pause()


    def unpause_audio(audio):
        audio_channel = Sounds.__audios[audio][1]
        pg.mixer.Channel(audio_channel).unpause()


    def from_title_to_theme():
        Sounds.pause_audio("title")
        Sounds.unpause_audio("theme")


    def from_theme_to_title():
        Sounds.pause_audio("theme")
        Sounds.unpause_audio("title")
