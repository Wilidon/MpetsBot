# сначала месяц, затем -- день. третье число -- день праздника.
holiday_1402 = [213, 215, 214]
holiday_1402_prizes = {"gifts": "14 ангелов",
                       "avatar": "2 ангела",
                       "anketa": "2 ангела"}
holiday_2302 = [222, 224, 223]
holiday_2302_prizes = {"gifts": "26 серебра",
                       "avatar": "3 серебра",
                       "anketa": "3 серебра"}
holiday_308 = [707, 709, 708]
holiday_308_prizes = {"gifts": "9999",
                      "avatar": "9999",
                      "anketa": "9999"}

month = {"01": "января", "02": "февраля", "03": "марта",
         "04": "апреля", "05": "мая", "06": "июня",
         "07": "июля", "08": "августа", "09": "сентября",
         "10": "октярбря", "11": "ноября", "12": "декабря"}

access_name = {0: "Пользователь",
               1: "VIP-игрок",
               2: "Модератор",
               3: "Администратор"}

holiday_0214 = {"gifts": "Обменяться подарками из раздела «Праздники: День Св. Валентина» с 15 разными игроками\n"
                         "📈 Прогресс: {} из {}\n"
                         f"🎖 Награда: {holiday_1402_prizes['gifts']}\n",
                "avatar": "Поставить аватарку на выбор: Влюблённый котик или Влюблённая кошка  на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          f"🎖 Награда: {holiday_1402_prizes['avatar']} \n",
                "anketa": "Поставить «❤️» в анкету на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          f"🎖 Награда: {holiday_1402_prizes['anketa']}\n",
                }

holiday_0214_completed = {
    "gifts": "Обменяться подарками из раздела «Праздники: День Св. Валентина» с 15 разными игроками\n",
    "avatar": "Поставить аватарку на выбор: Влюблённый котик или Влюблённая кошка  на 24 часа\n",
    "anketa": "Поставить «❤️» в анкету на 24 часа\n", }

holiday_0223 = {"gifts": "Обменяться подарками из раздела «23 февраля» с 23 разными игроками\n"
                         "📈 Прогресс: {} из {}\n"
                         f"🎖 Награда: {holiday_2302_prizes['gifts']}\n",
                "avatar": "Поставить аватарку на выбор: Британский кот или Сиамская кошечка  на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          f"🎖 Награда: {holiday_2302_prizes['avatar']}\n",
                "anketa": "Поставить «⭐️» в анкету на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          f"🎖 Награда: {holiday_2302_prizes['anketa']}\n",
                }

holiday_0223_completed = {
    "gifts": "Обменяться подарками из раздела «23 февраля» с 23 разными игроками\n",
    "avatar": "Поставить аватарку на выбор: Британский кот или Сиамская кошечка  на 24 часа\n",
    "anketa": "Поставить «⭐️» в анкету на 24 часа\n", }

holiday_0308 = {"gifts": "Обменяться подарками из раздела «8 марта» с 8 девушками\n"
                         "📈 Прогресс: {} из {}\n"
                         f"🎖 Награда: {holiday_308_prizes['gifts']}\n",
                "avatar": "Поставить аватарку на выбор: Британский кот или Сиамская кошечка  на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          f"🎖 Награда: {holiday_308_prizes['avatar']}\n",
                "anketa": "Поставить «⭐️» в анкету на 24 часа\n"
                          "📈 Прогресс: {} из {}ч\n"
                          f"🎖 Награда: {holiday_308_prizes['anketa']}\n",
                }

holiday_0308_completed = {
    "gifts": "Обменяться подарками из раздела «8 марта» с 8 девушками\n",
    "avatar": "Поставить аватарку на выбор: Британский кот или Сиамская кошечка  на 24 часа\n",
    "anketa": "Поставить «⭐️» в анкету на 24 часа\n", }

rewards = {"user_reward": "1 🌼 и 1-3 🏅 1🧩",
           "club_reward": "1 🦋 и 1-3 🎈 1🧩"}

user_task_log = {"avatar": "Поставить аватар",
                 "anketa": "Сменить анкету",
                 "30online": "Быть онлайн 30 минут",
                 "in_online_15": "Войти в определенное время",
                 "charm": "Набрать очки в игре «Снежки»",
                 "races": "Набрать очки в игре «Скачки»"}

club_task_log = {"coin": "Пополнить копилку монетами",
                 "heart": "Пополнить копилку сердцами",
                 "exp": "Набрать опыт",
                 "get_gift": "Получить подарок {} от любого игрока",
                 "get_random_gift": "Получить подарок от другого "
                                    "игрока",
                 "send_specific_gift_any_player": "Отправить подарок "
                                                  "{} любому "
                                                  "игроку",
                 "send_gift_any_player": "Отправить любой подарок "
                                         "любому игроку",
                 "play": "Сыграть в Поиграйку (Форум Клубы)",
                 "upRank": "Повысить любого игрока в клубе",
                 "downRank": "Понизить любого игрока в клубе",
                 "acceptPlayer": "Принять в клуб любого игрока"}

user_tasks_list = {"avatar": "Поставить аватар {} на 1 час.\n "
                             "📈 Прогресс: {} из {} \n"
                             f"🎖 Награда: {rewards['user_reward']}\n",
                   "anketa": "Сменить данные в «О себе» на 30 минут.\n "
                             "📈 Прогресс: {} из {} \n"
                             f"🎖 Награда: {rewards['user_reward']}\n",
                   "30online": "Не выходить из онлайна 30 минут.\n "
                               "📈 Прогресс: {} из {} \n"
                               f"🎖 Награда: {rewards['user_reward']}\n",
                   "in_online": "Войти в игру в {} по МСК.\n "
                                "📈 Прогресс: {} из {} \n"
                                f"🎖 Награда: {rewards['user_reward']}\n",
                   "charm": "Набрать очки в игре «Снежки»\n"
                            "🔝 Ваш рейтинг: {}\n"
                            "📈 Прогресс: {} из {} \n"
                            f"🎖 Награда: {rewards['user_reward']}\n",
                   "races": "Набрать очки в игре «Скачки»\n"
                            "🔝 Ваш рейтинг: {}\n"
                            "📈 Прогресс: {} из {} \n"
                            f"🎖 Награда: {rewards['user_reward']}\n"
                   }

user_completed_tasks_list = {"avatar": "Поставить аватар {}\n",
                             "anketa": "Сменить данные в «О себе»\n",
                             "30online": "Не выходить из онлайна 30 минут\n",
                             "in_online": "Войти в игру в {} по МСК\n",
                             "charm": "Набрать очки в игре «Снежки»\n",
                             "races": "Набрать очки в игре «Скачки»\n"}

club_tasks_list = {"coin": "Пополнить копилку монетами\n"
                           "📈 Прогресс: {} из {}. \n"
                           f"🎖 Награда: {rewards['club_reward']}\n",
                   "heart": "Пополнить копилку сердцами\n"
                            "📈 Прогресс: {} из {}.\n"
                            f"🎖 Награда: {rewards['club_reward']}\n",
                   "exp": "Набрать опыт\n"
                          "📈 Прогресс: {} из {}\n"
                          f"🎖 Награда: {rewards['club_reward']}\n",
                   "get_gift": "Получить подарок «{}» от любого игрока\n"
                               "📈 Прогресс: {} из {}\n"
                               f"🎖 Награда: {rewards['club_reward']}\n",
                   "get_random_gift": "Получить любой подарок от любого игрока\n"
                                      "📈 Прогресс: {} из {}\n"
                                      f"🎖 Награда: {rewards['club_reward']}\n",
                   "send_specific_gift_any_player": "Отправить подарок «{}» "
                                                    "любому игроку\n"
                                                    "📈 Прогресс: {} из {}\n"
                                                    f"🎖 Награда: {rewards['club_reward']}\n"
                                                    "\nКогда игрок принял "
                                                    "подарок, для проверки "
                                                    "отправьте +check 1, "
                                                    "где 1 — id игрока\n\n",
                   "send_gift_any_player": "Отправить любой подарок любому "
                                           "игроку. \n "
                                           "📈 Прогресс: {} из {}. \n"
                                           f"🎖 Награда: {rewards['club_reward']}\n"
                                           "\nКогда игрок принял "
                                           "подарок, для проверки "
                                           "отправьте +check 1, "
                                           "где 1 — id игрока.\n\n",
                   "chat": "Отправить любое сообщение в клубной чат. \n "
                           "📈 Прогресс: {} из {}. \n"
                           f"🎖 Награда: {rewards['club_reward']}\n",
                   "play": "Сыграть в Поиграйку (Форум Клубы)\n "
                           "📈 Прогресс: {} из {}. \n"
                           f"🎖 Награда: {rewards['club_reward']}\n",
                   "thread": "Написать сообщение в топике вашего клуба "
                             "на гостевом форуме \n "
                             "📈 Прогресс: {} из {}. \n"
                             f"🎖 Награда: {rewards['club_reward']}\n",
                   "upRank": "Повысить любого игрока в клубе \n "
                             "📈 Прогресс: {} из {}. \n"
                             f"🎖 Награда: {rewards['club_reward']}\n",
                   "downRank": "Понизить любого игрока в клубе \n "
                               "📈 Прогресс: {} из {}. \n"
                               f"🎖 Награда: {rewards['club_reward']}\n",
                   "acceptPlayer": "Принять в клуб любого игрока. \n "
                                   "📈 Прогресс: {} из {}. \n"
                                   f"🎖 Награда: {rewards['club_reward']}\n",
                   }

club_completed_tasks_list = {"coin": "Пополнить копилку монетами. \n",
                             "heart": "Пополнить копилку сердцами. \n",
                             "exp": "Набрать опыт. \n",
                             "get_gift": "Получить подарок {} от любого игрока. \n",
                             "get_random_gift": "Получить подарок от другого "
                                                "игрока. \n",
                             "send_specific_gift_any_player": "Отправить подарок "
                                                              "{} любому "
                                                              "игроку.\n",
                             "send_gift_any_player": "Отправить любой подарок "
                                                     "любому игроку.\n",
                             "send_gift_player": "Отправить подарок от игроку {}.\n",
                             "send_specific_gift_player": "Отправить подарок {} "
                                                          "игроку {}.\n",
                             "send_gift": "Отправить подарок другому игроку. \n",
                             "chat": "Отправить любое сообщение в клубной чат. \n",
                             "play": "Сыграть в Поиграйку (Форум Клубы) \n",
                             "thread": "Написать сообщение в топике "
                                       "вашего клуба на гостевом форуме\n",
                             "upRank": "Повысить любого игрока в клубе. \n",
                             "downRank": "Понизить любого игрока в клубе. \n",
                             "acceptPlayer": "Принять в клуб любого игрока. \n"}

gifts_name = [[1, "🍓Клубничка"], [2, "🦋Бабочка"],
              [3, "🧳 Чемодан с деньгами"],
              [4, "🐰Ушки зайки"], [5, "💍 Кольцо в ракушке"],
              [6, "🍹Апельсиновый сок"], [7, "🥥 Кокосовый сок"],
              [8, "🌹 Букет роз"], [9, "🏝 Остров"],
              [10, "🥤Лимонад с семечками"],
              [11, "💘Сердечко"], [12, "🐿Скрат"],
              [13, "⚽️Футбольный мяч"], [14, "☕️ Кофе"], [15, "🏍 Мотоцикл"],
              [16, "🍨Мороженое"], [17, "🧸Влюблённые мишки"],
              [18, "🐇Игрушечный зайчик"],
              [19, "🚢 Корабль"], [20, "🍕Пицца"], [21, "🎐Ёлочный шарик"],
              [22, "🎄Ёлочка"],
              [23, "⛄️Снеговик"], [24, "🎅Дед Мороз"],
              [25, "🍷Бутылка вина"], [26, "🚂Танк"],
              [27, "👨🏻‍✈️Шляпа офицера"],
              [28, "🥮Тортик в виде сердца"],
              [29, "🎂Праздничный торт"], [30, "💍Кольцо"],
              [31, "🐭Мышка в мешке"], [32, "🥢Волшебная палочка"],
              [33, "🧙🏻‍♀️Шляпа колдуньи"],
              [34, "👼Ангел Амур"], [35, "🕵🏻‍♀️Девушка"], [45, "🌼Ромашка"],
              [46, "🍫Шоколадка"],
              [47, "🐈Рыжий котик"], [48, "🍋Чай с лимоном"],
              [49, "🐱Манэки-нэко"],
              [50, "🐲Монстрик"],
              [51, "🦝 Енотик"], [52, "🚗 Машина"]]

avatar_name = [[0, "Кошечка"], [1, "Котенок"], [3, "Игривая кошечка"],
               [4, "Влюбленный котик"], [5, "Игривый котик"],
               [6, "Сиамская кошечка"], [7, "Британский котик"],
               [8, "Влюбленная кошечка"], [9, "Лисичка"],
               [10, "Хомячок"], [11, "Дракончик"], [12, "Щенок"],
               [13, "Собачка"], [16, "Сова"], [17, "Панда"],
               [18, "Кролик"], [19, "Тигренок"], [20, "Черепашка"]]

prizes = {10: "Монетка удачи",
          25: "200 монет",
          40: "5m ❤️",
          70: "25 золотых перьев и 5 ⭐️",
          100: "shop_1",
          125: "shop_2",
          160: "400 монет",
          177: "shop_3"}

c_prizes = {30: "2 ⭐️ всем участвующим",
            70: "300 монет в копилку клуба",
            160: "200k опыта",
            230: "5m ❤️ в копилку клуба и по 5 👼 всем участвующим",
            350: "15 🎄 и 5 🎈",
            510: "1 🔑 и по 15 серебра всем участвующим",
            620: "10m ❤️",
            800: "2’000 монет",
            980: "по 1 ⚙️ и по 1 монетке удачи всем участвующим",
            1111: "400k опыта в копилку, 15m ❤️ и 1 🎁 всем участвующим",
            1239: "2 🔑 и 10 🎈"}

shop1 = {"item1": "300 монет",
         "item2": "2 волшебных шестерни",
         "item3": "20 ангелов"}
shop2 = {"item1": "17 серебра",
         "item2": "5m ❤",
         "item3": "2 монетки удачи",
         "item4": "13 ангелов"}
shop3 = {"item1": "15🏅",
         "item2": "5m ❤",
         "item3": "4 ⚙",
         "item4": "10 👼",
         "item5": "15 🍿",
         "item6": "5 ⭐️"}

numbers = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']

collections = {1: {"name": "Книжный червь",
                   "required": [{"amount": 5, "icon": "📇"},
                                {"amount": 4, "icon": "⌛️"},
                                {"amount": 2, "icon": "📖"},
                                {"amount": 1, "icon": "💡"},
                                {"amount": 3, "icon": "☕️"}],
                   "reward": "50 золотых перьев"},
               2: {"name": "Киноман",
                   "required": [{"amount": 5, "icon": "🖥"},
                                {"amount": 4, "icon": "💿"},
                                {"amount": 2, "icon": "🎞"},
                                {"amount": 1, "icon": "🍿"},
                                {"amount": 3, "icon": "🕹"}],
                   "reward": "50 попкорна"},
               3: {"name": "От дяди Скруджа",
                   "required": [{"amount": 5, "icon": "💰"},
                                {"amount": 4, "icon": "💸"},
                                {"amount": 2, "icon": "💎"},
                                {"amount": 1, "icon": "🏦"},
                                {"amount": 3, "icon": "🏅"}],
                   "reward": "5 монеток удачи"},
               4: {"name": "Связка ключей",
                   "required": [{"amount": 5, "icon": "🗝"},
                                {"amount": 4, "icon": "🧸"},
                                {"amount": 2, "icon": "🗺"},
                                {"amount": 1, "icon": "🏡"},
                                {"amount": 3, "icon": "🏆"}],
                   "reward": "2 ключа"},
               5: {"name": "Небесное хранилище",
                   "required": [{"amount": 5, "icon": "☁️"},
                                {"amount": 4, "icon": "✨"},
                                {"amount": 2, "icon": "🛩"},
                                {"amount": 1, "icon": "🕊"},
                                {"amount": 3, "icon": "😇"}],
                   "reward": "33 ангела"},
               }
