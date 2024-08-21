from bs4 import BeautifulSoup
import requests
import random

BASE_URL = "https://quotes.toscrape.com"

def fetch_quotes():
    try:
        response = requests.get(f"{BASE_URL}/")
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        quotes = soup.find_all(class_="quote")
        return [
            {
                "text": quote.find("span", class_="text").get_text(),
                "author": quote.find("small", class_="author").get_text(),
                "bio_link": quote.find("a")["href"]
            }
            for quote in quotes
        ]
    except requests.RequestException as e:
        print(f"Error fetching quotes: {e}")
        return []

def get_author_bio(bio_link):
    bio_url = f"{BASE_URL}{bio_link}"
    try:
        response = requests.get(bio_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        birth_date = soup.find("span", class_="author-born-date").get_text()
        birth_location = soup.find("span", class_="author-born-location").get_text()
        birth_info = f"Born: {birth_date} {birth_location}"

        full_name = soup.find("h3", class_="author-title").get_text()
        initials_hint = get_initials_hint(full_name)

        author_description = soup.find("div", class_="author-description")
        description = author_description.get_text(strip=True) if author_description else "Description not available"

        return [birth_info, initials_hint, description]
    except requests.RequestException as e:
        print(f"Error fetching author bio: {e}")
        return ["Error retrieving bio"]  # Default hint in case of error
    except AttributeError as e:
        print(f"Error parsing bio page: {e}")
        return ["Error retrieving bio"]

def get_initials_hint(full_name):
    names = full_name.split()
    if len(names) > 1:
        first_initial = names[0][0].upper()
        last_initial = names[-1][0].upper()
        return f"Author's initials: {first_initial}.{last_initial}"
    return "Initials not available"

def play_game():
    quote_list = fetch_quotes()
    if not quote_list:
        print("No quotes available. Exiting the game.")
        return

    while True:
        num_guesses = 4
        random_quote = random.choice(quote_list)
        hints = get_author_bio(random_quote['bio_link'])
        hint_index = 0

        print(f"\nQuote: {random_quote['text']}")
        print(f"Guesses remaining: {num_guesses}")

        while num_guesses > 0:
            guess = input("Who said this quote?\n").strip()

            if guess.lower() == random_quote['author'].lower():
                print("Correct! You've guessed the author.")
                break
            else:
                num_guesses -= 1
                if num_guesses > 0:
                    print("That is incorrect.")
                    print(f"Guesses remaining: {num_guesses}")
                    if hint_index < len(hints) and (4 - num_guesses) <= len(hints):
                        print(f"Hint: {hints[hint_index]}")
                        hint_index += 1
                else:
                    print(f"Sorry, you're out of guesses. The author was {random_quote['author']}.")

        if input("Do you want to play again? (yes/no)\n").strip().lower() != "yes":
            break

if __name__ == "__main__":
    play_game()
