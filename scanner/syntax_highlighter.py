from bs4 import BeautifulSoup
import statics


class SyntaxHighlighter:

    def __init__(self):
        html = """
        <html>
        <head>
        </head>
        
        <body class="background">
        </body>
        </html>
        
        """
        self.soup = BeautifulSoup(html, 'html.parser')
        self.soup.head.append(BeautifulSoup(statics.css, 'html.parser'))

    def highlight(self, token):
        for k, v in statics.class_type_map.items():
            if token.type in v:
                code = f'<span class="{k}">{token.value}</span>'.replace('\n', '<br>')
                self.soup.body.append(BeautifulSoup(code, 'html.parser'))
                return
        if token.type == 'SPACE':
            code = f"<span>{'&nbsp;' * len(token.value)}</span>"
            self.soup.body.append(BeautifulSoup(code, 'html.parser'))
            return
        self.soup.body.append(BeautifulSoup(f'<span class="ERROR">{token.value}</span>', 'html.parser'))

    def flush(self, file_name):
        with open(file_name, 'w') as f:
            f.write(str(self.soup.prettify(formatter="html5")))
