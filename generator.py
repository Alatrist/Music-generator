from composing import Song, Percussion, Instrument, Scale, Chord, note2number, number2note, note_seq
import numpy as np
import os
import math

def take_closest(ref, values):
    min=0
    min_dist = 10000000
    for i in values:
        dist = abs(ref - i)
        if dist<min_dist:
            min_dist=dist
            min = i
    return min


def generate_melody(seed, start, length, track, melody_range, chords):
    r = np.random.RandomState(seed)
    pos = 0
    note_len = 0.5
    current_note = r.randint(0, len(melody_range))
    current_note = current_note + r.randint(-2, 3)
    current_note = np.clip(current_note, 0, len(melody_range) - 1)
    while pos<length-note_len:
        if pos % 2 == 0:
            chord_tones = chords[int(pos//4)] + chords[int(pos//(3/4))]
            current_note_val = take_closest(melody_range[current_note], chord_tones)
            track.add_note(current_note_val, pos + start, note_len)
        else:
            track.add_note(melody_range[current_note.item()], pos+start, note_len)
        pos += note_len
        if r.uniform() < 0.1:
            pos = math.ceil(pos)
        current_note = current_note + r.randint(-2, 3)
        current_note = np.clip(current_note, 0, len(melody_range) - 1)

        if r.uniform() < 0.33:
            if r.uniform()<0.5 and note_len<2:
                note_len *= 2
            elif note_len>0.25:
                note_len /= 2.0


def generate_bas(seed, start, length, track, chords):
    r = np.random.RandomState(seed)
    pos = 0
    note_len = 0.5

    while pos < length - note_len:
        chord_tones = chords[int(pos // 2)]
        track.add_note(chord_tones[r.randint(0, len(chord_tones))], pos + start, note_len)
        pos += note_len
        if r.uniform() < 0.3:
            pos = math.ceil(pos)
        if r.uniform() < 0.33:
            if r.uniform() < 0.5 and note_len < 2:
                note_len *= 2
            elif note_len > 0.25:
                note_len /= 2.0


def generate_harmony(seed, start, length, track, chords):
    r = np.random.RandomState(seed)
    pos = 0
    note_len = 1

    while pos < length - note_len:
        if r.uniform()<0.1:
            pos += note_len
        else:
            chord_tones = chords[int(pos // 4)] + chords[int(pos // 3/4)]

            if r.uniform()<0.:
                chord = chord_tones = chords[int(pos // 4)]
            else:
                chord = chord_tones = chords[int(pos // (3 / 4))]
            track.add_chord(chord, pos+start, note_len)

            pos += note_len
            if r.uniform() < 0.3:
                pos = math.ceil(pos)
            if r.uniform() < 0.33:
                if r.uniform() < 0.5 and note_len < 2:
                    note_len *= 2
                elif note_len > 0.5:
                    note_len /= 2.0



def generate_drums(seed, start, length, track, drums, optional_drum, optional_track):
    rng = np.random.RandomState(seed)
    main_drum = []
    r_val = rng.uniform()
    if r_val <0.25:
        main_drum = [True, True, True, True]
    elif r_val<0.5:
        main_drum = [True, False, True, False]
    elif r_val<0.75:
        main_drum = [True, False, False, False]
    else:
        main_drum = [True, False, False, True]

    drum1 = []
    for i in range(8):
        drum1.append(rng.uniform()<0.5)

    drum2 = []
    drum2_len = 0.25
    r_val = rng.uniform()
  #  if r_val<0.5:
  #      drum2_len = 0.25

    pos = 0
    index = 0
    while pos < 4:
        drum2.append(rng.uniform()<0.5)
        index+=1
        pos +=drum2_len

    for i in range(start, start + length, 4):
        for p in range(4):
            if main_drum[p]:
                track.add_note(note2number(drums[0]), i+p, 1)
        for p in range(8):
            if drum1[p]:
                track.add_note(note2number(drums[1]), i+p/2.0, 0.5)
        for p in range(int(4.0/drum2_len)):
            if drum2[p]:
                track.add_note(note2number(drums[2]), i+p*drum2_len, drum2_len)
        if rng.uniform()<0.33:
            for p in range(4):
                if rng.uniform()<0.5:
                    optional_track.add_beat(optional_drum, i+p, 1)


def drum_len(rng):
    r_val = rng.uniform()
    if r_val<0.33:
        return 0.125
    elif r_val<0.66:
        return 0.25
    else:
        return 0.5


def drum_solo(seed, start, length, drums, track):
    rng = np.random.RandomState(seed)
    active_drum = rng.randint(0, len(drums))
    drum_length = drum_len(rng)
    pos = 0
    while pos+drum_length<length:
        if pos == int(pos) and rng.uniform() < 0.2:
            active_drum = rng.randint(0, len(drums))
        if pos == int(pos) and rng.uniform() < 0.2:
            drum_length = drum_len(rng)
        if rng.uniform() < 0.1:
            pos+=drum_length*2
        else:
            track.add_note(note2number(drums[active_drum]), start+pos, drum_length)



def generate_chords(notes_range, l, r):
    chords =[]
    chord_len = 2
    tones =len(notes_range)
    while len(chords)<l:
        tone = r.randint(0, len(notes_range)-1)
        chord = [notes_range[tone], notes_range[(tone+3)%tones], notes_range[(tone+5)%tones]]
        chords.append(chord)
        if chord_len == 2:
            chords.append(chord)
        else:
            chord_len = 2
        if r.uniform()<0.2:
            chord_len = 1
    return chords

def run():
    seed = np.random.randint(1000000)
    song_name = name_from_seed(seed)

    song = Song(np.random.randint(120,150))

    # Very simple fixed drumset
    #drum_track = song.drum_track()
    synth_track = song.new_track(Instrument.SYNTH_DRUM)

    main_rng = np.random#.RandomState(1111)

    key = note_seq[main_rng.randint(0, 12)]
    key_type = Scale.MAJOR
    pentatonic = Scale.MAJOR_PENTATONIC

    drum_tones = [key + "2", key + "3", key + "4"]
    solo_drum_tones = [key + "3", key + "4", key + "5"]
    samples = []

    sample_count = 3

    for i in range(sample_count):
        length = 8 * main_rng.randint(1, 3)
        seed = main_rng.randint(10000000)
        r = np.random.RandomState(seed)
        bass_chords = generate_chords(key_type.start_from(key+"1"), length, r)
        r = np.random.RandomState(seed)
        melody_chords_l = generate_chords(key_type.start_from(key+"4"), length, r)
        r = np.random.RandomState(seed)
        melody_chords_h = generate_chords(key_type.start_from(key + "5"), length, r)
        harmony_chords = generate_chords(key_type.start_from(key + "3"), length, r) + generate_chords(key_type.start_from(key + "4"), length, r)
        samples.append((length, seed, bass_chords, (melody_chords_l, key_type.start_from(key+"3") + key_type.start_from(key+"4")),
                        (melody_chords_h, pentatonic.start_from(key+"4") + pentatonic.start_from(key+"5") ), harmony_chords))

    iters = main_rng.randint(12 , 20)
    position = 0
    drum_track = song.new_track(Instrument.SYNTH_DRUM)
    bass_track = song.new_track(Instrument.BASS_SYNTH_1)
    melody_track = song.new_track(Instrument.SYNTH_LEAD_6_VOICE)
    harmony_track = song.new_track(Instrument.SYNTH_PAD_3_POLOSYNTH)

    for i in range(iters):
        sample = main_rng.randint(sample_count)
        length = samples[sample][0]
        seed = samples[sample][1]
        bass_harmony = samples[sample][2]
        melody_chords_l = samples[sample][3][0]
        melody_chords_h = samples[sample][4][0]
        harmony_chords = samples[sample][5]
        melody_chords = melody_chords_h + melody_chords_l
        melody_range = samples[sample][4][1]


        if main_rng.uniform()<0.1:  #drum solo
            drum_solo(seed, position, length, solo_drum_tones, drum_track)
        else:
            is_playing = False
            if main_rng.uniform()<0.8:
                generate_drums(seed, position, length, synth_track, drum_tones, Percussion.HAND_CLAP, synth_track)
                is_playing = True
            if main_rng.uniform() < 0.5:
                generate_bas(seed, position, length, bass_track, bass_harmony)
                is_playing = True
            if main_rng.uniform() < 0.7:
                generate_melody(seed, position, length, melody_track, melody_range, melody_chords)
                is_playing = True
            if main_rng.uniform() < 0.5:
                if is_playing:
                    generate_harmony(seed, position, length, harmony_track, harmony_chords)
                    is_playing = True
                else:
                    generate_harmony(seed, position, 8, harmony_track, harmony_chords)
                    position += 8

            if is_playing:
                position += length


    if not os.path.exists('out'):
        os.mkdir('out')

    song.save('out/{}.mid'.format(song_name))
    print('Generated song "{}"'.format(song_name))


def name_from_seed(seed):
    with open('assets/nouns.txt') as f:
        nouns = [s.strip() for s in f.readlines()]
    with open('assets/adjectives.txt') as f:
        adjectives = [s.strip() for s in f.readlines()]
    noun = nouns[seed % 1000]
    adjective = adjectives[seed // 1000]
    return '{}_{}'.format(adjective, noun)


if __name__ == '__main__':
    run()
