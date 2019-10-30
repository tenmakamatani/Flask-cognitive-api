from janome.tokenizer import Tokenizer
import re

class Setup:

    def separate_text(self, text_path, output_path):
        # Read text from text_path
        try:
            not_separated_text = open(text_path, 'rb').read()
        except IOError:
            raise IOError
        
        not_separated_text = not_separated_text.decode('utf-8')

        # Delete disturbing words and patterns
        disturbing_words = ['\r', '\u3000', '-', '｜']
        for nww in disturbing_words:
            not_separated_text = not_separated_text.replace(nww, '')

        disturbing_patterns = [re.compile(r'《.*》'), re.compile(r'［＃.*］')]
        for nwp in disturbing_patterns:
            not_separated_text = re.sub(nwp, '', not_separated_text)
        
        # Separate text and delete disturbing words
        words = Tokenizer().tokenize(not_separated_text, wakati=True)
        disturbing_chars = [
            '(',
            ')',
            '[',
            ']',
            '"',
            "'",
            '\n'
        ]
        splited_text = ''
        for word in words:
            if word not in disturbing_chars:
                splited_text += word
            if word != '。' and word != '、' and word != '\n':
                splited_text += ' '
            if word == '。':
                splited_text += '\n'
                    
        # Write into output file
        try:
            with open(output_path, 'w') as f:
                f.write(splited_text)
        except IOError:
            raise IOError
        
        return 'ok'

if __name__ == '__main__':
    setup = Setup()
    setup.separate_text('./resources/not_splited.txt', './resources/splited.txt')