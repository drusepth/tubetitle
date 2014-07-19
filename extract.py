#!/usr/bin/py
import re

class SongDataExtractor:
  POTENTIAL_DELIMITERS = ['-', '~', '|']

  STRIPPABLE_TOKENS = ['\([^\)]+\)', '\[[^\]]+\]']
  STRIP_EXCEPTIONS  = ['f(ea)?t(uring)?\.? .+', '.+ remix', '.+ version']

  # Extract metadata from a string
  def information(self, string):
    string    = self.normalize(string)
    string    = self.clear_tokens(string)
    delimiter = self.find_delimiter(string)
    chunks    = map(lambda x:self.normalize(x), string.split(delimiter, 2))
    chunks    = self.put_artist_first(chunks)

    return chunks

  def put_artist_first(self, chunks):
    # todo
    return [chunks[0], chunks[1]]

  def normalize(self, string):
    string = string.strip()
    string = string.title()

    return string

  def find_delimiter(self, string):
    for symbol in self.POTENTIAL_DELIMITERS:
      if string.count(symbol) == 1:
        return symbol
    
    return "UNKNOWN"

  def clear_tokens(self, string):
    for token in self.STRIPPABLE_TOKENS:
      match_result = re.search(token, string, re.IGNORECASE)

      if match_result != None:
        innards = match_result.group(0)

        remove_match = True
        for exception in self.STRIP_EXCEPTIONS:
          if re.search(exception, innards, re.IGNORECASE) != None:
            remove_match = False
            break
        
        if remove_match == True:
          string = re.sub(token, '', string, re.IGNORECASE)
          string = self.clear_tokens(string)

    return string

titles = open('test.txt', 'r')
extract = SongDataExtractor()

for title in titles:
  print title.strip()
  print extract.information(title)
  print '-------------------------'
