import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# code by youssef lmouden

print("WhatsApp spam message 1000, men youssef lmouden, 2024")

# Lists of phrases to generate replies
phrases_intro = [
    "hey kiddo,", "yo,", "so,", "guess what,", "here's the thing,"
]

phrases_jokes = [
    "did you hear the one about the skeleton who stayed out too late?",
    "i would tell you a joke about skeletons, but you wouldn't have the guts.",
    "i'm just dying to make you laugh.",
    "i used to have a skeleton friend, but he was a bonehead.",
    "you look like you've seen a ghost... or is that just my imagination?",
]

phrases_reactions = [
    "ha! gotcha.", "you're pretty good at this.", "don't sweat it, i got tons of jokes left.",
    "oh, you're gonna love this one.", "no bones about it.", "just chill, kiddo."
]

# Function to generate a random phrase
def generate_sans_phrase():
    """Generate a random phrase composed of an introduction, a joke, and a reaction."""
    return f"{random.choice(phrases_intro)} {random.choice(phrases_jokes)} {random.choice(phrases_reactions)}"

# Generate 500 messages once
messages = [generate_sans_phrase() for _ in range(500)]

# Initialize Chrome driver
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH
driver.get('https://web.whatsapp.com')
input("Scan the QR code and press Enter...")

# Find the group
group_name = "3/9"
search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
search_box.click()
search_box.send_keys(group_name)
search_box.send_keys(Keys.ENTER)

time.sleep(1)  # Allow time for the chat to load

# Function to send a message
def send_message(contact, message):
    """Send a message to a specified contact."""
    try:
        # Wait until the message box is ready
        message_box = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p")
        message_box.click()
        message_box.send_keys(message)
        message_box.send_keys(Keys.ENTER)
        print(f"Message sent to {contact}: {message}")
    except Exception as e:
        print(f"Error with the contact {contact}: {e}")

# Input the name of the group or private chat
contact = input("Enter the name of the group or private chat for spam: ")

# Input the number of messages to send
n = input("Enter the number of messages to send: ")
n = int(n)  # Convert the input to an integer

nt = input("Enter the number of seconds to wait between messages: ")
nt = int(nt)  # Convert the input to an integer

# Print a message to let the user know how many messages will be sent
# Send the specified number of random messages from the list
for _ in range(n):
    message = random.choice(messages)  # Select a random message
    send_message(contact, message)      # Send the chosen message
    time.sleep(nt)                      # Wait for nt second before sending the next message

# Close the browser
driver.quit()
