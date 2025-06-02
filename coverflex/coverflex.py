from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# --- CONFIGURATION ---
EMAIL = "YOUR_EMAIL_HERE"
PASSWORD = "YOUR_PASSWORD_HERE"
LOGIN_URL = "https://my.coverflex.com/signin"
MEAL_URL = "https://my.coverflex.com/meal/activity"
BENEFITS_URL = "https://my.coverflex.com/benefits"
MEAL_CSV_FILE = "coverflex_meal.csv"
BENEFITS_CSV_FILE = "coverflex_benefits.csv"

# --- START WEBDRIVER ---
chrome_options = Options()
# Uncomment the next line to run headless
# chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=chrome_options)

def export_meal_csv():
    """
    Extracts Meal transactions from Coverflex and exports them to a CSV file.
    """
    driver.get(MEAL_URL)
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, ".css-g5y9jx.flex.flex-col.gap-section")
        print("✅ Meal transactions page loaded!")
    except Exception:
        print("❌ Could not find the meal transactions table.")
        return

    meses = driver.find_elements(By.CSS_SELECTOR, ".css-g5y9jx.flex.flex-col.gap-md")
    print(f"Months found: {len(meses)}")
    meses_disponiveis = []
    blocos_movimentos = []

    # Collect available months and their transaction blocks
    for mes in meses:
        try:
            nome_mes = mes.find_element(By.CSS_SELECTOR, "div.font-F37.text-md").text.strip()
            meses_disponiveis.append(nome_mes)
            bloco = mes.find_element(By.CSS_SELECTOR, "div.flex.flex-col.rounded-xl.overflow-hidden")
            blocos_movimentos.append(bloco)
        except Exception:
            continue

    print("\nAvailable months for export:")
    print("0 - All")
    for idx, nome in enumerate(meses_disponiveis, 1):
        print(f"{idx} - {nome}")

    escolha = input("Select the month number to export (0 for all): ").strip()
    try:
        escolha = int(escolha)
    except Exception:
        print("Invalid selection.")
        return

    data = []
    for idx, bloco in enumerate(blocos_movimentos):
        if escolha != 0 and escolha != idx + 1:
            continue
        movimentos = bloco.find_elements(By.CSS_SELECTOR, "div.flex-row.items-center.justify-between.gap-sm.py-md")
        for mov in movimentos:
            try:
                descricao = mov.find_element(By.CSS_SELECTOR, "div.font-F37.text-sm.text-neutral30").text.strip()
                data_mov = mov.find_element(By.CSS_SELECTOR, "div.font-F37.text-sm.text-neutral20").text.strip()
                valor_raw = mov.find_element(By.CSS_SELECTOR, "div.font-F37Bold.text-sm").text.strip()
                valor = float(valor_raw.replace("€", "").replace(",", ".").replace("+", "").replace("−", "-").strip())
                if valor < 0:
                    entrada = ""
                    saida = abs(valor)
                    tipo = "SAIDA"
                else:
                    entrada = valor
                    saida = ""
                    tipo = "ENTRADA"
                data.append([data_mov, descricao, entrada or saida, tipo])
            except Exception:
                continue

    with open(MEAL_CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Description", "Amount", "Type"])
        writer.writerows(data)
    print(f"✅ Exported {len(data)} meal transactions to {MEAL_CSV_FILE}")

def export_benefits_csv():
    """
    Extracts Benefits transactions from Coverflex and exports them to a CSV file.
    """
    driver.get(BENEFITS_URL)
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, ".css-g5y9jx.flex.flex-col.gap-section")
        print("✅ Benefits transactions page loaded!")
    except Exception:
        print("❌ Could not find the benefits transactions table.")
        return

    meses = driver.find_elements(By.CSS_SELECTOR, ".css-g5y9jx.flex.flex-col.gap-md")
    print(f"Months found: {len(meses)}")
    meses_disponiveis = []
    blocos_movimentos = []

    # Collect available months and their transaction blocks
    for mes in meses:
        try:
            nome_mes = mes.find_element(By.CSS_SELECTOR, "div.font-F37.text-md").text.strip()
            meses_disponiveis.append(nome_mes)
            bloco = mes.find_element(By.CSS_SELECTOR, "div.flex.flex-col.rounded-xl.overflow-hidden")
            blocos_movimentos.append(bloco)
        except Exception:
            continue

    print("\nAvailable months for export:")
    print("0 - All")
    for idx, nome in enumerate(meses_disponiveis, 1):
        print(f"{idx} - {nome}")

    escolha = input("Select the month number to export (0 for all): ").strip()
    try:
        escolha = int(escolha)
    except Exception:
        print("Invalid selection.")
        return

    data = []
    for idx, bloco in enumerate(blocos_movimentos):
        if escolha != 0 and escolha != idx + 1:
            continue
        movimentos = bloco.find_elements(By.CSS_SELECTOR, "div.flex-row.items-center.justify-between.gap-sm.py-md")
        for mov in movimentos:
            try:
                descricao = mov.find_element(By.CSS_SELECTOR, "div.font-F37.text-sm.text-neutral30").text.strip()
                data_mov = mov.find_element(By.CSS_SELECTOR, "div.font-F37.text-sm.text-neutral20").text.strip()
                valor_raw = mov.find_element(By.CSS_SELECTOR, "div.font-F37Bold.text-sm").text.strip()
                valor = float(valor_raw.replace("€", "").replace(",", ".").replace("+", "").replace("−", "-").strip())
                if valor < 0:
                    entrada = ""
                    saida = abs(valor)
                    tipo = "SAIDA"
                else:
                    entrada = valor
                    saida = ""
                    tipo = "ENTRADA"
                data.append([data_mov, descricao, entrada or saida, tipo])
            except Exception:
                continue

    with open(BENEFITS_CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Description", "Amount", "Type"])
        writer.writerows(data)
    print(f"✅ Exported {len(data)} benefits transactions to {BENEFITS_CSV_FILE}")

try:
    print("Choose an option:")
    print("1 - Automatic login (fills email/password and pauses for 2FA)")
    print("2 - I am already logged in, just export CSV")
    op = input("Option (1/2): ").strip()

    if op == "1":
        driver.get(LOGIN_URL)
        print("Login page loaded.")
        WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.ID, "email")))
        email_input = driver.find_element(By.ID, "email")
        password_input = driver.find_element(By.ID, "password")
        email_input.clear()
        email_input.send_keys(EMAIL)
        password_input.clear()
        password_input.send_keys(PASSWORD)
        print("Credentials filled.")
        login_button = driver.find_element(By.CLASS_NAME, "css-146c3p1")
        login_button.click()
        print("Login button clicked.")
        input("If prompted, enter the 2FA code in the browser and press ENTER here to continue...")
    elif op == "2":
        print("The Selenium browser will open. Log in manually and press ENTER here to continue...")
        driver.get(LOGIN_URL)
        input("After logging in, press ENTER to continue...")
    else:
        print("Invalid option.")

    # Export Meal transactions
    export_meal_csv()
    # Export Benefits transactions
    export_benefits_csv()

finally:
    driver.quit()  # Comment or remove this line if you want to keep the browser open