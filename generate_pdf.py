import asyncio
from playwright.async_api import async_playwright
import os
import sys

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

async def generate_pdf():
    html_file = os.path.abspath('cv_profesional_eddi.html')
    pdf_file = os.path.abspath('cv_profesional_eddi.pdf')
    
    # Convertir la ruta de Windows a formato file://
    html_url = f'file:///{html_file.replace(os.sep, "/")}'
    
    async with async_playwright() as p:
        print("Iniciando navegador...")
        # Configuración optimizada para mejor calidad
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-web-security', '--disable-features=VizDisplayCompositor']
        )
        
        # Crear contexto con configuración de alta calidad
        context = await browser.new_context(
            viewport={'width': 1200, 'height': 1600},
            device_scale_factor=2  # Mayor resolución para mejor calidad
        )
        page = await context.new_page()
        
        print(f"Cargando HTML desde: {html_url}")
        await page.goto(html_url, wait_until='networkidle')
        
        # Esperar a que las fuentes de Google se carguen completamente
        await page.wait_for_load_state('networkidle')
        await page.wait_for_timeout(3000)  # Tiempo adicional para fuentes
        
        # Forzar renderizado de fuentes web
        await page.evaluate('''() => {
            document.fonts.ready.then(() => {
                return new Promise(resolve => setTimeout(resolve, 500));
            });
        }''')
        
        print(f"Generando PDF en: {pdf_file}")
        
        # Configuración optimizada para alta calidad
        await page.pdf(
            path=pdf_file,
            format='A4',
            print_background=True,
            margin={
                'top': '0mm',
                'right': '0mm',
                'bottom': '0mm',
                'left': '0mm'
            },
            prefer_css_page_size=True,
            scale=1.0,
            display_header_footer=False,
            tagged=True
        )
        
        await browser.close()
        print(f"PDF generado exitosamente: {pdf_file}")

if __name__ == '__main__':
    try:
        asyncio.run(generate_pdf())
    except Exception as e:
        print(f"Error: {e}")
        print("\nIntentando instalar los navegadores de Playwright...")
        import subprocess
        import sys
        subprocess.run([sys.executable, '-m', 'playwright', 'install', 'chromium'], check=False)

