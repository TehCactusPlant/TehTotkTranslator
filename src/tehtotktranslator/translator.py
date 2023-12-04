import random, logging
from abc import ABC, abstractmethod
import translators as ts

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Translator(ABC):
    def __init__(self, input_file, output_file,translator='bing', **kwargs):
        self.input_file = input_file
        self.output_file = output_file
        self.translator = translator
        self.base_data = []
        self.output_data = []
        self.langs = ts.get_languages(self.translator)
        self.english: list = self.langs['en']
        self.lang_list = self.langs.keys()
        self.from_lang = 'en'
        self.to_lang = 'en'
        self.min_iterations = 3
        self.max_iterations = 7

    def update_vpn(self):
        pass

    def translate_text(self, from_lang, to_lang, text_to_translate):
        text_to_translate = ts.translate_text(query_text=text_to_translate, translator=self.translator, from_language=from_lang, to_language=to_lang)
        return text_to_translate

    def random_iteration(self, text_to_translate):
        while True:
            try:
                current_map = self.langs[self.from_lang]
                self.to_lang = random.choice(current_map)
                translated_text = self.translate_text(self.from_lang, self.to_lang, text_to_translate)
                self.from_lang = self.to_lang
                return translated_text
            except Exception as e:
                logger.warning(f"Failed to translate {text_to_translate} from {self.from_lang} to {self.to_lang}")

    def bad_translate(self, text_to_translate, iterations=5):
        before = text_to_translate.strip()
        for i in range(0, iterations):
            text_to_translate = self.random_iteration(text_to_translate)
        text_to_translate = self.translate_text(self.from_lang, 'en', text_to_translate)
        logger.info(f"Translated over {iterations} iterations: {before} -> {text_to_translate}")
        return text_to_translate

    def write_file(self, data):
        with open(self.output_file, 'w+') as file:
            for line in data:
                file.write(f"{line}\n")


class GenericTranslator(Translator):
    def __init__(self, input_file, output_file, **kwargs):
        super().__init__(input_file, output_file, **kwargs)

    def mass_translate(self):
        with open(self.input_file, 'r+') as file:
            self.base_data = file.readlines()

        output_data = self.base_data
        for i in range(0, len(output_data) - 1):
            entry = output_data[i]
            if '|-' in entry:
                # Filename, ignore
                pass
            else:
                entry = f"  {self.bad_translate(entry, random.randint(self.min_iterations, self.max_iterations))}"

        logging.info("Dumping entries in case of fatal error:")
        for entry in output_data:
            print(entry)
        logger.info("Data dump complete")

        self.write_file(output_data)
