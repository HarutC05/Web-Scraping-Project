from bs4 import BeautifulSoup
import requests
import random


def fetch_quotes():
    url = "https://quotes.toscrape.com/"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")

    quotes = soup.find_all(class_="quote")
    quote_list = []

    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        bio_link = quote.find("a")["href"]
        quote_dict = {
            "text": text,
            "author": author,
            "bio_link": bio_link
        }
        quote_list.append(quote_dict)
    return quote_list


def get_author_bio(bio_link):
    bio_url = "https://quotes.toscrape.com" + bio_link
    bio_request = requests.get(bio_url)
    bio_text = BeautifulSoup(bio_request.text, "html.parser")

    birth_date = bio_text.find("span", class_="author-born-date").get_text()
    birth_location = bio_text.find(
        "span", class_="author-born-location").get_text()
    birth_info = f"Born: {birth_date} {birth_location}"

    full_name = bio_text.find("h3", class_="author-title").get_text()
    names = full_name.split()
    first_initial = names[0][0].upper()
    last_initial = names[-1][0].upper()
    initials_hint = f"Author's initials: {first_initial}.{last_initial}"

    author_description = bio_text.find(
        "div", class_="author-description").get_text(strip=True)

    return [birth_info, initials_hint, author_description]


def play_game():
    quote_list = fetch_quotes()
    while True:
        num_guesses = 4
        random_quote = random.choice(quote_list)
        hints = get_author_bio(random_quote['bio_link'])
        hint_index = 0

        print(f"Quote: {random_quote['text']}")
        print(f"Guesses remaining: {num_guesses}")

        while num_guesses > 0:
            guess = input("Who said this quote?\n")

            if guess.lower() == random_quote['author'].lower():
                print("Correct! You've guessed the author.")
                break
            else:
                num_guesses -= 1
                if num_guesses > 0:
                    print("That is incorrect.")
                    print(f"Guesses Remaining: {num_guesses}")
                    if hint_index < len(hints) and (4 - num_guesses) < len(hints):
                        print(f"Hint: {hints[hint_index]}")
                        hint_index += 1
                else:
                    print(f"Sorry, you're out of guesses. The author was {random_quote['author']}.")

        play_again = input("Do you want to play again? (yes/no)\n").lower()
        if play_again != "yes":
            break


if __name__ == "__main__":
    play_game()
