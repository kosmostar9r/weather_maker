import datetime

from weather_maker import WeatherMaker
from weather_settings import *


class ImageMaker(WeatherMaker):

    def __init__(self, start_date, end_date):
        super().__init__(start_date, end_date)
        self.image = cv2.imread("files/probe.jpg")

    def weather_card(self):
        self.get_forecast()
        for day_info in self.weather_info:
            picture_text_overview = day_info['overview']
            picture_temperature = day_info['temperature']
            picture_date = day_info['date'].strftime('%d-%m-%Y')
            for intent in WEATHER_INTENTS:
                if any(token in picture_text_overview.lower() for token in intent["tokens"]):
                    icon = intent['image']
                    gradient = intent['gradient']
                    break
            else:
                print('no img, sry')
            try:
                self._make_card(picture_text_overview, picture_temperature, picture_date, icon, gradient)
            except UnboundLocalError:
                print('One of variables came wrong')

    def _make_card(self, overview, temp, date, icon, gradient):
        image = cv2.imread("files/probe.jpg")
        make_gradient(image, gradient)

        height, width = image.shape[:2]
        temperature_position = (int(width / 9), int(height / 1.8))
        date_position = (int(width / 3.5), int(height / 1.2))

        if 38 >= len(overview) >= 30:
            overview_position = (int(width / 20), int(height / 5))
            cv2.putText(img=image, text=overview, org=overview_position,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(0, 0, 0))
        elif len(overview) >= 38:
            overview_position = (int(width / 20), int(height / 5))
            cv2.putText(img=image, text=overview, org=overview_position,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=0.7, color=(0, 0, 0))
        else:
            overview_position = (int(width / 6), int(height / 5))
            cv2.putText(img=image, text=overview, org=overview_position,
                        fontFace=cv2.FONT_HERSHEY_COMPLEX_SMALL, fontScale=1, color=(0, 0, 0))

        cv2.putText(img=image, text=temp, org=temperature_position,
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=2, color=(0, 0, 0))
        cv2.putText(img=image, text=date, org=date_position,
                    fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(0, 0, 0))

        weather_icon = cv2.imread(icon)
        rows, cols = weather_icon.shape[:2]
        brows, bcols = image.shape[:2]
        roi = image[int(brows / 2) - int(rows / 2):int(brows / 2) + int(rows / 2),
              int(bcols / 2) - int(cols / 2):int(bcols / 2) + int(cols / 2)]
        weather_icon_fg = cv2.bitwise_and(roi, weather_icon)
        image[int(brows / 2) - int(rows / 2):int(brows / 2) + int(rows / 2),
        int(bcols / 2) - int(cols / 2):int(bcols / 2) + int(cols / 2)] = weather_icon_fg

        image_path = f'weather_images/{date}/'
        image_name = f'{date}.jpg'
        save_image(image, image_path, image_name)


if __name__ == '__main__':
    start_day = datetime.date.today()
    end_day = datetime.date(year=start_day.year, month=start_day.month, day=start_day.day + 2)
    draw_img = ImageMaker(start_day.strftime('%d-%m-%Y'), end_day.strftime('%d-%m-%Y'))
    draw_img.weather_card()
