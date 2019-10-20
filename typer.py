from selenium import webdriver
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Firefox()

driver.get('https://thetypingcat.com/typing-speed-test/1m')

sleep(2)

enter_key = ''
with open('enter_key.pkl', 'r') as file:
    enter_key = file.read()
# print(enter_key)

def get_spaced_words(input_element):
    word_list = input_element.get_attribute('innerHTML').split('<i class="spacer"> </i>')
    word_list[0] = word_list[0].split('<span>')[1]
    word_list[-1] = word_list[-1].split('</span>')[0]
    word_list_sentence = ' '.join(word_list)
    return word_list_sentence

def get_words_to_type():

    words = []

    active_words = driver.find_elements_by_xpath('//div[contains(@class, "line") and contains(@class, "active")]/span')

    words.append(active_words[0].get_attribute('innerText'))


    words.append(get_spaced_words(active_words[1]))

    active_words = driver.find_elements_by_xpath('//div[contains(@class, "line") and contains(@class, "next")]/span')

    for word in active_words:
        words.append(get_spaced_words(word))

    active_words = driver.find_elements_by_xpath('//div[@class="line"]')

    for word in active_words:
        words.append(word.get_attribute('innerText'))

    words = ''.join(words)
    
    # words.replace(' ', ':SPACE')
    words.replace(enter_key, ':ENTER')
    # print(words)
    return words

def send_words(words):
    action = ActionChains(driver)
    action.send_keys(words)
    action.perform()

# print(get_words_to_type())
send_words(get_words_to_type())
# driver.close()