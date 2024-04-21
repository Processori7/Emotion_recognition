import cv2
from deepface import DeepFace
import os

def take_photo():
    try:
        # Проверяем, существует ли папка img, если нет - создаем
        if not os.path.exists('img'):
            os.makedirs('img')

        # Инициализируем камеру
        cap = cv2.VideoCapture(0)

        # Проверяем, открылась ли камера
        if not cap.isOpened():
            print("Ошибка при открытии камеры!\n")
            main()

        # Считываем кадр
        ret, frame = cap.read()

        # Если кадр успешно считан
        if ret:
            # Получаем список файлов в папке img
            files = os.listdir('img')
            # Находим последний файл в папке
            last_file = max(files, key=lambda x: int(x.split('.')[0])) if files else '0'
            # Получаем номер последнего файла
            last_number = int(last_file.split('.')[0])
            # Формируем имя нового файла
            new_file_name = f"{last_number + 1}.jpg"
            # Сохраняем изображение в папку img
            cv2.imwrite(os.path.join('img', new_file_name), frame)
            print(f"Фотография сохранена как {new_file_name}")
            # Закрываем камеру
            cap.release()
            analyze(f"img\{new_file_name}")
        else:
            print("Ошибка при считывании кадра")

        # Закрываем камеру
        cap.release()
    except Exception as ex:
        print(ex)

def analyze(path):
    try:
        # Путь к вашему изображению
        image_path = path

        # Анализируем эмоции на изображении
        analysis = DeepFace.analyze(image_path, actions=['emotion'])

        # Проверяем, что результат анализа - это словарь, и выводим доминирующую эмоцию
        if isinstance(analysis, dict):
            print("Доминирующая эмоция:", analysis["dominant_emotion"])
        elif isinstance(analysis, list) and len(analysis) > 0:
            # Если результатом является список, выводим эмоции для каждого лица
            for face_analysis in analysis:
                emotion = face_analysis["dominant_emotion"]
                if emotion == "sad":
                    emotion_ru = "грусть"
                elif emotion == "angry":
                    emotion_ru = "злость"
                elif emotion == "surprise":
                    emotion_ru = "удивление"
                elif emotion == "fear":
                    emotion_ru = "страх"
                elif emotion == "happy":
                    emotion_ru = "счастье"
                elif emotion == "disgust":
                    emotion_ru = "отвращение"
                elif emotion == "neutral":
                    emotion_ru = "нейтральное"
                percent = face_analysis["emotion"][emotion]
            print(f"Человек испытывает: {emotion_ru} с вероятностью: {percent}\n")
            main()
        else:
            print("Не удалось определить эмоции.\n")
            main()
    except Exception as ex:
        print(ex)

def show_list_images():
    try:
        # Проверяем, существует ли папка 'img'
        if os.path.exists('img'):
            # Получаем список файлов в папке 'img'
            files = os.listdir('img')
            # Выводим список файлов
            for i, file in enumerate(files, start=1):
                print(f"{i} - {file}")

            # Запрашиваем у пользователя выбор файла
            selected_file = int(input("Выберите файл по номеру: ")) - 1
            # Проверяем, что выбранный файл существует
            if 0 <= selected_file < len(files):
                analyze(f"img\{files[selected_file]}")
            else:
                print("Неверный выбор файла.\n")
                show_list_images()
        else:
            print("Папка 'img' не найдена.\n")
            main()
    except Exception as ex:
        print(ex)
def main():
    try:
        ans = input("Что нужно сделать, введите число:\n1-Сделать фото\n2-Проанализировать фото из списка\n>>>")
        if ans.isdigit():
            if int(ans) == 1:
                take_photo()
            elif int(ans) == 2:
                show_list_images()
            else:
                print("Команда не распознана!\n")
                main()
        else:
            print("Пожалуйста, введите число!\n")
            main()
    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()