# Telegram to Google Drive Bot 🤖☁️

Este bot recibe **una foto o video** por Telegram y luego el **nombre con el que querés guardarlo**. Luego lo **sube automáticamente a tu Google Drive**.

## 🚀 ¿Cómo usar?

1. Cloná este repositorio o subilo a Render.
2. Cargá tus variables de entorno:
   - `TELEGRAM_TOKEN`: el token de tu bot de Telegram
   - `DRIVE_FOLDER_ID`: ID de la carpeta de Google Drive donde se subirán los archivos
3. Subí tu archivo `credentials.json`
4. Instalá las dependencias:
```bash
pip install -r requirements.txt
```
5. Ejecutá el bot:
```bash
python main.py
```
