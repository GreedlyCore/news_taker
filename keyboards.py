from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


class keyboard:
    @staticmethod
    def main():
        kb_mm = ReplyKeyboardMarkup(True)
        kb_mm.row('📤Получить статью', '⚖Калибровка')
        kb_mm.row('⏰Рассылка', '⚙Настройки')
        kb_mm.row('Источники')

        return kb_mm

    @staticmethod
    def calibration():
        kb = ReplyKeyboardMarkup(True)
        kb.row('Список', 'Пробные статьи')
        kb.row('Назад')
        return kb

    @staticmethod
    def calibration_list():
        kb = ReplyKeyboardMarkup(True)

        kb.row('health_medicine', 'mind_brain', 'living_well')
        kb.row('matter_energy', 'space_time', 'computers_math')
        kb.row('plants_animals', 'earth_climate', 'fossils_ruins')
        kb.row('science_society', 'business_industry', 'education_learning')
        kb.row('Назад')
        return kb

    @staticmethod
    def rate(theme, id):
        kb = InlineKeyboardMarkup()
        kb.row(
            InlineKeyboardButton('👍', callback_data=f"1 {theme} {id}"),
            InlineKeyboardButton('🤷‍', callback_data=f"0.5 {theme} {id}"),
            InlineKeyboardButton('👎', callback_data=f"-1 {theme} {id}"),
        )
        return kb

    @staticmethod
    def settings():
        kb = ReplyKeyboardMarkup(True)
        kb.row('Статистика')
        kb.row('🧨Сбросить рекомендации', '🧠Сбросить статистику')
        kb.row('Назад')
        return kb
