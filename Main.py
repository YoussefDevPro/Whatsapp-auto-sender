from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests

API_TOKEN = "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"
MODEL_NAME = "Qwen/Qwen2.5-72B-Instruct"  # Always use this model

headers = {"Authorization": f"Bearer {API_TOKEN}"}

# XPaths constants
SEARCH_BOX_XPATH = '//div[@contenteditable="true"][@data-tab="3"]'
MESSAGE_INPUT_XPATH = '/html/body/div[1]/div/div/div[3]/div[4]/div/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'
MESSAGES_XPATH = "(//div[contains(@class, 'message-in')]//span[contains(@class, 'selectable-text') or contains(@class, 'copyable-text')])[last()]"

def talk_with_model(message):
    """Uses the Qwen model to respond to a message."""
    print(f"Message sent to the model: {message}")
    url = f"https://api-inference.huggingface.co/models/{MODEL_NAME}"

    payload = {"inputs": message}
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data[0]["generated_text"]
    except requests.RequestException as e:
        print("Error with the API:", e)
        return "Sorry, there was an error with the API."

def replace_newlines_with_period(text):
    """Replace new lines with periods."""
    return text.replace("\n", ". ")

def send_message(driver, text):
    """Sends a message to the group."""
    try:
        message_box = driver.find_element(By.XPATH, MESSAGE_INPUT_XPATH)
        message_box.click()
        message_box.send_keys(text)
        message_box.send_keys(Keys.ENTER)
        print(f"Message sent: {text}")
    except Exception as e:
        print("Error sending the message:", e)

def main():
    """Main entry point for the script execution."""
    driver = webdriver.Chrome()  # Ensure that chromedriver is in your PATH
    driver.get('https://web.whatsapp.com')
    input("Scan the QR code and press Enter...")

    group_name = input("Enter your discussion group name: ")
    search_box = driver.find_element(By.XPATH, SEARCH_BOX_XPATH)
    search_box.click()
    search_box.send_keys(group_name)
    search_box.send_keys(Keys.ENTER)

    last_message = ""
    no_message_sent = True

    try:
        while True:
            messages = driver.find_elements(By.XPATH, MESSAGES_XPATH)

            if messages:
                current_message = messages[-1].text

                if current_message != last_message:
                    last_message = current_message
                    print(f"Last message: {last_message}")

                    response_message = talk_with_model(last_message)
                    response_message = replace_newlines_with_period(response_message)
                    send_message(driver, response_message)
                    no_message_sent = False

            if no_message_sent:
                send_message(driver, "There are no new messages.")
                no_message_sent = False

            time.sleep(0.5)

    except KeyboardInterrupt:
        print("Script stopped by the user.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()  # Executes the main script
