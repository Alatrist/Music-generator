from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
from enum import Enum
from collections import defaultdict
import numpy as np


note_seq = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']


# See https://en.wikipedia.org/wiki/General_MIDI#Program_change_events
class Instrument(Enum):
    """Enumeration of all instruments available in MIDI"""
    # Piano
    PIANO_ACOUSTIC_GRAND = 0
    PIANO_ACOUSTIC_BRIGHT = 1
    PIANO_ELECTRIC_GRAND = 2
    PIANO_HONKY_TONK = 3
    PIANO_ELECTRIC_1 = 4
    PIANO_ELECTRIC_2 = 5
    HARPSICHORD = 6
    CLAVINET = 7
    # Chromatic Percussion
    CELESTA = 8
    GLOCKENSPIEL = 9
    MUSIC_BOX = 10
    VIBRAPHONE = 11
    MARIMBA = 12
    XYLOPHONE = 13
    TUBULAR_BELLS = 14
    DULCIMER = 15
    # Organ
    ORGAN_DRAWBAR = 16
    ORGAN_PERCUSSIVE = 17
    ORGAN_ROCK = 18
    ORGAN_CHURCH = 19
    ORGAN_REED = 20
    ACCORDION = 21
    HARMONICA = 22
    ACCORDION_TANGO = 23
    # Guitar
    GUITAR_ACOUSTIC_NYLON = 24
    GUITAR_ACOUSTIC_STEEL = 25
    GUITAR_ELECTRIC_JAZZ = 26
    GUITAR_ELECTRIC_CLEAN = 27
    GUITAR_ELECTRIC_MUTED = 28
    GUITAR_ELECTRIC_OVERDRIVEN = 29
    GUITAR_ELECTRIC_DISTORTED = 30
    GUITAR_HARMONICS = 31
    # Bass
    BASS_ACOUSTIC = 32
    BASS_ELECTRIC_FINGER = 33
    BASS_ELECTRIC_PICK = 34
    BASS_FRETLESS = 35
    BASS_SLAP_1 = 36
    BASS_SLAP_2 = 37
    BASS_SYNTH_1 = 38
    BASS_SYNTH_2 = 39
    # Strings
    VIOLIN = 40
    VIOLA = 41
    CELLO = 42
    CONTRABASS = 43
    STRINGS_TREMOLO = 44
    STRINGS_PIZZICATO = 45
    HARP_ORCHESTRAL = 46
    TIMPANI = 47
    # Ensemble
    STRINGS_ENSEMBLE_1 = 48
    STRINGS_ENSEMBLE_2 = 49
    STRINGS_SYNTH_1 = 50
    STRINGS_SYNTH_2 = 51
    CHOIR_AAHS = 52
    CHOIR_OOHS = 53
    CHOIR_SYNTH = 54
    ORCHESTRA_HIT = 55
    # Brass
    TRUMPET = 56
    TROMBONE = 57
    TUBA = 58
    TRUMPET_MUTED = 59
    FRENCH_HORN = 60
    BRASS_SECTION = 61
    BRASS_SYNTH_1 = 62
    BRASS_SYNTH_2 = 63
    # Reed
    SAX_SOPRANO = 64
    SAX_ALTO = 65
    SAX_TENOR = 66
    SAX_BARITONE = 67
    OBOE = 68
    ENGLISH_HORN = 69
    BASSOON = 70
    CLARINET = 71
    # Pipe
    PICCOLO = 72
    FLUTE = 73
    RECORDER = 74
    PAN_FLUTE = 75
    BLOWN_BOTTLE = 76
    SHAKUHACHI = 77
    WHISTLE = 78
    OCARINA = 79
    # Synth Lead
    SYNTH_LEAD_1_SQUARE = 80
    SYNTH_LEAD_2_SAW = 81
    SYNTH_LEAD_3_CALLIOPE = 82
    SYNTH_LEAD_4_CHIFF = 83
    SYNTH_LEAD_5_CHARANG = 84
    SYNTH_LEAD_6_VOICE = 85
    SYNTH_LEAD_7_FIFTHS = 86
    SYNTH_LEAD_8_BASS_LEAD = 87
    # Synth Pad
    SYNTH_PAD_1_NEW_AGE = 88
    SYNTH_PAD_2_WARM = 89
    SYNTH_PAD_3_POLOSYNTH = 90
    SYNTH_PAD_4_CHOIR = 91
    SYNTH_PAD_5_BOWED = 92
    SYNTH_PAD_6_METALLIC = 93
    SYNTH_PAD_7_HALO = 94
    SYNTH_PAD_8_SWEEP = 95
    # Synth Effects
    SYNTH_FX_1_RAIN = 96
    SYNTH_FX_2_SOUNDTRACK = 97
    SYNTH_FX_3_CRYSTAL = 98
    SYNTH_FX_4_ATMOSPHERE = 99
    SYNTH_FX_5_BRIGHTNESS = 100
    SYNTH_FX_6_GOBLINS = 101
    SYNTH_FX_7_ECHOES = 102
    SYNTH_FX_8_SCI_FI = 103
    # Ethnic
    SITAR = 104
    BANJO = 105
    SHAMISEN = 106
    KOTO = 107
    KALIMBA = 108
    BAGPIPE = 109
    FIDDLE = 110
    SHANAI = 111
    # Percussive
    TINKLE_BELL = 112
    AGOGO = 113
    DRUMS_STEEL = 114
    WOODBLOCK = 115
    TAIKO_DRUM = 116
    MELODIC_TOM = 117
    SYNTH_DRUM = 118
    CYMBAL_REVERSE = 119
    # SFX
    GUITAR_FRET_NOISE = 120
    BREATH_NOISE = 121
    SEASHORE = 122
    BIRD_TWEET = 123
    TELEPHONE_RING = 124
    HELICOPTER = 125
    APPLAUSE = 126
    GUNSHOT = 127


class Percussion(Enum):
    """Enumeration of all percussion available in MIDI"""
    BASS_DRUM_ACOUSTIC = 35
    BASS_DRUM_1 = 36
    RIMSHOT = 37
    SNARE_ACOUSTIC = 38
    HAND_CLAP = 39
    SNARE_ELECTRIC = 40
    LOW_FLOOR_TOM = 41
    CLOSED_HI_HAT = 42
    HIGH_FLOOR_TOM = 43
    PEDAL_HI_HAT = 44
    LOW_TOM = 45
    OPEN_HI_HAT = 46
    LOW_MID_TOM = 47
    HI_MID_TOM = 48
    CRASH_CYMBAL_1 = 49
    HIGH_TOM = 50
    RIDE_CYMBAL_1 = 51
    CHINESE_CYMBAL = 52
    RIDE_BELL = 53
    TAMBOURINE = 54
    SPLASH_CYMBAL = 55
    COWBELL = 56
    CRASH_CYMBAL_2 = 57
    VIBRA_SLAP = 58
    RIDE_CYMBAL_2 = 59
    HIGH_BONGO = 60
    LOW_BONGO = 61
    MUTE_HIGH_CONGA = 62
    OPEN_HIGH_CONGA = 63
    LOW_CONGA = 64
    HIGH_TIMBALE = 65
    LOW_TIMBALE = 66
    HIGH_AGOGO = 67
    LOW_AGOGO = 68
    CABASA = 69
    MARACAS = 70
    SHORT_WHISTLE = 71
    LONG_WHISTLE = 72
    SHORT_GUIRO = 73
    LONG_GUIRO = 74
    CLAVES = 75
    HIGH_WOOD_BLOCK = 76
    LOW_WOOD_BLOCK = 77
    MUTE_CUICA = 78
    OPEN_CUICA = 79
    MUTE_TRIANGLE = 80
    OPEN_TRIANGLE = 81


# Taken from http://www.procjam.com/tutorials/en/music/
class Scale(Enum):
    """Several scales (given by intervals between notes) commonly used in music"""
    MAJOR = [2, 2, 1, 2, 2, 2]  # classic, happy
    HARMONIC_MINOR = [2, 1, 2, 2, 1, 3]  # haunting, creepy
    MINOR_PENTATONIC = [3, 2, 2, 3]  # blues, rock
    NATURAL_MINOR = [2, 1, 2, 2, 1, 2]  # scary, epic
    MELODIC_MINOR_UP = [2, 1, 2, 2, 2, 2]  # wistful, mysterious
    # MELODIC_MINOR_DOWN = [2, 1, 2, 2, 1, 2]  # sombre, soulful, actually the same as harmonic minor
    DORIAN = [2, 1, 2, 2, 2, 1]  # cool, jazzy
    MIXOLYDIAN = [2, 2, 1, 2, 2, 1]  # progressive, complex
    AHAVA_RABA = [1, 3, 1, 2, 1, 2]  # exotic, unfamiliar
    MAJOR_PENTATONIC = [2, 2, 3, 2]  # country, gleeful
    DIATONIC = [2, 2, 2, 2, 2]  # bizarre, symmetrical
    # CHROMATIC = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # random, atonal: all twelve notes

    def start_from(self, start_note):
        """
        Creates the scale as a sequence of notes starting from a given note.
        Note can be passed in int or string representation.
        """
        start_note = ensure_is_number(start_note)
        return list(map(lambda x: start_note + x, [0] + list(np.cumsum(self.value))))


# Taken from http://www.procjam.com/tutorials/en/music/
class Chord(Enum):
    """
    Several chords given as commonly used in music, stored as distances from first note.
    Note can be passed in int or string representation.
    """
    MAJOR = [0, 4, 7]
    MINOR = [0, 3, 7]
    REL_MINOR_1ST_INV = [0, 4, 9]
    SUBDOMINANT_2ND_INV = [0, 5, 9]
    MAJOR_7TH = [0, 4, 7, 11]
    MINOR_7TH = [0, 3, 7, 10]
    MAJOR_9TH = [0, 4, 7, 14]
    MINOR_9TH = [0, 3, 7, 13]
    MAJOR_6TH = [0, 4, 9]
    MINOR_6TH = [0, 3, 8]
    MAJOR_7TH_9TH = [0, 4, 7, 11, 14]
    MINOR_7TH_9TH = [0, 3, 7, 10, 13]
    MAJOR_7TH_11TH = [0, 4, 7, 11, 18]
    MINOR_7TH_11TH = [0, 3, 7, 10, 17]

    def start_from(self, start_note):
        """
        Chord as a sequence of notes starting on a given note. Note can be passed in int or string representation.
        """
        start_note = ensure_is_number(start_note)
        return list(map(lambda x: start_note + x, self.value))

    def end_at(self, end_note):
        """
        Chord as a sequence of notes ending at a given note. Note can be passed in int or string representation.
        """
        end_note = ensure_is_number(end_note)
        last_value = self.value[-1]
        return list(map(lambda x: end_note - last_value + x, self.value))


class Song:
    """
    Main class of composing, representing the whole song. You can add tracks to it and eventually save it into MIDI.
    """
    def __init__(self, bpm):
        self.bpm = bpm
        self.tracks = []

    def new_track(self, instrument=Instrument.PIANO_ACOUSTIC_GRAND):
        track = Track(self.bpm, instrument, MidiFile().ticks_per_beat, len(self.tracks))
        self.tracks.append(track)
        return track

    def drum_track(self):
        track = Track(self.bpm, Instrument.PIANO_ACOUSTIC_GRAND, MidiFile().ticks_per_beat, 9)
        self.tracks.append(track)
        return track

    def save(self, filename):
        midi_file = MidiFile()
        for i, track in enumerate(self.tracks):
            midi_file.tracks.append(track.to_midi_track())
        midi_file.save(filename)


class Track:
    # Helper class to represent "elements" of music (key press / key release)
    class MusicEvent:
        def __init__(self, type, note, tick):
            self.type = type
            self.note = note
            self.tick = tick

    def __init__(self, bpm, instrument, ticks_per_beat, channel):
        """
        Inits the track. Bound directly to a specific channel, thus we don't need to swap instruments on the go.
        """
        self.bpm = bpm
        self.ticks_per_beat = ticks_per_beat
        self.instrument = instrument
        self.events = []
        self.channel = channel

    # Adds a note to this track
    def add_note(self, note, beat, length):
        """
        Adds a note to a beat on this track. Notes can be given either by string or int representation.
        """
        note = ensure_is_number(note)

        start_tick = int(round(beat * self.ticks_per_beat))
        length_ticks = int(round(length * self.ticks_per_beat))

        self.events.append(Track.MusicEvent('start', note, start_tick))
        self.events.append(Track.MusicEvent('stop', note, start_tick + length_ticks))

    def add_beat(self, drum, beat, length):
        """
        Adds percussion hit to a beat in this track. Should be one of the Percussion enum.
        Also, this track should be created by the drum_track function of song.
        """
        # By General MIDI standard, percussion is on track 10 (counting from one)
        self.add_note(drum.value, beat, length)

    def add_chord(self, notes, beat, length):
        """Adds a chord (list of notes) to a single beat in this track."""
        self.add_arpeggio(notes, beat, length, 0.0)

    def add_arpeggio(self, notes, beat, length, arpeggio_spread=0.3):
        """
        Adds a chord as an arpeggio.
        :param notes: list of notes to be played
        :param beat: beat the arpeggio should start at
        :param length: length of individual notes presses (in beats)
        :param arpeggio_spread: interval, over which is the arpeggio spread (in beats)
        :return:
        """
        starts = np.linspace(beat, beat + arpeggio_spread, len(notes))
        for note, note_start in zip(notes, starts):
            self.add_note(note, note_start, length)

    def to_midi_track(self):
        """Converts this track to MidiTrack from mido"""
        track = MidiTrack()
        track.append(MetaMessage('set_tempo', tempo=bpm2tempo(self.bpm)))
        # dont yet know what this does
        track.append(Message('program_change', program=self.instrument.value, time=0, channel=self.channel))

        preprocessed_events = self.__preprocess_events()

        last_tick = 0
        for event in preprocessed_events:
            time_diff = event.tick - last_tick
            last_tick = event.tick

            track.append(Message(
                'note_on' if event.type == 'start' else 'note_off',
                note=event.note,
                velocity=64,
                time=time_diff,
                channel=self.channel,
            ))
        return track

    def __preprocess_events(self):
        """
        We want to deal with overlapping notes (it can happen by accident easily enough)
        Thus, we monitor amount of times pressed, and only release if it hits 0
        Also we need to release keys before re-pressing them
        """
        self.events.sort(key=lambda ev: ev.tick)

        current_presses = defaultdict(int)
        preprocessed_events = []
        for event in self.events:
            current_presses[event.note] += 1 if event.type == 'start' else -1

            # If a key is pressed again, release it before that
            if event.type == 'start' and current_presses[event.note] > 1:
                preprocessed_events.append(Track.MusicEvent('stop', event.note, event.tick))
            # If a key was pressed again, don't release it on the original release
            if event.type == 'stop' and current_presses[event.note] != 0:
                continue

            preprocessed_events.append(event)

        return preprocessed_events


def note2number(note):
    """
    Converts string representation (e.g. "G5" or "F#4") to integer representation of the note ("C0" = 0, "C#0" = 1)
    """
    tone = note[:-1]
    octave = int(note[-1])
    return octave * 12 + note_seq.index(tone)


def number2note(num):
    """
    Converts integer (e.g. 65, 66) to string representation of the note (65 = "F5", 66 = "F#5").
    """
    return note_seq[num % 12] + str(num // 12)


def ensure_is_number(num_or_note):
    """
    Converts the note to number if it was a string.
    """
    return note2number(num_or_note) if isinstance(num_or_note, str) else num_or_note
