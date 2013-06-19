#!/usr/bin/python2.7
import re
import sys
import operator

chr_scale = ['A', 'A#', 'B', 'C', 'C#', 'D',
             'D#', 'E', 'F', 'F#', 'G', 'G#']

chord_names = {"Major": [0,4,7], "Minor": [0,3,7], "Major7": [0,4,7,11],
               "Augmented": [0, 4, 8], "Diminished": [0,3,6], "Diminished7": [0,3,6,9],
               "Half-diminished7": [0,3,6,10], "Minor-major7": [0, 3, 7, 11],
               "Augmented7": [0, 4, 8, 10], "Augmented major7": [0, 4, 8, 11],
               "Minor7": [0,3,7,10], "Major6": [0,4,7,9],
               "Minor6": [0,3,7,9], "Dominant7": [0,4,7,10],
               "Sus2": [0,2,7], "Sus4": [0,5,7], "Add9": [0,2,4,7]}

def parse_notes(notes):
    """ Parses a string and converts valid notes to sharp notation

    Valid notes include a letter A-G, uppercase or lowercase, followed by
    between 0 and 2 sharp symbols (hash symbol "#") or between 0 and 2 flat
    symbols (lower case "b"). Notes are converted to their enharmonic
    equivalent if they contain a flat symbol, so only natural notes and sharp
    notes are returned.
    
    >>> parse_notes("C D J b D# G## Ab AB")
    ['C', 'D', 'A#', 'D#', 'A', 'G#', 'A', 'B']

    Args:
        A string containing valid notes
    Returns:
        A list of valid sharp-notation notes

    """
    raw_list = re.compile("[A-Ga-g][#b]{0,2}").findall(notes)
    parsed_list = []
    for note in raw_list:
        note_name = note[0]  #First character is name of note
        chr_note_pos = chr_scale.index(note_name.upper())  #Get chr_scale index
        #Increment or decrement if sharps or flats are found
        for char in note:
            if char == "#": chr_note_pos += 1
            elif char == "b": chr_note_pos -= 1
        #Get the enharmonic equivalent from chr_scale and append it to
        #the list to be returned.
        final_chr_note = chr_scale[(chr_note_pos + 12) % 12]
        parsed_list.append(final_chr_note)
    return parsed_list

def find_chords(notes):
    """ Finds chords that describe the notes given

    >>> find_chords("A, C#, E")
    ['A Major']
    >>> find_chords("C, E, G, E, C")
    ['C Major']
    >>> find_chords("C D G")
    ['C Sus2', 'G Sus4']

    Args:
        A list of notes in sharp notation

    Returns:
        A list of chord names that describe the given notes

    """
    notes = parse_notes(notes)
    chords_found = []
    #Each iteration, we assume a different note is the tonic
    for tonic in notes:
        pattern = []
        #Each note is compared to the tonic and a pattern is built
        for note in notes:
            interval = ((chr_scale.index(note) -
                         chr_scale.index(tonic)) + 12 ) % 12
            pattern.append(interval)
        
        pattern = list(set(pattern)) #Eliminate duplicate intervals
        pattern.sort()
        #Match the pattern to one in the chord library
        for name, match_pattern in chord_names.items():
            if pattern == match_pattern:
                chords_found.append(str(tonic) + " " + str(name))
    return list(set(chords_found)) #Eliminate duplicate chord names

if __name__ == "__main__":    
    import doctest
    doctest.testmod()
    #No args given
    if len(sys.argv) == 1:
      print "Usage: chordfinder.py {note1} [note2] [note3] ..."
      sys.exit(1)

    #Flatten the args into a single string
    notes = reduce(operator.concat, sys.argv[1:])
    #Find and display chords
    chords = find_chords(notes)
    for chord in chords:
      print chord
