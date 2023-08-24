# 
import json
import locale
import ctypes

class localized:
  # Switch to default UI's language if possible
  json_data = ""
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
        self.__json_data = json.load(jsd)
      jsd.close()
    except:
      with open(f"locales/default.json") as jsd:
        self.__json_data = json.load(jsd)
      jsd.close()
    finally:
      with open(f"locales/default.json") as jsd:
        self.__default = json.load(jsd)
      jsd.close()
  
  def get(self, textkey):
    if textkey in self.__json_data:
      return self.__json_data[textkey]
    if textkey in self.__default:
      return __default[textkey]
    return textkey + " (no description available)"