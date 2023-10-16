# 
import re
import json
import locale
import ctypes

class localized:
  # Switch to default UI's language if possible
  _json_data = ""
  _windll = ctypes.windll.kernel32
  current_lang = locale.windows_locale[ _windll.GetUserDefaultUILanguage() ]
  
  def __init__(self, langcode=None): 
    self.langdic = {\
      "en_GB" : "English (Great Britain)",\
      "en_US" : "English (United States)",\
      "de_DE" : "German"\
    }
    
    self.current_language_name = "English (United States)"
    try:
      self.current_language_name = self.langdic[self.current_lang]
    except:
      pass
  
    if langcode != None:
      self.__prepareJson(langcode)
    else:
      self.__prepareJson(self.current_lang)
  
  #
  def __prepareJson(self, langcode):
    try:
      with open(f"locales/{langcode}.json") as jsd:
        self._json_data = json.load(jsd)
      jsd.close()
    except:
      with open(f"locales/default.json") as jsd:
        self._json_data = json.load(jsd)
      jsd.close()
    finally:
      with open(f"locales/default.json") as jsd:
        self._default = json.load(jsd)
      jsd.close()
  
  def get(self, textkey):
    if textkey in self._json_data:
      return self._json_data[textkey]
    if textkey in self._default:
      return _default[textkey]
    return textkey + " (no description available)"


class textfilter:
  @staticmethod
  def make_readable(rawtext):
    rawtext = [re.sub(r"\n+", " ", str(x)) for x in rawtext]
    rawtext = [re.sub(r"([a-z])([A-Z])", r"\1 \2", str(x)) for x in rawtext]
    rawtext = [re.sub(r"([A-Z]{2,})([a-z])", r"\1 \2", str(x)) for x in rawtext]
    rawtext = [re.sub(r"([0-9])([A-Z])", r"\1 \2", str(x)) for x in rawtext]
    rawtext = [re.sub(r"([A-Z])([0-9])", r"\1 \2", str(x)) for x in rawtext]
    rawtext = [re.sub(r"([0-9])([a-z])", r"\1 \2", str(x)) for x in rawtext]
    rawtext = [re.sub(r"(\))([A-Z])", r"\1 \2", str(x)) for x in rawtext]
    rawtext = [re.sub(r'– +', "–", str(x)) for x in rawtext]
    # rawtext = [re.sub(r'\n', " ", str(x)) for x in rawtext]
    rawtext = [re.sub(r'\s+', " ", str(x)) for x in rawtext]
    ####
    # remove control bytes except from \0\t\r\n
    rawtext = [re.sub(r"[\x01-\x08]", "", str(x)) for x in rawtext]
    rawtext = [re.sub(r"[\x0b-\x0c]", "", str(x)) for x in rawtext]
    rawtext = [re.sub(r"[\x0e-\x1f]", "", str(x)) for x in rawtext]
    rawtext = [re.sub(r"[\x1f]", "", str(x)) for x in rawtext]
    return rawtext