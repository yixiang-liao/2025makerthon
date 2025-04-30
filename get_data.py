import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import re

tool_url = "https://www2.e-show.tw/edit_makerthon/index.php?option=productm&lang=cht&task=showlist2&id=8"
equipment_url = "https://www2.e-show.tw/edit_makerthon/index.php?option=productm&lang=cht&task=showlist2&id=6"

user_agent = UserAgent()

def get_equipment_data():
    req = requests.get(equipment_url, headers={ 'user-agent': user_agent.random }, timeout=5)
    soup = BeautifulSoup(req.text, 'lxml')

    results = []

    for tab in soup.select('div.tab-content'):
        rows = tab.select('tbody tr')
        for row in rows:
            cols = row.find_all('td')
            if len(cols) < 6:
                continue
            category = cols[1].get_text(strip=True)
            name = cols[2].get_text(strip=True)
            spec = cols[3].get_text(strip=True)
            admitted = [li.get_text(strip=True) for li in cols[4].find_all('li')]
            waiting = [li.get_text(strip=True) for li in cols[5].find_all('li')]

            results.append({
                "類別": category,
                "名稱": name,
                "規格": spec,
                "正取": admitted,
                "候補": waiting
            })

    return results

def get_tool_data():
    req = requests.get(tool_url, headers={ 'user-agent': user_agent.random }, timeout=5)
    soup = BeautifulSoup(req.text, 'lxml')
    rows = soup.select('div.table-responsive tbody tr')

    tool_data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) != 2:
            continue
        idx = int(cols[0].get_text(strip=True))
        team_info = cols[1].get_text(strip=True)

        match = re.match(r"(.+)\s+\((\d+)\)", team_info)
        if match:
            name, code = match.groups()
            tool_data.append({
                "編號": idx,
                "團隊": name.strip(),
                "代碼": code.strip()
            })

    return tool_data

def main():
    output = {
        "設備預約資料": get_equipment_data(),
        "工具可領取名單": get_tool_data()
    }

    print(json.dumps(output, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
