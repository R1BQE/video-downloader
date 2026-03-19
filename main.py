import yt_dlp
import os
import subprocess
import winsound

# Путь к WAV файлу для проигрывания
wav_file = os.path.join(os.getcwd(), 'success.wav')  # Поменяйте на путь к вашему WAV файлу

def download_video(url):
    # Папка для видеофайлов
    video_folder = os.path.join(os.getcwd(), 'video')
    
    # Проверяем, существует ли папка "video", если нет — создаем её
    if not os.path.exists(video_folder):
        os.makedirs(video_folder)

    # Параметры для скачивания видео
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Скачиваем лучшее видео с аудио
        'outtmpl': os.path.join(video_folder, '%(title)s.%(ext)s'),  # Путь для сохранения видео
        'progress_hooks': [progress_hook],  # Хук для отслеживания прогресса
        'quiet': True,  # Тихий режим
        'noplaylist': True  # Не скачивать плейлист, только одно видео
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])  # Скачиваем видео
        # Получаем имя скачанного файла
        downloaded_file = ydl.prepare_filename(ydl.extract_info(url, download=False))
        
    # После завершения скачивания — проигрываем WAV файл
    print("\nЗагрузка видео завершена.")
    play_wav(wav_file)  # Воспроизведение WAV файла

    return downloaded_file  # Возвращаем путь к скачанному видео


def convert_to_mp3(video_file):
    # Папка для аудиофайлов
    audio_folder = os.path.join(os.getcwd(), 'audio')

    # Проверяем, существует ли папка "audio", если нет — создаем её
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    # Проверка расширения файла
    valid_video_extensions = ['.mp4', '.mkv', '.webm', '.flv', '.avi', '.mov']
    file_extension = os.path.splitext(video_file)[1].lower()
    
    if file_extension not in valid_video_extensions:
        print(f"Ошибка: файл {video_file} не является видеофайлом с поддерживаемым расширением.")
        return

    # Путь для сохранения MP3
    audio_file = os.path.join(audio_folder, f"{os.path.splitext(os.path.basename(video_file))[0]}.mp3")

    # Проверяем существует ли видеофайл
    if not os.path.exists(video_file):
        print(f"Видео файл {video_file} не найден.")
        return

    # Команда для конвертации с помощью ffmpeg
    try:
        print(f"Конвертируем видео {video_file} в MP3...")
        subprocess.run(['ffmpeg', '-i', video_file, '-vn', '-acodec', 'libmp3lame', audio_file], check=True)
        print(f"Конвертация завершена, файл сохранен в: {audio_file}")
        
        # После конвертации — проигрываем WAV файл
        play_wav(wav_file)  # Воспроизведение WAV файла
        
        # Удаляем исходный видеофайл после конвертации
        if os.path.exists(video_file):
            os.remove(video_file)
            print(f"Исходное видео {video_file} удалено.")
    
    except Exception as e:
        print(f"Ошибка при конвертации: {str(e)}")


def play_wav(wav_file):
    """Функция для воспроизведения WAV файла"""
    if os.path.exists(wav_file):
        winsound.PlaySound(wav_file, winsound.SND_FILENAME)
    else:
        print(f"Ошибка: WAV файл {wav_file} не найден.")


def progress_hook(d):
    if d['status'] == 'downloading':
        # Выводим прогресс в одной строке
        print(f"\rСкачано: {d['_percent_str']} | Скорость: {d['_speed_str']} | Оставшееся время: {d['_eta_str']}", end="")


def main():
    while True:
        print("Выберите опцию:")
        print("1. Скачать аудио в MP3 (скачивается всё видео, потом конвертируется в аудио)")
        print("2. Скачать видео")

        choice = input("Введите 1 или 2: ").strip()

        if choice == '1':
            url = input("Введите ссылку на видео для скачивания аудио: ").strip()
            if url:
                downloaded_file = download_video(url)  # Скачиваем видео
                convert_to_mp3(downloaded_file)  # Конвертируем его в MP3
            else:
                print("Ссылка не может быть пустой. Попробуйте снова.")
        
        elif choice == '2':
            url = input("Введите ссылку на видео для скачивания: ").strip()
            if url:
                downloaded_file = download_video(url)  # Скачиваем видео
            else:
                print("Ссылка не может быть пустой. Попробуйте снова.")
        
        else:
            print("Некорректный ввод. Пожалуйста, выберите 1 или 2.")
            continue


if __name__ == "__main__":
    main()
