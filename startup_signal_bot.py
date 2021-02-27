from signalBot import signalBot

settings = signalBot.Settings()
json_data_list = signalBot.get_messages(settings.signal_number, settings=settings)

signalBot.prepare_background_image(json_data_list, settings=settings)

