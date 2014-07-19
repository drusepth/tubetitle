#!/usr/bin/py
import re

class SongDataExtractor:
  POTENTIAL_DELIMITERS = ['-', '~', '|']

  STRIPPABLE_TOKENS = ['\([^\)]+\)', '\[[^\]]+\]']
  STRIP_EXCEPTIONS  = ['f(ea)?t(uring)?\.? .+', '.+ remix']

  # Extract metadata from a string
  def information(self, string):
    string    = self.normalize(string)
    delimiter = self.find_delimiter(string)
    chunks    = string.split(delimiter, 2)

    return chunks

  def normalize(self, string):
    string = self.clear_tokens(string)
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
      match_result = re.search(token, string)
      if match_result != None:
        innards = match_result.group(0)
        remove_match = True
        
        for exception in self.STRIP_EXCEPTIONS:
          if re.match(exception, innards):
            replace = False
            break
        
        if remove_match:
          string = re.sub(token, '', string)
          string = self.clear_tokens(string)

    return string

titles = open('titles.txt', 'r')
extract = SongDataExtractor()

for title in titles:
  print title
  print extract.information(title)
