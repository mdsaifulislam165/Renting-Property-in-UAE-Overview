from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

column_titles = ["Verification Status", "Agent Type", "Property Type", "Rent Amount (AED/YR)", "Features", "Listing Level", "Location", "No of Bedroom", "No of Bathroom", "Area in sqft"]

def rent_details(rent_items):
    db = {}
    
    # Taking the 2 side by side section
    sec_top_left = rent_items.find_element(By.XPATH, "article/div/div/section[1]/div/div[1]") # .text has 4 divs
    sec_top_right = rent_items.find_element(By.XPATH, "article/div/div/section[2]") # .text grabs 8 main features
    
    agent_info = sec_top_left.text.split('\n')
    features = sec_top_right.text.split('\n')
    len_features = len(features)    

    try:
        for info in agent_info:
            capitalized = info.capitalize()
            if capitalized == "Verified":
                db["Verification Status"] = "Verified"
                break
            else:
                db["Verification Status"] = "Not Verified"
        for info in agent_info:
            capitalized = info.capitalize()
            if capitalized == "Superagent":
                db["Agent Type"] = "Superagent"
                break
            else:
                db["Agent Type"] = "Not Superagent"
    except Exception as e:
        print(e)
        db = {}
        return db
    
    # Appending the 8 features of a property
    try:               
        if len_features == 8:
            db["Property Type"] = features[0]
            db["Rent Amount (AED/YR)"] = int(features[1].split(" ")[0].replace(",", ""))
            db["Features"] = features[2]
            db["Listing Level"] = features[3].capitalize()
            db["Location"] = features[4]
            db["No of Bedroom"] = features[5]
            db["No of Bathroom"] = features[6]
            try:
                db["Area in sqft"] = int(features[7].split(" ")[0].replace(",", ""))
            except:
                db["Area in sqft"] = int(features[7].split(" ")[0])
        elif len_features == 7:
            db["Property Type"] = features[0]
            db["Rent Amount (AED/YR)"] = int(features[1].split(" ")[0].replace(",", ""))
            db["Features"] = features[2]
            db["Listing Level"] = "Not Premium"
            db["Location"] = features[3]
            db["No of Bedroom"] = features[4]
            db["No of Bathroom"] = features[5]
            try:
                db["Area in sqft"] = int(features[6].split(" ")[0].replace(",", ""))
            except:
                db["Area in sqft"] = int(features[6].split(" ")[0])
        
    except Exception as e:
        print(e)
        db = {}
        return db

    return db


def main():
    rent_data = []                  # keeping all the data here > transfer to PANDAS
    driver = webdriver.Edge()       # any problem if outside?
    
    for page_id in range(1, 4001):     # Iterate through the pages
        url = f"https://www.propertyfinder.ae/en/rent/properties-for-rent.html?page={page_id}"
        driver.get(url)
        
        # picking the list items -- 25 items per page 
        rent_items = driver.find_elements(By.XPATH, "//li[@role='listitem']")
        
        total_rent_items = len(rent_items)
        # iterating each item to scrape the necessary data > appending to rent_data
        for i in range(total_rent_items):
            rent_data.append(rent_details(rent_items[i]))
    
    driver.close()
    
    df = pd.DataFrame(data=rent_data, columns=column_titles)
    df.to_csv("Property_Finder_Rent_Items_in_Abu_Dhabi", index=False)
    
    return

if __name__ == "__main__":
    main()
