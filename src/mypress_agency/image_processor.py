import os
import yaml
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

class ImageProcessor:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config/brand_config.yaml')
        
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)['brand']

    def create_branded_cover(self, background_path, title_text, output_path):
        """
        Sobrepõe texto e elementos gráficos em uma imagem de fundo.
        """
        # 1. Carrega a imagem de fundo gerada pela IA
        bg = Image.open(background_path).convert("RGBA")
        
        # Redimensiona para o padrão do blog (ex: 1200x630)
        target_size = (self.config['layout']['width'], self.config['layout']['height'])
        bg = bg.resize(target_size, Image.Resampling.LANCZOS)

        # 2. Cria uma camada de overlay para o texto (opcional, para legibilidade)
        overlay = Image.new("RGBA", target_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        
        # Desenha um retângulo branco semi-transparente no lado esquerdo (estilo do exemplo)
        draw.rectangle([0, 0, 500, target_size[1]], fill=(255, 255, 255, 180))

        # 3. Adiciona o Texto
        try:
            # Tenta carregar uma fonte padrão do sistema, senão usa a básica
            font_bold = ImageFont.load_default(size=self.config['fonts']['title_size'])
            font_regular = ImageFont.load_default(size=self.config['fonts']['subtitle_size'])
        except:
            font_bold = ImageFont.load_default()
            font_regular = ImageFont.load_default()

        # Divide o título em "Guia de" e o "Assunto" (estilo do exemplo)
        main_title = title_text.upper()
        prefix = "GUIA DE"
        
        x = self.config['layout']['text_x_offset']
        y = self.config['layout']['text_y_offset']

        # Desenha o prefixo (Cinza)
        draw.text((x, y), prefix, font=font_regular, fill=self.config['colors']['secondary'])
        
        # Desenha o título principal (Vermelho)
        # Quebra o texto se for muito longo
        words = main_title.split()
        current_y = y + 50
        line = ""
        for word in words:
            if len(line + word) < 15:
                line += word + " "
            else:
                draw.text((x, current_y), line.strip(), font=font_bold, fill=self.config['colors']['primary'])
                current_y += 70
                line = word + " "
        draw.text((x, current_y), line.strip(), font=font_bold, fill=self.config['colors']['primary'])

        # 4. Combina as camadas
        combined = Image.alpha_composite(bg, overlay)
        combined.convert("RGB").save(output_path, "PNG")
        
        return output_path

# Singleton
image_processor = ImageProcessor()
